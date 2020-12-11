"""ZiphyrStream's module."""

from io import RawIOBase


def _gen_crc(crc):

    """
    cpython zipfile/_gen_crc from python3.7.
    copy-pasted for retro-compatibility.
    """
    for j in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ 0xEDB88320
        else:
            crc >>= 1
    return crc


class ZiphyrStream(RawIOBase):

    """
    A zipcrypto encrypted unseekable stream.
    Disclaimer: zipcrypto is known to be flawed.
    Adapted from Ivan Ergunov zipfile_generator.
    """
    def __init__(self, password: bytes = None):
        """
        Optional bytes-type password parameter.
        If provided, initialize the crctable and keys for zipcrypto.
        """
        self._buffer = b''

        if password:
            self.crctable = list(map(_gen_crc, range(256)))

            self.x = 305419896  # PKZIP Key(0)
            self.y = 591751049  # PKZIP Key(1)
            self.z = 878082192  # PKZIP Key(2)

            for p in password:
                self.update_keys(p)

    def crc32(self, ch, crc):
        """
        Compute the CRC32 primitive on one byte.
        From cpython zipfile.
        """
        return (crc >> 8) ^ self.crctable[(crc ^ ch) & 0xFF]

    def update_keys(self, c):
        """
        zipcrypto keys cycling.
        Adapted from cpython zipfile _ZipDecrypter.
        """
        self.x = self.crc32(c, self.x)
        self.y = (self.y + (self.x & 0xFF)) & 0xFFFFFFFF
        self.y = (self.y * 134775813 + 1) & 0xFFFFFFFF
        self.z = self.crc32((self.y >> 24) & 0xFF, self.z)

    def cypher(self, c):
        """
        zipcrypto byte cyphering.
        Adapted from devthat/zipencrypt _ZipEncrypter.
        """
        k = self.z | 2
        _c = c ^ ((k * (k ^ 1)) >> 8) & 0xFF
        self.update_keys(c)
        return _c

    def writable(self):
        return True

    def write(self, b):
        if self.closed:
            raise ValueError('Stream was closed!')
        self._buffer += b
        return len(b)

    def get(self):
        chunk = self._buffer
        self._buffer = b''
        return chunk

    def cypher_chunk(self, chunk):
        """
        Cyphering a whole chunk.
        Adapted from devthat/zipencrypt _ZipWriteFile.
        """
        tfx = lambda x: bytes(map(self.cypher, x))  # noqa
        return tfx(chunk)
