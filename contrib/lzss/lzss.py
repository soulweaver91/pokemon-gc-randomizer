"""
Based on the unfit implementation from https://gist.github.com/nucular/258d544bbd1ba401232ae83a11bd8857
with default values also changed for the purposes of this project.

Original C implementation by Okumura Haruhiko (public domain)
"""

import logging


STALE_LIMIT = 4096 - 16 - 2


class LZSSBase(object):
    def __init__(self, infile, outfile, EI=12, EJ=4, P=2, N=0, F=0, rless=2, init_chr=b'\x00'):
        self.infile = infile
        self.outfile = outfile

        self.EI = EI
        self.EJ = EJ
        self.P = P
        self.N = N or (1 << self.EI)
        self.F = F or (1 << self.EJ)
        self.rless = rless

        if isinstance(init_chr, int):
            self.init_chr = init_chr
        else:
            self.init_chr = init_chr[0]

        self.buffer = bytearray(self.N)


class LZSSDictionaryNode:
    def __init__(self, depth, file_pos):
        self.subnodes = {}
        self.value = None

        self.depth = depth
        self.file_pos = file_pos

    def __getitem__(self, i):
        return self.subnodes[i]

    def __setitem__(self, i, v):
        self.subnodes[i] = v

    def __delitem__(self, i):
        del self.subnodes[i]

    def store(self, s, file_pos):
        self.update_position(file_pos)

        if len(s) == 0:
            return

        if s[0] not in self.subnodes.keys():
            self[s[0]] = LZSSDictionaryNode(self.depth + 1, file_pos)

        self[s[0]].store(s[1:], file_pos)

    def find(self, s, file_pos):
        if len(s) == 0 or self.file_pos < file_pos - STALE_LIMIT:
            match_start, match_len = self.file_pos, self.depth
        elif s[0] not in self.subnodes.keys():
            match_start, match_len = self.file_pos, self.depth
        else:
            match_start, match_len = self[s[0]].find(s[1:], file_pos)

            if match_start < file_pos - STALE_LIMIT:
                match_start, match_len = self.file_pos, self.depth
                del self[s[0]]

        return match_start, match_len

    def update_position(self, new_pos):
        if new_pos > self.file_pos:
            self.file_pos = new_pos

    def gc(self, file_pos):
        keys = list(self.subnodes.keys())
        for key in keys:
            if self[key].file_pos < file_pos - STALE_LIMIT:
                del self[key]
            else:
                self[key].gc(file_pos)


class LZSSDictionary:
    # This determines how often the QC is run: every nth time the upper buffer is mirrored, i.e. every n * 4 kB.
    # Nodes also do lazy self-cleanup whenever they would be returning a stale node (see the deletion in their
    # find function). 16 kB was determined to be the sweet spot when it comes to efficiency; more time is lost
    # either GCing or maintaining an unnecessarily large dictionary tree with both larger and smaller multipliers.
    ROUNDS_FOR_GC = 4

    def __init__(self):
        self.subnodes = {}
        self.rounds_for_gc = self.ROUNDS_FOR_GC

    def __getitem__(self, i):
        return self.subnodes[i]

    def __setitem__(self, i, v):
        self.subnodes[i] = v

    def __delitem__(self, i):
        del self.subnodes[i]

    def store(self, s, file_pos, start_before):
        if len(s) == 0:
            return

        for i in reversed(range(len(s))):
            ss = s[-(i + 1):][:18]
            pos = file_pos + (len(s) - i - 1)

            if pos >= start_before:
                continue

            if ss[0] not in self.subnodes.keys():
                self[ss[0]] = LZSSDictionaryNode(1, pos)

            self[ss[0]].store(ss[1:], pos)

    def find(self, s, file_pos):
        if s[0] not in self.subnodes.keys() or len(s) < 2:
            return 0, 0
        else:
            match_start, match_len = self[s[0]].find(s[1:], file_pos)

        return match_start, match_len

    def maybe_gc(self, file_pos):
        # The garbage collector goes through the entire node tree and prunes all known sequences that were last
        # encountered so long ago that they are not in the buffer anymore. Notably, if a node is deemed stale, that
        # entire subtree can be immediately also deemed stale and removed, since it is not possible to encounter i.e.
        # a sequence starting with "GAM" at a later point than any sequence starting with "GA".
        # Garbage collecting would strictly not be necessary, but with large files (like common_rel at 707 kB),
        # the massive node tree will eventually make Python munch upwards of 2 GB of RAM, so it very much makes sense.
        # Moreover, the code performs better with smaller subnode hashes anyway, making a properly GC'd code run
        # faster, too.
        self.rounds_for_gc -= 1
        if self.rounds_for_gc == 0:
            keys = list(self.subnodes.keys())
            for key in keys:
                if self[key].file_pos < file_pos - STALE_LIMIT:
                    del self[key]
                else:
                    self[key].gc(file_pos)

            self.rounds_for_gc = self.ROUNDS_FOR_GC


