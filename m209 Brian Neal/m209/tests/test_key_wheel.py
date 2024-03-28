# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""test_key_wheel.py - Unit tests for the KeyWheel class for the M-209
simulation.

"""
import random
import string
import unittest

from ..key_wheel import KeyWheel, KeyWheelError


class KeyWheelTestCase(unittest.TestCase):
    """Basic tests to verify KeyWheel functionality"""

    def test_bad_init(self):
        self.assertRaises(KeyWheelError, KeyWheel, [], 'X')
        self.assertRaises(KeyWheelError, KeyWheel, '', 'X')
        self.assertRaises(KeyWheelError, KeyWheel, 'A', 'X')
        self.assertRaises(KeyWheelError, KeyWheel, 'ABCDEFG', 'X')
        self.assertRaises(KeyWheelError, KeyWheel, 'ABCDEFG', 'G', 'X')
        self.assertRaises(KeyWheelError, KeyWheel, 'ABCDEFG', 'G', 'AX')
        self.assertRaises(KeyWheelError, KeyWheel, 'ABCDEFG', 'G', 'AXG')

    def test_reset_pins(self):
        letters = string.ascii_uppercase
        kw = KeyWheel(letters, 'F', 'ACEGHLMQSXY')
        kw.reset_pins()
        for c in letters:
            self.assertFalse(kw.is_effective())
            kw.rotate()

        kw = KeyWheel(letters, 'P', letters)
        kw.reset_pins()
        for c in letters:
            self.assertFalse(kw.is_effective())
            kw.rotate()
        for c in letters:
            self.assertFalse(kw.is_effective())
            kw.rotate()

    def test_set_pins(self):
        letters = string.ascii_uppercase
        kw = KeyWheel(letters, 'P', letters)
        for c in letters:
            self.assertTrue(kw.is_effective())
            kw.rotate()

        kw = KeyWheel(letters, 'P')
        kw.set_pins(letters)
        for c in letters:
            self.assertTrue(kw.is_effective())
            kw.rotate()

        kw = KeyWheel(letters, 'P')
        kw.set_pins([])
        for c in letters:
            self.assertFalse(kw.is_effective())
            kw.rotate()

        kw = KeyWheel(letters, 'P')
        for n in range(0, len(letters) + 1):
            pins = random.sample(letters, n)
            kw.set_pins(pins)
            for c in letters:
                if kw.guide_letter() in pins:
                    self.assertTrue(kw.is_effective())
                else:
                    self.assertFalse(kw.is_effective())
                kw.rotate()

    def test_set_pins_bad(self):
        letters = 'ABCDEFG'
        kw = KeyWheel(letters, 'F')
        self.assertRaises(KeyWheelError, kw.set_pins, 'X')
        self.assertRaises(KeyWheelError, kw.set_pins, 'AX')
        self.assertRaises(KeyWheelError, kw.set_pins, 'XA')
        self.assertRaises(KeyWheelError, kw.set_pins, 'AXFG')

    def test_rotate_display(self):
        letters = string.ascii_uppercase
        kw = KeyWheel(letters, 'P')
        for n in range(5):
            for c in letters:
                self.assertTrue(c == kw.display())
                kw.rotate()

        for n in range(5):
            for c in letters[::2]:
                self.assertTrue(c == kw.display())
                kw.rotate(2)

        for n in range(5):
            for c in letters[1::2]:
                kw.rotate(1)
                self.assertTrue(c == kw.display())
                kw.rotate(1)

    def test_set_pos(self):
        letters = string.ascii_uppercase
        kw = KeyWheel(letters, 'P')
        for c in letters:
            kw.set_pos(c)
            self.assertEqual(c, kw.display())

    def test_str(self):
        kw = KeyWheel(string.ascii_uppercase, 'P', 'FGIKOPRSUVWYZ')
        self.assertEqual(str(kw), ('-A -B -C -D -E F- G- -H I- -J K- -L -M -N '
                                   'O- P- -Q R- S- -T U- V- W- -X Y- Z-'))
