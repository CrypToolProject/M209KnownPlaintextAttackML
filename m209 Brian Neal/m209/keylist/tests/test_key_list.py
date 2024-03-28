# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""Unit tests for the functions in the key_list module."""

import unittest

from ..key_list import valid_indicator, IndicatorIter


INVALID_LIST = ['', 'a', 'aaa', '12', '1', '@', 'A8', 'Az', 'A)']


class IndicatorIterTestCase(unittest.TestCase):

    def test_bad_args(self):

        for ind in INVALID_LIST:
            self.assertRaises(ValueError, IndicatorIter, ind)

    def test_next_initial(self):

        self.assertEqual(next(IndicatorIter()), 'AA')
        self.assertEqual(next(IndicatorIter('AA')), 'AA')
        self.assertEqual(next(IndicatorIter('AB')), 'AB')
        self.assertEqual(next(IndicatorIter('JA')), 'JA')
        self.assertEqual(next(IndicatorIter('ZZ')), 'ZZ')

    def test_range(self):

        result = [v for v in IndicatorIter()]
        self.assertEqual(len(result), 26 ** 2)

        for n in range(26 ** 2):
            x = (ord(result[n][0]) - ord('A')) * 26 + ord(result[n][1]) - ord('A')
            self.assertEqual(x, n)

    def test_len(self):

        n = 26 ** 2
        it = IndicatorIter()
        while n >= 0:
            self.assertEqual(n, len(it))
            try:
                next(it)
            except StopIteration:
                pass
            n -= 1


class ValidIndicatorTestCase(unittest.TestCase):

    def test_invalid(self):

        for ind in INVALID_LIST:
            self.assertFalse(valid_indicator(ind))

    def test_valid(self):

        for i in IndicatorIter():
            self.assertTrue(valid_indicator(i))