class LZSSEncoder(LZSSBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buffer = bytearray(self.N * 2)

        self.flag_byte = 0
        self.flag_bits_written = 0
        self.data_buffer = bytearray()

        self.codecount = 0
        self.textcount = 0

    def get_buffer_ref_bytes(self, pos, length):
        low_byte = pos % 256
        high_byte = (pos // 256 << self.EJ) + (length - self.P - 1)
        return bytes((low_byte, high_byte))

    def maybe_write_bytes(self, eof=False):
        if self.flag_bits_written == 8 or (eof and self.flag_bits_written > 0):
            self.outfile.write(bytes((self.flag_byte, )))
            self.outfile.write(self.data_buffer)

            self.flag_bits_written = 0
            self.flag_byte = 0
            self.data_buffer = bytearray()
        pass

    def store_literal_flag(self):
        self.flag_byte |= (1 << self.flag_bits_written)
        self.flag_bits_written += 1
        self.codecount += 1
        self.maybe_write_bytes()

    def store_reference_flag(self):
        self.flag_bits_written += 1
        self.codecount += 1
        self.maybe_write_bytes()

    def store_literal(self, c):
        self.data_buffer.append(c)
        self.store_literal_flag()

    def store_reference(self, x, y):
        self.data_buffer.extend(self.get_buffer_ref_bytes(x, y))
        self.store_reference_flag()

    def encode(self):
        F2 = self.F + self.P

        # Fill first half of the buffer with init character
        for i in range(0, self.N - F2):
            self.buffer[i] = self.init_chr

        # Read data into the remainder of the buffer
        for i in range(self.N - F2, self.N * 2):
            buffer_end = i
            z = self.infile.read(1)

            if len(z) == 0:
                break

            self.buffer[i] = z[0]
            self.textcount += 1

        encode_head = self.N - F2
        effective_head = encode_head

        dictionary = LZSSDictionary()
        dictionary.store(self.buffer[encode_head - F2 - 1:encode_head + F2 + 1], encode_head - F2 - 1, encode_head)

        while encode_head < buffer_end:
            max_match_len = min(F2, buffer_end - encode_head)

            match_start, match_len = dictionary.find(self.buffer[encode_head:encode_head + max_match_len],
                                                     effective_head)

            if match_len <= self.P:
                match_len = 1
                self.store_literal(self.buffer[encode_head])
            else:
                self.store_reference(match_start & (self.N - 1), match_len)

            dictionary.store(self.buffer[encode_head:min(encode_head + match_len + F2, buffer_end + 1)], effective_head,
                             effective_head + match_len)

            encode_head += match_len
            effective_head += match_len

            if encode_head >= self.N * 2 - F2:
                logging.debug('  %.2fkB encoded in %.2fkB', self.textcount / 1024, self.outfile.tell() / 1024)
                offset_from_boundary = (encode_head - (self.N * 2 - F2))

                dictionary.maybe_gc(effective_head)

                # Mirror the upper buffer half to the bottom
                self.buffer[0:self.N] = self.buffer[self.N:self.N * 2]

                # Move to the end of the bottom buffer
                buffer_end -= self.N
                encode_head -= self.N

                # Read data to the upper buffer
                while buffer_end < self.N * 2 - self.P:
                    buffer_end += 1

                    z = self.infile.read(1)
                    if len(z) == 0:
                        break

                    self.textcount += 1
                    self.buffer[buffer_end] = z[0]

                # Add buffer border crossing dictionary entries
                for i in reversed(range(0, offset_from_boundary)):
                    dictionary.store(self.buffer[encode_head - F2 - 1 - i:encode_head + F2 + 1 - i],
                                     effective_head - F2 - 1 - i, effective_head - i)

        self.maybe_write_bytes(True)
        logging.debug('  %.2fkB encoded in %.2fkB', self.textcount / 1024, self.outfile.tell() / 1024)

        return self.textcount, self.codecount


class LZSSDecoder(LZSSBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bit_buffer = 0
        self.bit_mask = 256

    def get_next_flag(self):
        if self.bit_mask >= 256:
            z = self.infile.read(1)
            if len(z) == 0:
                return None
            self.bit_buffer = z[0]
            self.bit_mask = 1

        x = self.bit_buffer & self.bit_mask
        self.bit_mask <<= 1

        return x

    def decode(self):
        # Initialize buffer with init character
        for i in range(0, self.N):
            self.buffer[i] = self.init_chr

        # current buffer position
        r = (self.N - self.F) - self.rless

        buffer_bitmask = self.N - 1
        copy_count_bitmask = self.F - 1

        while True:
            c = self.get_next_flag()

            if c is None:
                # End of the file
                break
            if c:
                # Bit is on, read next byte from file to buffer and output
                c = self.infile.read(1)
                if len(c) == 0:
                    break
                self.outfile.write(c)
                self.buffer[r] = c[0]
                r = (r + 1) & buffer_bitmask
            else:
                # Bit is off, read bytes from buffer to buffer and output
                low_byte = self.infile.read(1)
                if len(low_byte) == 0:
                    break

                high_byte = self.infile.read(1)
                if len(high_byte) == 0:
                    break

                low_byte = low_byte[0]
                high_byte = high_byte[0]

                # Calculate start offset to read from
                buffer_start = low_byte | ((high_byte >> self.EJ) << 8)
                # Calculate the number of bytes to copy
                copy_count = (high_byte & copy_count_bitmask) + self.P + 1

                for idx in range(0, copy_count):
                    c = self.buffer[(buffer_start + idx) & buffer_bitmask]
                    self.outfile.write(bytes((c,)))
                    self.buffer[r] = c
                    r = (r + 1) & buffer_bitmask


def encode(*args, **kwargs):
    encoder = LZSSEncoder(*args, **kwargs)
    return encoder.encode()


def decode(*args, **kwargs):
    decoder = LZSSDecoder(*args, **kwargs)
    return decoder.decode()
