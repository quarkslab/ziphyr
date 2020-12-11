#!/usr/bin/env python

"""Tests for `ziphyr.stream` module."""

import unittest

import ziphyr.stream as module


class TestZiphyrStream(unittest.TestCase):
    def test_emptypassword(self):
        """Test stream consistent behavior with an empty password."""
        stream = module.ZiphyrStream(b'')

        self.assertTrue(stream.writable())
        self.assertFalse(stream.seekable())

        stream.write(b'azerty')
        self.assertEqual(stream.get(), b'azerty')

        with self.assertRaises(AttributeError):
            self.x

    def test_password(self):
        """Test stream consistent behavior with a specific password."""
        stream = module.ZiphyrStream(b'Setec Astronomy')

        self.assertTrue(stream.writable())
        self.assertFalse(stream.seekable())

        self.assertEqual(stream.x, 634591792)
        self.assertEqual(stream.y, 1488870758)
        self.assertEqual(stream.z, 2152654391)

        stream.write(b'azerty')
        self.assertEqual(stream.get(), b'azerty')

        c = stream.cypher_chunk(b'too many secrets')
        self.assertEqual(
            c, b'\x8d\x1df\xf1"4(\xe1\x00\xdd\xc8\xf3\x0f\x9f(\x8a'
        )

        self.assertEqual(stream.x, 3410687069)
        self.assertEqual(stream.y, 4199982011)
        self.assertEqual(stream.z, 3483152694)
