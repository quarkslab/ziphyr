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

        self.assertEqual(stream.x, 305419896)
        self.assertEqual(stream.y, 591751049)
        self.assertEqual(stream.z, 878082192)

        stream.write(b'azerty')
        self.assertEqual(stream.get(), b'azerty')

        c = stream.cypher_chunk(b'no more secrets')
        self.assertEqual(
            c, b'\xc5\x13\xb5}E\xeb\x95\xcb\xec\xa7C\xdd\xe0\xb6\x8b'
        )

        self.assertEqual(stream.x, 3375634188)
        self.assertEqual(stream.y, 478167685)
        self.assertEqual(stream.z, 1020505358)

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
