#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from io import BytesIO
from struct import unpack, pack

import os

from contrib.lzss import decode, encode
from randomizer import config


class FsysFile:
    def __init__(self, fname, header, data, duplicate_counter=0, fsys_name=None):
        logging.debug('Starting decoding file %s contained in fsys archive%s into memory.',
                      fname.decode('ascii', errors='replace'),
                      ' ' + fsys_name.decode('ascii', errors='replace') if fsys_name else '')
        self.fname = fname
        self.header = header
        self._original_encoded_data = data
        self._data = BytesIO()
        self.accessed = False
        self.duplicate_counter = duplicate_counter

        decode(BytesIO(data[16:]), outfile=self._data)
        length = self._data.tell()

        if length == self.header.data_size:
            logging.debug('Successfully decoded %d bytes from the compressed stream.', length)

        else:
            logging.warning('Decoded %d bytes from the compressed stream, but expected %d bytes!',
                            length, self.header.data_size)

        if config.dump_files:
            dump_path = os.path.join(config.working_dir, 'dump',
                                     self.fname if not fsys_name else '%s__%s%s' % (
                                         fsys_name.decode('ascii', errors='replace'),
                                         self.fname.decode('ascii', errors='replace'),
                                         '' if self.duplicate_counter == 0 else '__' + str(self.duplicate_counter)))
            try:
                with open(dump_path, 'wb') as f:
                    f.write(self._data.getvalue())
            except IOError:
                logging.warning('Couldn\'t dump the file %s, skipping dumping.', dump_path)

    def encode(self):
        if not self.accessed:
            logging.debug('  %s was not accessed, returning the original compressed data.',
                          self.fname.decode('ascii', errors='replace'))
            return self.header, self._original_encoded_data

        logging.debug('  Compressing %s.', self.fname.decode('ascii', errors='replace'))
        self._data.seek(0)
        output = BytesIO()
        encode(self._data, outfile=output)

        self.header.data_size = self._data.tell()
        self.header.data_size_compressed = len(output.getvalue()) + 16

        return self.header, (
                pack(
                    '>4sIII',
                    b'LZSS',
                    self.header.data_size,
                    self.header.data_size_compressed,
                    0
                ) +
                output.getvalue()
        )

    def _invalidate_original_data(self):
        if not self.accessed:
            self.accessed = True
            del self._original_encoded_data

    @property
    def data(self):
        self._invalidate_original_data()
        return self._data

    @data.setter
    def data(self, value):
        self._invalidate_original_data()
        self._data = value


class FsysHeader1:
    SIGNATURE = '>4s4s4sI8sIII'

    def __init__(self, header_data):
        values = unpack(self.SIGNATURE, header_data)

        if values[0] != b"FSYS":
            raise TypeError('Not a valid FSYS header')

        (
            self.magic,
            self.unknown_1,
            self.identifier,
            self.file_count,
            self.unknown_2,
            self.header2_offset,
            self.data_offset,
            self.data_length
        ) = values

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.magic,
            self.unknown_1,
            self.identifier,
            self.file_count,
            self.unknown_2,
            self.header2_offset,
            self.data_offset,
            self.data_length
        )


class FsysHeader2:
    SIGNATURE = '>III'

    def __init__(self, header_data):
        (
            self.file_header_table_offset,
            self.file_name_table_offset,
            self.data_offset
        ) = unpack(self.SIGNATURE, header_data)

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.file_header_table_offset,
            self.file_name_table_offset,
            self.data_offset
        )


class FsysFileHeader:
    SIGNATURE = '>4sIIc7sI12sI4sI'

    def __init__(self, header_data):
        (
            self.unknown_1,
            self.data_start,
            self.data_size,
            self.unknown_flag,
            self.unknown_2,
            self.data_size_compressed,
            self.unknown_3,
            self.name_pointer_1,
            self.unknown_4,
            self.name_pointer_2
        ) = unpack(self.SIGNATURE, header_data)

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.unknown_1,
            self.data_start,
            self.data_size,
            self.unknown_flag,
            self.unknown_2,
            self.data_size_compressed,
            self.unknown_3,
            self.name_pointer_1,
            self.unknown_4,
            self.name_pointer_2
        )


