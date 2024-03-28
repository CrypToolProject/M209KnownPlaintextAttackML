# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""test_drum.py - Unit tests for the Drum class for the M-209 simulation."""

import unittest

from ..drum import Drum, DrumError


class DrumTestCase(unittest.TestCase):

    def test_invalid_drum(self):
        self.assertRaises(DrumError, Drum, 5)
        self.assertRaises(DrumError, Drum, "fail")

        invalid_lug_list = [(0, 5)] * (Drum.NUM_BARS + 1)
        self.assertRaises(DrumError, Drum, invalid_lug_list)

        invalid_lug_list = [(0, 0)] * Drum.NUM_BARS
        self.assertRaises(DrumError, Drum, invalid_lug_list)

        invalid_lug_list = [(0, 1), (-1, 2), (3, 4)]
        self.assertRaises(DrumError, Drum, invalid_lug_list)

        invalid_lug_list = [(0, ), (1, 8), (3, 4)]
        self.assertRaises(DrumError, Drum, invalid_lug_list)

        invalid_lug_list = [(0, 1), (1, 'x'), (3, 4)]
        self.assertRaises(DrumError, Drum, invalid_lug_list)

        invalid_lug_list = [(0, 1), (1, 8, 1), (3, 4)]
        self.assertRaises(DrumError, Drum, invalid_lug_list)

        invalid_lug_list = [(0, ), (1, 5), (3, 3)]
        self.assertRaises(DrumError, Drum, invalid_lug_list)

    def test_valid_drum(self):
        # These should not raise anything
        drum = Drum()
        self.assertEqual(0, len(drum.bars))

        drum = Drum([])
        drum = Drum(None)
        drum = Drum(lug_list=[])
        drum = Drum([(0, 1), (2, 3), (4, 5), (5, ), (1, )])

        lug_list = [(0,)] * Drum.NUM_BARS
        drum = Drum(lug_list)

        lug_list = [(0, 2)] * Drum.NUM_BARS
        drum = Drum(lug_list)
        self.assertEqual(Drum.NUM_BARS, len(drum.bars))

    def test_invalid_key_list(self):
        key_list = "jkdlaj;af;"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "jkdla-;af;"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "-1--99"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "1-99"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "101-99"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "10-4"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0 1-0 1-0 10-4 2-3"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0 1-0 1-0 4-4 2-3"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0" * (Drum.NUM_BARS + 1)
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0* 1-0 1-0 4-4 2-3"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0 1-0*-3 1-0 4-4 2-3"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0 1-0*-3 1-0 4-4 2*3"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

        key_list = "2-0*10 1-0*2 4-4*10 1-6*6"
        self.assertRaises(DrumError, Drum.from_key_list, key_list)

    def test_valid_key_list(self):
        key_list = "0-6 1-4 2-5"
        drum = Drum.from_key_list(key_list)
        self.assertEqual([(5, ), (0, 3), (1, 4)], drum.bars)

        key_list = "2-4 " + ("0-6 1-4 " * 13).rstrip()
        drum = Drum.from_key_list(key_list)
        bars = [(1, 3)] + [(5, ), (0, 3)] * 13
        self.assertEqual(bars, drum.bars)

        key_list = "2-4 0-6*13 1-4*13"
        drum = Drum.from_key_list(key_list)
        self.assertEqual(sorted(bars), sorted(drum.bars))

    def test_rotate(self):
        # These are just simple tests to flush out syntax errors, etc. Higher
        # level tests will verify the correct operation of the entire machine.

        drum = Drum()
        self.assertEqual(0, drum.rotate([False] * 6))

        drum = Drum()
        self.assertEqual(0, drum.rotate([True] * 6))

        drum = Drum([(1, )] * Drum.NUM_BARS)
        self.assertEqual(drum.NUM_BARS, drum.rotate([True] * 6))

        drum = Drum([(0, 5)] * Drum.NUM_BARS)
        self.assertEqual(drum.NUM_BARS, drum.rotate([True] * 6))

        drum = Drum([(2, 4)] * 10)
        self.assertEqual(10, drum.rotate([False, False, True, False, True, False]))

        drum = Drum([(2, 4)] * 10)
        self.assertEqual(10, drum.rotate([False, False, False, False, True, False]))

    def test_to_key_list(self):

        drum = Drum.from_key_list('1-0*5 0-3*3 0-4 0-5*4 0-6*6 1-2 1-5*4 3-4 3-6 5-6')
        s = drum.to_key_list()
        self.assertEqual(s, '0-4 0-5*4 0-6*6 1-0*5 1-2 1-5*4 3-0*3 3-4 3-6 5-6')

        s = drum.to_key_list(shortcut=False)
        self.assertEqual(s, ('0-4 0-5 0-5 0-5 0-5 0-6 0-6 0-6 0-6 0-6 0-6 1-0 '
            '1-0 1-0 1-0 1-0 1-2 1-5 1-5 1-5 1-5 3-0 3-0 3-0 3-4 3-6 5-6'))
