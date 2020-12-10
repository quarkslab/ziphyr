"""Main Ziphyr module."""

import platform
import struct
from os import urandom
from zipfile import ZIP_STORED, ZipFile, ZipInfo, crc32

from ziphyr.retro import RetroZipFile, retro_from_file
from ziphyr.stream import ZiphyrStream


class PKCryptoZipInfo(ZipInfo):
    """
    Custom ZipInfo to inject the zipcrypto flag through ZipFile.open()
    when _open_to_write writes down ZipInfo.FileHeader,
    and to provide a fake from_file to py35
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

    def FileHeader(self, zip64=None):  # noqa
        """Flips the PKCrypto flag in ZipInfo FileHeader"""
        self.flag_bits |= 0x01
        return super().FileHeader(zip64)


class Ziphyr():
    """
    Ziphyr object, initiated with password.
    Requires priming with the target file (path or metadata).
    Provides then a generator to be consumed for zipcrypted archive.
    """

    def __init__(self, password: bytes):
        """
        Requires a bytes-type password parameter.
        Initializes internals at None.
        """
        self.password = password
        self.stream = None
        self.zinfo = None

        if platform.sys.version_info.minor < 6:
            self.ZipFile = RetroZipFile
        else:
            self.ZipFile = ZipFile

    def from_metadata(self, filename, filesize, ext_attr=25165824):
        """
        Primes Ziphyr for a target using provided filename and filesize.
        Default external_attr produced by python is 0o600.
        """
        self.zinfo = PKCryptoZipInfo.from_file('/dev/null')
        self.zinfo.orig_filename = filename
        self.zinfo.filename = filename
        self.zinfo.file_size = filesize
        self.zinfo.external_attr = ext_attr

    def from_filepath(self, filepath, ext_attr=25165824):
        """
        Primes Ziphyr for a target using its filepath.
        Default external_attr produced by python is 0o600.
        """
        self.zinfo = PKCryptoZipInfo.from_file(filepath)
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
                # the zipcrypto asks for twelve almost-random bytes
                self.zinfo._raw_time = (
                    self.zinfo.date_time[3] << 11
                    | self.zinfo.date_time[4] << 5
                    | (self.zinfo.date_time[5] // 2))
                check_byte = (self.zinfo._raw_time >> 8) & 0xff
                twelve_angry_bytes = urandom(11) + struct.pack("B", check_byte)
                dest.write(self.stream.cypher_chunk(twelve_angry_bytes))

                for chunk in source:
                    # the internal crc is updated when dest.write()
                    # but we want it to be of the clear data
                    # hence doing our own in parallel
                    clear_crc = crc32(chunk, clear_crc)
                    dest.write(self.stream.cypher_chunk(chunk))
                    yield self.stream.get()

            self.zinfo.file_size -= 12  # withdrawing the mandatory 12 bytes
            self.zinfo.CRC = clear_crc  # overwriting with the clearbytes crc

        yield self.stream.get()
