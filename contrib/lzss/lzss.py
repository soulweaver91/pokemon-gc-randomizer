"""
Based on the unfit implementation from https://gist.github.com/nucular/258d544bbd1ba401232ae83a11bd8857
with default values also changed for the purposes of this project.

Original C implementation by Okumura Haruhiko (public domain)
"""

import logging

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

    # TODO: this is slooooooooooooooooooow.
    # I had adapted the LZSS encoder from QuickBMS previously, but it didn't seem to work (the ROM crashed on boot), so
    # I threw the implementation away before the first commit in the repository. Later it was apparent that the problem
    # was likely the incorrect data alignment and not the encoding process; it would probably be worth it to try that
    # approach again.
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
        s = 0

        while encode_head < buffer_end:
            max_match_len = min(F2 + 1, buffer_end - encode_head + 1)
            match_start = 0
            match_len = 1

            c = self.buffer[encode_head]
            for i in range(encode_head - 1, s - 1, -1):
                if self.buffer[i] == c:
                    for j in range(1, max_match_len):
                        if self.buffer[i + j] != self.buffer[encode_head + j]:
                            break

                    if j > match_len:
                        match_start = i
                        match_len = j

                        if j >= max_match_len:
                            break

            if match_len <= self.P:
                match_len = 1
                self.store_literal(c)
            else:
                self.store_reference(match_start & (self.N - 1), match_len)

            encode_head += match_len
            s += match_len
            if encode_head >= self.N * 2 - F2:
                logging.debug('  %.2fkB encoded in %.2fkB', self.textcount / 1024, self.outfile.tell() / 1024)

                # Mirror the upper buffer half to the bottom
                self.buffer[0:self.N - 1] = self.buffer[self.N:self.N * 2 - 1]

                # Move to the end of the bottom buffer
                buffer_end -= self.N
                encode_head -= self.N
                s -= self.N

                # Read data to the upper buffer
                while buffer_end < self.N * 2 - self.P:
                    buffer_end += 1

                    z = self.infile.read(1)
                    if len(z) == 0:
                        break

                    self.textcount += 1
                    self.buffer[buffer_end] = z[0]

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
