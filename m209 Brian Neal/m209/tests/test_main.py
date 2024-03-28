# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

import os
import tempfile
import unittest

from ..main import main


class KeyGenTestCase(unittest.TestCase):

    def setUp(self):

        self.fp = tempfile.NamedTemporaryFile(mode='w')

    def tearDown(self):

        self.fp.close()

    def test_overwrite(self):
        """Verify we exit if the key file already exists"""

        argv = ['keygen', '--start=YA', '--number=100', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

    def test_too_many(self):
        """Verify we exit if we can't generate N key lists if start is too
        high

        """
        argv = ['keygen', '--start=YA', '--number=100', '-o', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

    def test_nominal_random(self):
        """Test we can generate N key lists with random indicators"""

        argv = ['keygen', '--number=10', '-o', '-z', self.fp.name]
        main(argv)

    def test_nominal_start(self):
        """Test we can generate N key lists with a fixed starting indicator"""

        argv = ['keygen', '--start=GG', '--number=10', '-o', '-z', self.fp.name]
        main(argv)


class EncryptDecryptBadArgsTestCase(unittest.TestCase):

    def test_no_key_file(self):
        """Ensure we exit if key file doesn't exist"""

        fp = tempfile.NamedTemporaryFile()
        name = fp.name
        fp.close()

        argv = ['encrypt', '--text=TEST', '-z', name]
        self.assertRaises(SystemExit, main, argv)

        argv = ['decrypt', '--text=TEST', '-z', name]
        self.assertRaises(SystemExit, main, argv)


class EncryptDecryptTestCase(unittest.TestCase):

    def setUp(self):

        self.fp = tempfile.NamedTemporaryFile(mode='w')
        argv = ['keygen', '--start=GG', '--number=10', '-o', '-z', self.fp.name]
        main(argv)

    def tearDown(self):

        self.fp.close()

    def test_conflicting_sources(self):
        """Ensure -f or -t is supplied but not both"""

        argv = ['encrypt', '--text=TEST', '-f', '-', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

        argv = ['encrypt', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

        argv = ['decrypt', '--text=TEST', '-f', '-', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

        argv = ['decrypt', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

    def test_encrypt_text(self):

        argv = ['encrypt', '--text=TEST', '--key-list-ind=GG', '-z', self.fp.name]
        main(argv)

    def test_encrypt_text_no_key_list(self):

        argv = ['encrypt', '--text=TEST', '--key-list-ind=GA', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

    def test_encrypt_file(self):

        infile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        infile.write("TEST")
        filename = infile.name
        infile.close()

        argv = ['encrypt', '-f', filename, '--key-list-ind=GG', '-z', self.fp.name]
        try:
            main(argv)
        finally:
            os.remove(filename)

    def test_decrypt_text(self):

        argv = ['decrypt', '-t', 'OOOZS IENGA DSGJX OOOZS IENGA', '-z', self.fp.name]
        self.assertRaises(SystemExit, main, argv)

    def test_decrypt_text_no_key_list(self):

        argv = ['decrypt', '-t', 'OOOZS IENGG DSGJX OOOZS IENGG', '-z', self.fp.name]
        main(argv)

    def test_decrypt_file(self):

        infile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        infile.write("OOOZS IENGG DSGJX OOOZS IENGG")
        filename = infile.name
        infile.close()

        argv = ['decrypt', '-f', filename, '-z', self.fp.name]
        try:
            main(argv)
        finally:
            os.remove(filename)
