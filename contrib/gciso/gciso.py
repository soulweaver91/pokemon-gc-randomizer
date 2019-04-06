import struct
from collections import OrderedDict as odict

from .isofilewrapper import IsoInternalFileWrapper
from .bannerfile import BannerFile
from .dolfile import DolFile

class IsoFile(object):
    """
    The central class representing an .iso file.
    For information about many of it's attributes, see here: http://hitmen.c02.at/files/yagcd/yagcd/chap13.html#sec13

    Parameters
    ----------
    isoPath : str
        The path to the iso file.

    Attributes
    ----------
    gameCode : bytes
    makerCode: bytes
    diskId : int
    version : int
    gameName : bytes
    dolOffset : int
        Offset to the main executable DOL ("start.dol")
    dolSize : int
        Size of the main executable DOL ("start.dol")
    fstOffset : int
        Offset to the file system table
    fstSize : int
        Size of the file system table
    maxFstSize : int
        Maximum size of the file system table (relevant for games with multiple disks)
    apploaderDate : bytes
        Date (version) of the apploader (ASCII).
    apploaderEntryPoint: int
    apploaderCodeSize: int
    apploaderTrailerSize : int
    numFstEntries : int
        The number of file system table entries (files and directories)
    stringTableOffset : int
        The offset to the FST string table
    files : OrderedDict
        A dictionary with keys being paths to all files in the .iso and values being tuples of the form `(offset, size)` (offset and size of the file). See Notes for added system files!

    Notes
    -----
    A couple of files are added to the files attribute, that are not listed in the FST:

    - *boot.bin* - The header of the .iso file
    - *bi2.bin* - More disk information (containing dol/FST offsets etc.)
    - *fst.bin* - The file system table
    - *start.dol* - The main executable DOL. See :class:`DolFile` and :meth:`getDolFile`

    :class:`IsoFile` may also be used as a context manager::

        with IsoFile("melee.iso") as isoFile:
            data = isoFile.readFile("opening.bnr", 0)
            with isoFile.open("opening.bnr") as bnrFile:
                print(bnrFile.read())

    Also all files that take a file path may raise :class:`TypeError`, if the given path is not of type `bytes`.

    """

    _FST_ENTRY_LENGTH = 0xC

    def __init__(self, isoPath):
        self.file = open(isoPath, "r+b")
        self.files = odict()
        self._readDiskHeader()
        self._readFst()

    # http://hitmen.c02.at/files/yagcd/yagcd/chap13.html#sec13
    def _readDiskHeader(self):
        self.file.seek(0)
        values = struct.unpack(">4s2sBB", self.file.read(8))
        self.gameCode = values[0]
        self.makerCode = values[1]
        self.diskId = values[2]
        self.version = values[3]
        self.gameName = self._readString(0x20)

        self.file.seek(0x420)
        values = struct.unpack(">IIII", self.file.read(16))
        self.dolOffset = values[0]
        self.fstOffset = values[1]
        self.fstSize = values[2]
        self.maxFstSize = values[3] # relevant for multiple disks
        self.dolSize = self.fstOffset - self.dolOffset

        self.files[b"boot.bin"] = (0x0, 0x440, None)
        self.files[b"bi2.bin"] = (0x440, 0x2000, None)
        self.files[b"fst.bin"] = (self.fstOffset, self.fstSize, None)
        self.files[b"start.dol"] = (self.dolOffset, self.dolSize, None)

        self.appLoaderOffset = 0x2440
        # I am unsure about this whole part
        self.file.seek(self.appLoaderOffset)
        values = struct.unpack(">10s6xIII", self.file.read(28))
        self.apploaderDate = values[0]
        self.apploaderEntryPoint = values[1]
        self.apploaderCodeSize = values[2]
        self.apploaderTrailerSize = values[3]
        self.appLoaderCodeOffset = self.appLoaderOffset + 0x20

        self.files[b"appldr.bin"] = (self.appLoaderCodeOffset, self.apploaderCodeSize, None)


    def _readFst(self):
        self.file.seek(self.fstOffset + 0x8)
        # length of root entry
        self.numFstEntries = struct.unpack(">I", self.file.read(4))[0]
        self.stringTableOffset = self.fstOffset + (self.numFstEntries * IsoFile._FST_ENTRY_LENGTH)

        self._readDirectory(b"", 0)

    # https://github.com/CraftedCart/GCISOManager cleared a lot of things up
    def _readDirectory(self, path, index):
        self.file.seek(self.fstOffset + IsoFile._FST_ENTRY_LENGTH * index)
        isDir = self.file.read(1)[0]
        fileNameOffset = struct.unpack(">I", b"\0" + self.file.read(3))[0]
        offset = struct.unpack(">I", self.file.read(4))[0]
        length = struct.unpack(">I", self.file.read(4))[0]
        name = b"" if index == 0 else self._readString(self.stringTableOffset + fileNameOffset)

        if isDir:
            i = index + 1

            while i < length:
                i += self._readDirectory(path + name + b"/", i)

            return length - index
        else:
            filePath = path + name
            if filePath[0] == b"/"[0]: filePath = filePath[1:]
            self.files[filePath] = (offset, length, index)
            return 1

    def _readString(self, offset):
        self.file.seek(offset)
        s = b""
        while True:
            byte = self.file.read(1)
            if byte == b"\0":
                break
            else:
                s += byte
        return s

    def close(self):
        """
        Closes the file
        """
        self.file.close()

    @staticmethod
    def _checkPath(path):
        if not isinstance(path, bytes):
            raise TypeError("Path must be bytes!")

    def _writeFile(self, fileOffset, fileSize, offset, data):
        if offset < 0:
            raise IndexError("Offset must be > 0!")
        if offset >= fileSize:
            raise IndexError("Offset is out of file bounds!")
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes!")
        if offset + len(data) > fileSize:
            raise ValueError("Cannot change file size!")
        self.file.seek(fileOffset + offset)
        return self.file.write(data)

    def writeFile(self, path, offset, data):
        """
        Writes `data` to the file with path `path` inside the .iso at offset `offset`.

        Parameters
        ----------
        path : bytes
        offset : int
        data : bytes

        Returns
        -------
        int
            The number of bytes written

        Raises
        ------
        IndexError
            If `offset` is negative or greater than the file size.
        TypeError
            If `path` or `data` is not `bytes`
        ValueError
            If the write would go past the end of the file, since it cannot change size.
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        return self._writeFile(fileOffset, fileSize, offset, data)

    def _readFile(self, fileOffset, fileSize, offset=0, count=-1):
        if offset < 0:
            raise IndexError("Offset must be > 0!")
        if offset >= fileSize:
            raise IndexError("Offset is out of file bounds!")
        if count == None or count < 0:
            count = fileSize - offset
        if offset + count > fileSize:
            raise ValueError("Cannot read beyond end of file!")
        self.file.seek(fileOffset + offset)
        return self.file.read(count)

    def readFile(self, path, offset, count=-1):
        """
        Reads `count` bytes from `offset` inside the file with path `path`

        Parameters
        ----------
        path : bytes
        offset : int
        count : int
            If count is negative, none or omitted, read until end of file

        Returns
        -------
        bytes
            The data read

        Raises
        ------
        IndexError
            If `offset` is negative or greater than the file size.
        ValueError
            If the read would go past the end of the file.
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        return self._readFile(fileOffset, fileSize, offset, count)

    def resizeFile(self, path, new_size):
        # TODO: This will invalidate any ISOFileWrappers!
        # Reading and writing operations will operate on an unallocated area if the wrapper is not recreated afterwards.

        if path not in self.files:
            raise KeyError('Cannot resize a file that does not exist!')

        fileOffset, fileSize, fileIndex = self.files[path]

        if fileSize == new_size:
            return
        if fileSize < new_size:
            self._relocateFile(path, new_size)
        if fileSize > new_size:
            # Blank truncated data
            self.file.seek(fileOffset + new_size)
            self.file.write(b'\x00' * (fileSize - new_size))

            # Update file header data in ISO
            self.file.seek(self.fstOffset + IsoFile._FST_ENTRY_LENGTH * fileIndex + 8)
            self.file.write(struct.pack(">I", new_size))

            # Update file pointer in memory
            self.files[path] = (fileOffset, new_size, fileIndex)

    def _relocateFile(self, path, bytes_required):
        if path not in self.files:
            raise KeyError('Cannot relocate a file that does not exist!')

        fileEntry = self.files[path]

        # Go through files until a gap of the required length is found
        last_free_offset = None
        for n, f in sorted(self.files.items(), key=lambda x: x[1][0]):
            if f[2] is not None and last_free_offset is not None and last_free_offset + bytes_required < f[0]:
                print('%d bytes free before %s (%d-%d)' % (f[0] - (last_free_offset + bytes_required), n, last_free_offset + bytes_required, f[0]))
                break

            last_free_offset = f[0] + f[1]

        # Copy data
        old_data = self.readFile(path, 0)
        self.file.seek(last_free_offset)
        self.file.write(old_data)

        # Blank out old data
        self.file.seek(fileEntry[0])
        self.file.write(b'\x00' * fileEntry[1])

        # Update file header data in ISO
        self.file.seek(self.fstOffset + IsoFile._FST_ENTRY_LENGTH * fileEntry[2] + 4)
        self.file.write(struct.pack(">I", last_free_offset))
        self.file.write(struct.pack(">I", bytes_required))

        # Update file pointer in memory
        self.files[path] = (last_free_offset, bytes_required, fileEntry[2])


    @staticmethod
    def _normalizeDirPath(path):
        if len(path) > 0: # empty path = root => can stay empty
            if path[-1] != b"/"[0]: path += b"/" # add training slash
            if path[0] == b"/"[0]: path = path[1:] # remove leading slash
        return path

    @staticmethod
    def fileInDir(filePath, dirPath):
        """
        Parameters
        ----------
        filePath : bytes
        dirPath : bytes

        Returns
        -------
        bool
            Whether the file `filePath` is inside the directory `dirPath`
        """
        IsoFile._checkPath(filePath)
        IsoFile._checkPath(dirPath)
        dirPath = IsoFile._normalizeDirPath(dirPath)
        if dirPath == "": return True
        return filePath.startswith(dirPath)

    def listDir(self, path):
        """
        Lists all files in a directory (including files in subdirectories, not including other directories).

        Parameters
        ----------
        path : bytes

        Yields
        ------
        bytes
            Filenames of the files in the directory. Relative to the directory being listed.
        """
        IsoFile._checkPath(path)
        path = IsoFile._normalizeDirPath(path)
        for file in self.files:
            if IsoFile.fileInDir(file, path):
                yield file[len(path):]

    def isFile(self, path):
        """
        Parameters
        ----------
        path : bytes

        Returns
        -------
        bool
            Whether the given path belongs to a file that exists inside the .iso.
        """
        IsoFile._checkPath(path)
        return path in self.files

    def isDir(self, path):
        """
        Parameters
        ----------
        path : bytes

        Returns
        -------
        bool
            Whether the given path belongs to a directory that exists inside the .iso and contains files.
        """
        IsoFile._checkPath(path)
        return any(IsoFile.fileInDir(file, path) for file in self.files.keys())

    def open(self, path):
        """
        Parameters
        ----------
        path : bytes

        Returns
        -------
        :class:`IsoInternalFileWrapper`
            A wrapper of the given file.

        Notes
        -----
        See the notes of :class:`IsoFile` and :class:`IsoInternalFileWrapper` for examples.
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        return IsoInternalFileWrapper(self, fileOffset, fileSize)

    def fileOffset(self, path):
        """
        Parameters
        ----------
        path : bytes

        Returns
        -------
        int
            The offset of the file with the given path inside the .iso file.
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        return fileOffset

    def fileSize(self, path):
        """
        Parameters
        ----------
        path : bytes

        Returns
        -------
        bool
            The size of the file with the given path inside the .iso file.
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        return fileSize

    def getBannerFile(self, path):
        """
        Creates a :class:`BannerFile` from the file with the given `path`

        Parameters
        ----------
        path : bytes

        Returns
        -------
        :class:`BannerFile`
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        self.file.seek(fileOffset)
        return BannerFile(self.file.read(fileSize))

    def getDolFile(self, path=b"start.dol"):
        """
        Creates a :class:`DolFile` from the file with the given `path`

        Parameters
        ----------
        path : bytes
            If no path is given, the main executable DOL `start.dol` is used.

        Returns
        -------
        :class:`DolFile`
        """
        IsoFile._checkPath(path)
        fileOffset, fileSize, fileIndex = self.files[path]
        self.file.seek(fileOffset)
        return DolFile(self.file.read(fileSize))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()
