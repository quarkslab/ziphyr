#!/usr/bin/env python

"""Tests for `ziphyr.retro` module."""

import unittest
from unittest.mock import patch

import ziphyr.retro as module


class TestRetro(unittest.TestCase):
    @patch('stat.S_ISDIR', autospec=True)
    @patch('os.stat', autospec=True)
    def test_retro_from_file(self, m_os_stat, m_stat_ISDIR):
        """Testing the fake .from_file() retro-port."""
        m_os_stat.return_value.st_size = 1
        m_stat_ISDIR.return_value = False

        arcname, size = module.retro_from_file('/tmp/tmp.tmp')

        self.assertEqual(arcname, 'tmp/tmp.tmp')
        self.assertEqual(size, 1)

        m_stat_ISDIR.return_value = True

        arcname, size = module.retro_from_file('/tmp/tmp.tmp')

        self.assertEqual(arcname, 'tmp/tmp.tmp/')
        self.assertEqual(size, 1)
