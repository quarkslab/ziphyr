""" Functions provided for retro-portability to python3.5 """

import io
import os
import stat
import struct
from zipfile import (
    ZIP64_LIMIT, ZIP_LZMA, ZIP_STORED,
    ZipFile, ZipInfo, _get_compressor, crc32,
)


_DD_SIGNATURE = 0x08074b50


def retro_from_file(filepath):
    """ Faking write-oriented zinfo creation """
    st = os.stat(filepath)
    isdir = stat.S_ISDIR(st.st_mode)
    arcname = os.path.normpath(os.path.splitdrive(filepath)[1])
    while arcname[0] in (os.sep, os.altsep):
        arcname = arcname[1:]
    if isdir:
        arcname += '/'
    return arcname, st.st_size


class RetroZipInfo(ZipInfo):
    """
    Custom ZipInfo to provide a fake from_file to py35
    """

    @classmethod
    def from_file(cls, filepath):
        """Hack to handle the lack of from_file in py35"""
        try:
            return super().from_file(filepath)
        except AttributeError:
            zinfo = cls(filename=filepath)

            arcname, st_size = retro_from_file(filepath)
            zinfo.orig_filename = arcname
            zinfo.filename = arcname
            zinfo.file_size = st_size

            return zinfo


class _ZipWriteFile(io.BufferedIOBase):
    """ taken from python3.6 readapted for python3.5 """
    def __init__(self, zf, zinfo, zip64):
        self._zinfo = zinfo
        self._zip64 = zip64
        self._zipfile = zf
        self._compressor = _get_compressor(zinfo.compress_type)
        self._file_size = 0
        self._compress_size = 0
        self._crc = 0

    @property
    def _fileobj(self):
        return self._zipfile.fp

    def writable(self):
        return True

    def write(self, data):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        nbytes = len(data)
        self._file_size += nbytes
        self._crc = crc32(data, self._crc)
        if self._compressor:
            data = self._compressor.compress(data)
            self._compress_size += len(data)
        self._fileobj.write(data)
        return nbytes

    def close(self):
        if self.closed:
            return
        try:
            super().close()
            # Flush any data from the compressor, and update header info
            if self._compressor:
                buf = self._compressor.flush()
                self._compress_size += len(buf)
                self._fileobj.write(buf)
                self._zinfo.compress_size = self._compress_size
            else:
                self._zinfo.compress_size = self._file_size
            self._zinfo.CRC = self._crc
            self._zinfo.file_size = self._file_size

            # Write updated header info
            if self._zinfo.flag_bits & 0x08:
                # Write CRC and file sizes after the file data
                fmt = '<LLQQ' if self._zip64 else '<LLLL'
                self._fileobj.write(struct.pack(
                    fmt, _DD_SIGNATURE, self._zinfo.CRC,
                    self._zinfo.compress_size, self._zinfo.file_size)
                )
                self._zipfile.start_dir = self._fileobj.tell()
            else:
                if not self._zip64:
                    if self._file_size > ZIP64_LIMIT:
                        raise RuntimeError(
                            'File size unexpectedly exceeded ZIP64 limit')
                    if self._compress_size > ZIP64_LIMIT:
                        raise RuntimeError(
                            'Compressed size unexpectedly exceeded ZIP64 limit'
                        )
                # Seek backwards and write file header (which will now include
                # correct CRC and file sizes)

                # Preserve current position in file
                self._zipfile.start_dir = self._fileobj.tell()
                self._fileobj.seek(self._zinfo.header_offset)
                self._fileobj.write(self._zinfo.FileHeader(self._zip64))
                self._fileobj.seek(self._zipfile.start_dir)

            # Successfully written: Add file to our caches
            self._zipfile.filelist.append(self._zinfo)
            self._zipfile.NameToInfo[self._zinfo.filename] = self._zinfo
        finally:
            self._zipfile._writing = False


class RetroZipFile(ZipFile):
    """ taken from python3.6 readapted for python3.5 """
    def __init__(
        self, file, mode="r", compression=ZIP_STORED, allowZip64=True
    ):
        self._writing = False
        super().__init__(
            file=file, mode=mode, compression=compression,
            allowZip64=allowZip64
        )

    def _open_to_write(self, zinfo, force_zip64=False):
        if force_zip64 and not self._allowZip64:
            raise ValueError(
                "force_zip64 is True, but allowZip64 was False when opening "
                "the ZIP file."
            )
        if self._writing:
            raise ValueError("Can't write to the ZIP file while there is "
                             "another write handle open on it. "
                             "Close the first handle before opening another.")

        # Size and CRC are overwritten with correct data
        # after processing the file
        zinfo.compress_size = 0
        zinfo.CRC = 0

        zinfo.flag_bits = 0x00
        if zinfo.compress_type == ZIP_LZMA:
            # Compressed data includes an end-of-stream (EOS) marker
            zinfo.flag_bits |= 0x02
        if not self._seekable:
            zinfo.flag_bits |= 0x08

        if not zinfo.external_attr:
            zinfo.external_attr = 0o600 << 16  # permissions: ?rw-------

        # Compressed size can be larger than uncompressed size
        zip64 = self._allowZip64 and \
            (force_zip64 or zinfo.file_size * 1.05 > ZIP64_LIMIT)

        if self._seekable:
            self.fp.seek(self.start_dir)
        zinfo.header_offset = self.fp.tell()

        self._writecheck(zinfo)
        self._didModify = True

        self.fp.write(zinfo.FileHeader(zip64))

        self._writing = True
        return _ZipWriteFile(self, zinfo, zip64)

    def open(self, name, mode='r', pwd=None, *, force_zip64=False):
        if mode != 'w':
            return super().open(name=name, mode='r', pwd=None)
        if pwd and not isinstance(pwd, bytes):
            raise TypeError("pwd: expected bytes, got %s" % type(pwd).__name__)
        if not self.fp:
            raise ValueError(
                "Attempt to use ZIP archive that was already closed")

        # Make sure we have an info object
        if isinstance(name, ZipInfo):
            # 'name' is already an info object
            zinfo = name
        elif mode == 'w':
            zinfo = ZipInfo(name)
            zinfo.compress_type = self.compression
            zinfo._compresslevel = self.compresslevel
        else:
            # Get info object for name
            zinfo = self.getinfo(name)

        return self._open_to_write(zinfo, force_zip64=force_zip64)
