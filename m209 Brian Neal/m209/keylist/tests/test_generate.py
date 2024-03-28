# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""Tests for the key list generator functions."""

import collections
import random
import unittest

from ..generate import (generate_key_list, pin_list_check, check_overlaps,
                        KeyListGenError)
from m209.converter import M209
from m209.data import KEY_WHEEL_DATA
from m209.drum import Drum
from m209.keylist.data import GROUP_A, GROUP_B, ALL_DRUM_ROTATE_INPUTS


def make_pin_list(eff_cnt):
    """Generates a pin list with an effect pin count given by eff_cnt."""
    cards = [1] * eff_cnt
    cards.extend([0] * (131 - len(cards)))
    random.shuffle(cards)
    deck = collections.deque(cards)
    pin_list = []
    for letters, _ in KEY_WHEEL_DATA:
        pins = [c for c in letters if deck.pop()]
        pin_list.append(''.join(pins))

    return pin_list


class GenerateTestCase(unittest.TestCase):

    def setUp(self):

        self.valid_pin_list = [
            'FGIKOPRSUVWYZ',
            'DFGKLMOTUY',
            'ADEFGIORTUVX',
            'ACFGHILMRSU',
            'BCDEFJKLPS',
            'EFGHIJLMNP'
        ]

    def do_test_generate_key_list(self):

        key_list = generate_key_list('BN')
        self.assertEqual(key_list.indicator, 'BN')
        self.assertTrue(isinstance(key_list.pin_list, list))
        self.assertEqual(len(key_list.pin_list), 6)

        for i, pins in enumerate(key_list.pin_list):
            self.assertTrue(all(c in KEY_WHEEL_DATA[i][0] for c in pins))

        m_209 = M209(lugs=key_list.lugs, pin_list=key_list.pin_list)
        m_209.set_key_wheels('AAAAAA')
        s = m_209.encrypt('A' * 26)
        self.assertEqual(s, key_list.letter_check)

    def test_generate_key_list(self):

        for n in range(32):
            self.do_test_generate_key_list()

    def do_test_lug_settings(self, selection, failures, max_lug_attempts=1024):

        try:
            key_list = generate_key_list('BN', lug_selection=selection,
                    max_lug_attempts=max_lug_attempts)
        except KeyListGenError:
            failures.append(selection)
            return

        drum = Drum.from_key_list(key_list.lugs)

        vals = set()
        for pins in ALL_DRUM_ROTATE_INPUTS:
            val = drum.rotate(pins)
            self.assertTrue(1 <= val <= 27)
            vals.add(val)
            if len(vals) == 27:
                break
        else:
            self.fail('Invalid drum settings (1-27 check)')

    def test_key_list_group_a(self):

        failures = []
        for selection in GROUP_A:
            self.do_test_lug_settings(selection, failures)

        if failures:
            self.fail("Group A failures: %s" % failures)

    def test_key_list_group_b(self):

        failures = []
        for selection in GROUP_B:
            self.do_test_lug_settings(selection, failures)

        if failures:
            self.fail("Group B failures: %s" % failures)

    def test_pin_list_check(self):

        # Effective pin ratio too high (100%)
        all_pins = [t[0] for t in KEY_WHEEL_DATA]
        self.assertEqual(False, pin_list_check(all_pins))

        # Effective pin ratio too low (0%)
        no_pins = ['' for i in range(6)]
        self.assertEqual(False, pin_list_check(no_pins))

        # Effective pin ratio too low (< 40%)
        self.assertFalse(pin_list_check(make_pin_list(10)))
        self.assertFalse(pin_list_check(make_pin_list(20)))
        self.assertFalse(pin_list_check(make_pin_list(30)))
        self.assertFalse(pin_list_check(make_pin_list(40)))
        self.assertFalse(pin_list_check(make_pin_list(50)))

        # Effective pin ratio too high (< 60%)
        self.assertFalse(pin_list_check(make_pin_list(79)))
        self.assertFalse(pin_list_check(make_pin_list(85)))
        self.assertFalse(pin_list_check(make_pin_list(95)))
        self.assertFalse(pin_list_check(make_pin_list(100)))
        self.assertFalse(pin_list_check(make_pin_list(125)))

    def test_consecutive_effective_pins_0(self):

        pin_list = self.valid_pin_list
        pin_list[0] = 'ABEGHIJKLNOSUZ'
        self.assertTrue(pin_list_check(pin_list))
        pin_list[0] = 'ABEGHIJKLM'
        self.assertFalse(pin_list_check(pin_list))
        pin_list[0] = 'ABEGHIJKLMN'
        self.assertFalse(pin_list_check(pin_list))
        pin_list[0] = 'ABCDEFGHIJ'
        self.assertFalse(pin_list_check(pin_list))
        pin_list[0] = 'BDJKLMNOPTW'
        self.assertFalse(pin_list_check(pin_list))
        pin_list[0] = 'BEFGHIJKSUX'
        self.assertFalse(pin_list_check(pin_list))
        pin_list[0] = 'ABCDGKOTXYZ'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_effective_pins_1(self):

        pin_list = self.valid_pin_list
        pin_list[1] = 'BCEGIKMOTUVXYZ'
        self.assertTrue(pin_list_check(pin_list))
        pin_list[1] = 'ABCEGIKMOTUVXYZ'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_effective_pins_2(self):

        pin_list = self.valid_pin_list
        pin_list[2] = 'ACEGIKMOSTUVX'
        self.assertTrue(pin_list_check(pin_list))
        pin_list[2] = 'ABEGIKMOSTUVX'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_effective_pins_3(self):

        pin_list = self.valid_pin_list
        pin_list[3] = 'ACEGIKMOSTU'
        self.assertTrue(pin_list_check(pin_list))
        pin_list[3] = 'ABCDGIKMOSTU'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_effective_pins_4(self):

        pin_list = self.valid_pin_list
        pin_list[4] = 'ABCEGIKMOQRS'
        self.assertTrue(pin_list_check(pin_list))
        pin_list[4] = 'ABGIKMOPQRS'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_effective_pins_5(self):

        pin_list = self.valid_pin_list
        pin_list[5] = 'ABCEGIKMOQ'
        self.assertTrue(pin_list_check(pin_list))
        pin_list[5] = 'ABGIKMNOPQ'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_noneffective_pins_0(self):

        pin_list = self.valid_pin_list
        pin_list[0] = 'ABCDENOPQSUWYZ'
        self.assertFalse(pin_list_check(pin_list))
        pin_list[0] = 'BCDFGHJKLMOPRST'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_noneffective_pins_1(self):

        pin_list = self.valid_pin_list
        pin_list[1] = 'CDEGHJKLNOPQRST'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_noneffective_pins_2(self):

        pin_list = self.valid_pin_list
        pin_list[2] = 'CDEFHIJKMNOPQRS'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_noneffective_pins_3(self):

        pin_list = self.valid_pin_list
        pin_list[3] = 'CDEGHIKLNOP'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_noneffective_pins_4(self):

        pin_list = self.valid_pin_list
        pin_list[4] = 'EFGIJKMOP'
        self.assertFalse(pin_list_check(pin_list))

    def test_consecutive_noneffective_pins_5(self):

        pin_list = self.valid_pin_list
        pin_list[5] = 'DEFHIKLM'
        self.assertFalse(pin_list_check(pin_list))


