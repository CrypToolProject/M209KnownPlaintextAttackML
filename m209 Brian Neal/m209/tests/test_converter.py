# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""test_converter.py - Unit tests for the M209 class for the M-209 simulation."""

import unittest

from .. import M209Error
from ..converter import M209


# Data taken from Mark J. Blair's AA key list
AA_LUGS = '0-4 0-5*4 0-6*6 1-0*5 1-2 1-5*4 3-0*3 3-4 3-6 5-6'

AA_PIN_LIST = [
    'FGIKOPRSUVWYZ',
    'DFGKLMOTUY',
    'ADEFGIORTUVX',
    'ACFGHILMRSU',
    'BCDEFJKLPS',
    'EFGHIJLMNP'
]

AA_CHECK = 'QLRRN TPTFU TRPTN MWQTV JLIJE J'


class M209TestCase(unittest.TestCase):

    def test_invalid_set_pins(self):
        """Ensure invalid inputs raise errors."""
        m = M209()
        pins = 'BFJKLOSTUWXZ'
        self.assertRaises(M209Error, m.set_pins, -1, pins)
        self.assertRaises(M209Error, m.set_pins, -2, pins)
        self.assertRaises(M209Error, m.set_pins, 6, pins)
        self.assertRaises(M209Error, m.set_pins, 7, pins)
        self.assertRaises(M209Error, m.set_pins, 100, pins)

    def test_invald_set_all_pins(self):
        m = M209()
        self.assertRaises(M209Error, m.set_all_pins, 'A')

        bad_pins1 = AA_PIN_LIST * 2
        self.assertRaises(M209Error, m.set_all_pins, bad_pins1)
        bad_pins2 = ['ABCD', 'EFGH', 'XYZ']
        self.assertRaises(M209Error, m.set_all_pins, bad_pins2)

    def letter_check(self, lugs, pin_list, check):
        """Generic letter check routine"""

        pt = 'A' * 26
        ct = check

        m = M209(lugs, pin_list)

        result = m.encrypt(pt)
        self.assertEqual(result, ct)
        self.assertEqual(m.letter_counter, 26)

        m.letter_counter = 0
        m.set_key_wheels('A' * 6)
        result = m.decrypt(ct)

        self.assertEqual(result, pt)
        self.assertEqual(m.letter_counter, 26)

    def test_aa_letter_check(self):
        """See if we can pass a letter check using Mark J. Blair's AA key list."""

        self.letter_check(AA_LUGS, AA_PIN_LIST, AA_CHECK)

    def test_yl_letter_check(self):
        """See if we can pass a letter check using Mark J. Blair's YL key list."""

        lugs = '1-0 2-0*4 0-3 0-4*3 0-5*3 0-6*11 2-5 2-6 3-4 4-5'

        pin_list = [
            'BFJKLOSTUWXZ',
            'ABDJKLMORTUV',
            'EHJKNPQRSX',
            'ABCHIJLMPQR',
            'BCDGJLNOPQS',
            'AEFHIJP',
        ]

        check = 'OZGPK AFVAJ JYRZW LRJEG MOVLU M'
        self.letter_check(lugs, pin_list, check)

    def test_fm_letter_check(self):
        """See if we can pass a letter check using Mark J. Blair's FM key list."""

        lugs = '1-0 2-0*8 0-3*7 0-4*5 0-5*2 1-5 1-6 3-4 4-5'

        pin_list = [
            'BCEJOPSTUVXY',
            'ACDHJLMNOQRUYZ',
            'AEHJLOQRUV',
            'DFGILMNPQS',
            'CEHIJLNPS',
            'ACDFHIMN'
        ]

        check = 'TNMYS CRMKK UHLKW LDQHM RQOLW R'
        self.letter_check(lugs, pin_list, check)

    def test_no_group(self):

        m = M209(AA_LUGS, AA_PIN_LIST)
        result = m.encrypt('A' * 26, group=False)
        expected = AA_CHECK.replace(' ', '')
        self.assertEqual(result, expected)

    def test_encrpyt_no_spaces(self):

        m = M209()
        self.assertRaises(M209Error, m.encrypt, 'ATTACK AT DAWN', spaces=False)

    def test_encrypt_spaces(self):

        m = M209(AA_LUGS, AA_PIN_LIST)

        wheels = 'YGXREL'
        m.set_key_wheels(wheels)
        result1 = m.encrypt('ATTACK AT DAWN')

        m.set_key_wheels(wheels)
        result2 = m.encrypt('ATTACKZATZDAWN', spaces=False)

        m.set_key_wheels(wheels)
        result3 = m.encrypt('ATTACKZATZDAWN', spaces=True)

        self.assertTrue(result1 == result2 == result3)

    def test_decrpyt_no_spaces(self):

        m = M209()
        self.assertRaises(M209Error, m.decrypt, 'ATTACK AT DAWN', spaces=False)

    def test_decrypt_no_z_sub(self):

        m = M209(AA_LUGS, AA_PIN_LIST)

        pt = 'ATTACK AT DAWN'
        wheels = 'YGXREL'
        m.set_key_wheels(wheels)
        ct = m.encrypt(pt)

        m.set_key_wheels(wheels)
        result = m.decrypt(ct, z_sub=False)

        self.assertEqual(pt.replace(' ', 'Z'), result)

    def test_set_pins_vs_all_pins(self):

        m1 = M209(AA_LUGS, AA_PIN_LIST)

        pt = 'ATTACK AT DAWN'
        wheels = 'YGXREL'
        m1.set_key_wheels(wheels)
        ct1 = m1.encrypt(pt)

        m2 = M209()
        m2.set_drum_lugs(AA_LUGS)
        for n, pins in enumerate(AA_PIN_LIST):
            m2.set_pins(n, pins)

        m2.set_key_wheels(wheels)
        ct2 = m2.encrypt(pt)

        self.assertEqual(ct1, ct2)

    def test_get_settings(self):

        m = M209(AA_LUGS, AA_PIN_LIST)
        settings = m.get_settings()

        self.assertEqual(settings.lugs, AA_LUGS)
        self.assertEqual(settings.pin_list, AA_PIN_LIST)
