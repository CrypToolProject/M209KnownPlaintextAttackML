# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""Unit tests for the key list read/write routines for the config file
format.

"""

from contextlib import contextmanager
import os
import tempfile
import unittest

from ..key_list import KeyList
from ..config import read_key_list, write


@contextmanager
def file_remover(path):
    """Ensures a file is deleted."""
    try:
        yield
    except Exception:
        raise
    finally:
        os.remove(path)


class ConfigFileTestCase(unittest.TestCase):

    def test_round_trip(self):

        key_list1 = KeyList(
                indicator='AA',
                lugs='0-4 0-5*4 0-6*6 1-0*5 1-2 1-5*4 3-0*3 3-4 3-6 5-6',
                pin_list= [
                    'FGIKOPRSUVWYZ',
                    'DFGKLMOTUY',
                    'ADEFGIORTUVX',
                    'ACFGHILMRSU',
                    'BCDEFJKLPS',
                    'EFGHIJLMNP'
                ],
                letter_check='QLRRN TPTFU TRPTN MWQTV JLIJE J')

        fd, path = tempfile.mkstemp(suffix='.ini', text=True)
        os.close(fd)

        with file_remover(path):
            write(path, [key_list1])
            key_list2 = read_key_list(path, key_list1.indicator)

            self.assertEqual(key_list1, key_list2)

            kl3 = read_key_list(path, 'BB')
            self.assertTrue(kl3 is None)