class CheckOverlapsTestCase(unittest.TestCase):

    def test_most_of_six(self):

        self.assertTrue(check_overlaps([(0, 1, 2), (0, 2, 2)]))
        self.assertTrue(check_overlaps([(0, 1, 2), (0, 2, 1), (0, 3, 1)]))
        self.assertTrue(check_overlaps([(0, 1, 2), (1, 2, 1), (1, 3, 1), (4, 5, 1)]))
        self.assertFalse(check_overlaps([(0, 1, 2), (0, 2, 1), (1, 2, 1)]))
        self.assertFalse(check_overlaps([(2, 4, 2), (2, 5, 1), (4, 5, 1)]))

    def test_separated(self):

        self.assertTrue(check_overlaps([(0, 1, 1)]))
        self.assertTrue(check_overlaps([(0, 2, 1)]))
        self.assertFalse(check_overlaps([(0, 1, 1), (1, 2, 1)]))
        self.assertFalse(check_overlaps([(0, 1, 1), (1, 2, 1), (3, 4, 1)]))
        self.assertFalse(check_overlaps([(0, 1, 1), (1, 2, 1), (3, 4, 1), (4, 5, 1)]))

    def test_side_by_side(self):

        self.assertTrue(check_overlaps([(0, 1, 1)]))
        self.assertTrue(check_overlaps([(0, 2, 1)]))
        self.assertFalse(check_overlaps([(0, 2, 1), (1, 3, 1)]))
        self.assertFalse(check_overlaps([(0, 2, 1), (1, 3, 1), (2, 4, 1)]))
        self.assertFalse(check_overlaps([(0, 2, 1), (1, 3, 1), (2, 4, 1), (2, 5, 1)]))

