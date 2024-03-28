# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""Unit tests for the utils module."""

import unittest

from ..utils import group_text


class UtilsTestCase(unittest.TestCase):

    def test_group_text(self):
        s = ''
        r = group_text(s)
        self.assertEqual(r, '')

        s = 'ABCDE'
        r = group_text(s)
        self.assertEqual(r, 'ABCDE')

        s = 'ABCDEFGH'
        r = group_text(s)
        self.assertEqual(r, 'ABCDE FGH')

        s = 'ABCDEFGH'
        r = group_text(s, 3)
        self.assertEqual(r, 'ABC DEF GH')