class FsysArchive:
    def __init__(self, data, name):
        self.name = name
        self.header = None
        self.header2 = None
        self.files = []
        self.file_indices = {}

        header = self.header = FsysHeader1(data.read(36))

        logging.debug('FSYS has %d files', header.file_count)
        logging.debug('Header 1 length: %d bytes + %d bytes padding', data.tell(), header.header2_offset - data.tell())
        logging.debug('FSYS contains %d bytes of payload data.', header.data_length)

        # Read header 2
        data.seek(header.header2_offset)
        header2 = self.header2 = FsysHeader2(data.read(12))

        logging.debug('Header 1 length: %d bytes', data.tell() - header.header2_offset)

        if config.dump_files:
            dump_path = os.path.join(config.working_dir, 'dump', self.name.decode('ascii', errors='replace'))
            try:
                with open(dump_path, 'wb') as f:
                    f.write(data.getvalue())
            except IOError:
                logging.warning('Couldn\'t dump the file %s, skipping dumping.', dump_path)

        # Read files
        for file_idx in range(0, header.file_count):
            logging.debug('Reading file #%d...', file_idx + 1)

            data.seek(header2.file_header_table_offset + file_idx * 4)
            data.seek(unpack('>I', data.read(4))[0])

            file_header = FsysFileHeader(data.read(48))

            # Get file name
            name_pointer = file_header.name_pointer_1 or file_header.name_pointer_2 or None
            namebuf = bytearray(0)
            if name_pointer is not None:
                data.seek(name_pointer)

                while len(namebuf) < 512:
                    byte = data.read(1)
                    if byte == b'\x00':
                        break

                    namebuf.append(byte[0])

            duplicate_name_counter = 0
            if namebuf.hex() in self.file_indices:
                duplicate_name_counter = len(self.file_indices[namebuf.hex()])
            else:
                self.file_indices[namebuf.hex()] = []

            logging.debug('  File: %s', namebuf.decode('ascii', errors='replace'))
            logging.debug('  %d bytes compressed', file_header.data_size_compressed)
            logging.debug('  %d bytes uncompressed', file_header.data_size)

            data.seek(file_header.data_start)
            self.files.append(FsysFile(namebuf, file_header, data.read(file_header.data_size_compressed),
                                       duplicate_counter=duplicate_name_counter, fsys_name=name))
            self.file_indices[namebuf.hex()].append(len(self.files) - 1)

    def get_file(self, name, idx=0):
        file_idx = self.file_indices[name.hex()][idx]
        return self.files[file_idx]

    @staticmethod
    def from_iso(iso, name):
        logging.debug('Reading the FSYS file %s from the ISO.', name.decode('ascii', errors='replace'))
        return FsysArchive(BytesIO(iso.readFile(name, 0)), name)

    def encode(self):
        logging.debug('Starting to pack the FSYS %s.', self.name.decode('ascii', errors='replace'))
        encoded_fsys = BytesIO()

        # Encode files
        encoded_files = [(f.fname, *f.encode()) for f in self.files]
        for i, f in enumerate(encoded_files):
            # Alignment
            encoded_files[i] = (f[0], f[1], f[2] + b'\x00' * (32 - len(f[2]) % 16))

        # Build name header
        file_names = [f[0] + b'\x00' for f in encoded_files]
        name_header = b''.join(file_names)
        if len(name_header) % 16 != 0:
            # alignment
            name_header += b'\x00' * (16 - (len(name_header) % 16))

        # Calculate offsets
        header2_offset = 0x40
        file_header_table_offset = 0x60
        file_name_table_offset = file_header_table_offset + len(encoded_files) * 4 \
            + (12 - 4 * ((len(encoded_files) - 1) % 4))
        file_header_block_offset = file_name_table_offset + len(name_header)
        file_data_offset = file_header_block_offset + len(encoded_files) * 112 \
            + (file_header_block_offset + len(encoded_files) * 112) % 32
        end_magic_offset = ((file_data_offset + sum([len(f[2]) for f in encoded_files])) // 16) * 16 + 60
        end_offset = end_magic_offset + 4

        # Update headers
        self.header.header2_offset = header2_offset
        self.header.data_offset = file_data_offset
        self.header.data_length = end_offset

        self.header2.data_offset = file_data_offset
        self.header2.file_name_table_offset = file_name_table_offset
        self.header2.file_header_table_offset = file_header_table_offset

        name_table_inner_offset = 0
        data_inner_offset = 0
        for i, f in enumerate(encoded_files):
            f_header = f[1]

            f_header.data_start = file_data_offset + data_inner_offset
            f_header.name_pointer_1 = file_name_table_offset + name_table_inner_offset

            name_table_inner_offset += len(file_names[i])
            data_inner_offset += len(f[2])

        # Write main headers
        encoded_fsys.write(self.header.encode())
        encoded_fsys.write(b'\x00' * (header2_offset - encoded_fsys.tell()))
        encoded_fsys.write(self.header2.encode())
        encoded_fsys.write(b'\x00' * (file_header_table_offset - encoded_fsys.tell()))

        # Write file header offset table
        encoded_fsys.write(b''.join([pack('>I', file_header_block_offset + i * 112)
                                     for i in range(0, len(encoded_files))]))
        encoded_fsys.write(b'\x00' * (file_name_table_offset - encoded_fsys.tell()))

        # Write name table
        encoded_fsys.write(name_header)

        # Write file headers
        for f in encoded_files:
            encoded_fsys.write(f[1].encode())
            encoded_fsys.write(b'\x00' * 64)

        encoded_fsys.write(b'\x00' * (file_data_offset - encoded_fsys.tell()))

        # Write file data
        for f in encoded_files:
            encoded_fsys.write(f[2])

        # Write end padding & magic
        encoded_fsys.write(b'\x00' * (end_magic_offset - encoded_fsys.tell()))
        encoded_fsys.write(b'FSYS')

        if config.dump_files:
            dump_path = os.path.join(config.working_dir, 'dump',
                                     self.name.decode('ascii', errors='replace') + '.!modified')
            try:
                with open(dump_path, 'wb') as f:
                    f.write(encoded_fsys.getvalue())
            except IOError:
                logging.warning('Couldn\'t dump the file %s, skipping dumping.', dump_path)

        return encoded_fsys.getvalue()
