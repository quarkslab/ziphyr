"""Main Ziphyr module."""

import platform
import struct
from os import urandom
from zipfile import ZIP_STORED, ZipFile, crc32

from ziphyr.retro import RetroZipFile, RetroZipInfo
from ziphyr.stream import ZiphyrStream


class PKCryptoZipInfo(RetroZipInfo):
    """
    Custom ZipInfo to inject the zipcrypto flag through ZipFile.open()
    when _open_to_write writes down ZipInfo.FileHeader.
    """

    def FileHeader(self, zip64=None):  # noqa
        """Flips the PKCrypto flag in ZipInfo FileHeader"""
        self.flag_bits |= 0x01
        return super().FileHeader(zip64)


class Ziphyr():
    """
    Ziphyr object, initiated with or without password.
    Requires priming with the target file (path or metadata).
    Provides then a generator to be consumed for zipcrypted archive.
    """

    def __init__(self, password: bytes = None):
        """
        Optional bytes-type password parameter.
        Initializes internals at None.
        """
        self.password = password
        self.stream = None
        self.zinfo = None

        if self.password:
            self.ZipInfo = PKCryptoZipInfo
        else:
            self.ZipInfo = RetroZipInfo

        if platform.sys.version_info.minor < 6:
            self.ZipFile = RetroZipFile
        else:
            self.ZipFile = ZipFile

    def from_metadata(self, filename, filesize, ext_attr=25165824):
        """
        Primes Ziphyr for a target using provided filename and filesize.
        Default external_attr produced by python is 0o600.
        """
        self.zinfo = self.ZipInfo.from_file('/dev/null')
        self.zinfo.orig_filename = filename
        self.zinfo.filename = filename
        self.zinfo.file_size = filesize
        self.zinfo.external_attr = ext_attr

    def from_filepath(self, filepath, ext_attr=25165824):
        """
        Primes Ziphyr for a target using its filepath.
        Default external_attr produced by python is 0o600.
        """
        self.zinfo = self.ZipInfo.from_file(filepath)
        self.zinfo.external_attr = ext_attr

    def generator(self, source, compression=ZIP_STORED):
        """
        Turn a streamed file source into a stream zipcrypted archive file.
        Some lines are based upon Ivan Ergunov's work.
        Some lines are based upon devthat's work on zipencrypt.
        """
        if not self.zinfo:
            raise RuntimeError(
                "Ziphyr object not primed. "
                "Please use either from_filepath() or from_metadata()."
            )

        self.stream = ZiphyrStream(self.password)

        with self.ZipFile(
            self.stream, mode='w', compression=compression
        ) as zfile:
            clear_crc = 0
            with zfile.open(self.zinfo, mode='w') as dest:
                if self.password:
                    # the zipcrypto asks for twelve almost-random bytes
                    self.zinfo._raw_time = (
                        self.zinfo.date_time[3] << 11
                        | self.zinfo.date_time[4] << 5
                        | (self.zinfo.date_time[5] // 2))
                    check_byte = (self.zinfo._raw_time >> 8) & 0xff
                    twelve_angry = urandom(11) + struct.pack("B", check_byte)
                    dest.write(self.stream.cypher_chunk(twelve_angry))

                for chunk in source:
                    # the internal crc is updated when dest.write()
                    # but we want it to be of the clear data
                    # hence doing our own in parallel
                    clear_crc = crc32(chunk, clear_crc)
                    if self.password:
                        chunk = self.stream.cypher_chunk(chunk)
                    dest.write(chunk)
                    yield self.stream.get()

            if self.password:
                self.zinfo.file_size -= 12  # withdrawing the 12 bytes
            self.zinfo.CRC = clear_crc  # overwriting with the clearbytes crc

        yield self.stream.get()
