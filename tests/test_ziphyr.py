#!/usr/bin/env python

"""Tests for `ziphyr.ziphyr` module."""

import tempfile
import unittest
from filecmp import cmp
from unittest.mock import patch
from zipfile import ZipFile

import ziphyr.ziphyr as module
from ziphyr.retro import RetroZipFile
from ziphyr.utils import file_iterable


class TestZiphyr(unittest.TestCase):
    def test__init__(self):
        """Test Ziphyr object init."""
        _password = b'password'

        z = module.Ziphyr(_password)

        self.assertEqual(z.password, _password)
        self.assertEqual(z.stream, None)
        self.assertEqual(z.stream, None)

    @patch('platform.sys.version_info', autospec=True)
    def test_35_behavior(self, m_version_info):
        """ """
        m_version_info.minor = 7

        z = module.Ziphyr(b'')

        self.assertTrue(
            issubclass(z.ZipFile, ZipFile),
            msg="Ziphyr.ZipFile is not a subclass of ZipFile",
        )

        m_version_info.minor = 5

        z = module.Ziphyr(b'')

        self.assertTrue(
            issubclass(z.ZipFile, RetroZipFile),
            msg="Ziphyr.ZipFile is not a subclass of RetroZipFile",
        )

    def test_from_metadata(self):
        """Test Ziphyr.zinfo set-up from metadata."""
        _filename = "Animal Farm"
        _filesize = 1984

        z = module.Ziphyr(b'password')
        z.from_metadata(_filename, _filesize)

        self.assertEqual(z.zinfo.orig_filename, _filename)
        self.assertEqual(z.zinfo.filename, _filename)
        self.assertEqual(z.zinfo.file_size, _filesize)
        self.assertEqual(z.zinfo.external_attr, 25165824)

    def test_generator(self):
        """Test Ziphyr object's generator consumption."""
        z = module.Ziphyr(b'password')
        z.from_metadata("h2g2", 42)
        zg = z.generator(list())

        self.assertEqual(next(zg)[:4], b'PK\x03\x04')

    def test_zip_unzip(self):
        """Test zipping with Ziphyr then unzipping with zipfile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_fp = tmpdir+'/test.file'
            test_zp = tmpdir+'/test.zip'
            password = b'laughing'

            with open(test_fp, 'w') as f:
                f.write(
                    "I thought what I'd do was, I'd pretend I was one "
                    "of those deaf-mutes. That way I wouldn't have to "
                    "have any goddam stupid useless conversations with "
                    "anybody."
                )

            z = module.Ziphyr(password)
            z.from_filepath(test_fp)
            source = file_iterable(test_fp)

            with open(test_zp, 'ab') as f:
                for chunk in z.generator(source):
                    f.write(chunk)

            with ZipFile(test_zp, 'r') as f:
                f.setpassword(password)
                test_rp = f.extract(test_fp[1:], tmpdir)

            self.assertTrue(cmp(test_fp, test_rp))
