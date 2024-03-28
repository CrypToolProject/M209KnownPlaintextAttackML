# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""Unit tests for the M209 encrypt & decrypt procedures."""

import unittest

from ..keylist import KeyList
from ..procedure import StdProcedure, ProcedureError


PLAINTEXT = 'ATTACK AT DAWN'
CIPHERTEXT = 'GGABC DEFFM NQHNL CAARZ OLTVX GGABC DEFFM'


class ProcedureTestCase(unittest.TestCase):

    def setUp(self):
        self.fm = KeyList(indicator="FM",
                    lugs='1-0 2-0*8 0-3*7 0-4*5 0-5*2 1-5 1-6 3-4 4-5',
                    pin_list=[
                        'BCEJOPSTUVXY',
                        'ACDHJLMNOQRUYZ',
                        'AEHJLOQRUV',
                        'DFGILMNPQS',
                        'CEHIJLNPS',
                        'ACDFHIMN'
                    ],
                    letter_check='TNMYS CRMKK UHLKW LDQHM RQOLW R')
        self.proc = StdProcedure(key_list=self.fm)

    def test_encrypt(self):
        result = self.proc.encrypt(PLAINTEXT, ext_msg_ind='ABCDEF', sys_ind='G')
        self.assertEqual(result, CIPHERTEXT)

    def test_decrypt(self):
        result = self.proc.set_decrypt_message(CIPHERTEXT)

        self.assertEqual(result.sys_ind, 'G')
        self.assertEqual(result.ext_msg_ind, 'ABCDEF')
        self.assertEqual(result.key_list_ind, 'FM')
        self.assertEqual(result.ciphertext, CIPHERTEXT[12:29])

        plaintext = self.proc.decrypt()
        self.assertEqual(plaintext[:len(PLAINTEXT)], PLAINTEXT)

    def test_encrypt_padding(self):
        """Ensure we pad the final group out to 5 chars."""

        for n in range(1, 21):
            pt = 'A' * n
            ct = self.proc.encrypt(pt)
            groups = ct.split()
            counts_good = [len(group) == 5 for group in groups]
            self.assertTrue(all(counts_good), "Failed on n = %s; ct = %s" % (n, ct))

    def test_blair_decrypt(self):

        ciphertext = (
            'DDGPD UCOFM JSCPS XZTGR HHWJG '
            'BDKKK SHISC IMDFK RLUVH TWGAW '
            'SUYMM VZBQP OEBJE KPMBW GPGNI '
            'OFGAL VRYJC LSPLJ GRFYE UQVZT '
            'PSNDT OAPYG SKGKM CKQTD JCPBE '
            'NHYRX DDGPD UCOFM')
        plaintext = ('MISSION ACCOMPLISHED X ALL ENEMY FORCES NEUTRALI ED X'
                     '  ERO CASUALTIES X EIGHT PRISONERS TAKEN X'
                     ' AWAITING FURTHER ORDERSO')

        result = self.proc.set_decrypt_message(ciphertext)

        self.assertEqual(result.sys_ind, 'D')
        self.assertEqual(result.ext_msg_ind, 'GPDUCO')
        self.assertEqual(result.key_list_ind, 'FM')
        self.assertEqual(result.ciphertext, ciphertext[12:-12])

        result = self.proc.decrypt()
        self.assertEqual(result, plaintext)


class ProcedureErrorsTestCase(unittest.TestCase):

    def setUp(self):
        self.fm = KeyList(indicator="FM",
                    lugs='1-0 2-0*8 0-3*7 0-4*5 0-5*2 1-5 1-6 3-4 4-5',
                    pin_list=[
                        'BCEJOPSTUVXY',
                        'ACDHJLMNOQRUYZ',
                        'AEHJLOQRUV',
                        'DFGILMNPQS',
                        'CEHIJLNPS',
                        'ACDFHIMN'
                    ],
                    letter_check='TNMYS CRMKK UHLKW LDQHM RQOLW R')

    def test_encrypt_no_key_list(self):
        proc = StdProcedure()
        self.assertRaises(ProcedureError, proc.encrypt, 'TEST')

    def test_encrypt_bad_ext_msg_ind(self):
        proc = StdProcedure(key_list=self.fm)
        self.assertRaises(ProcedureError, proc.encrypt, 'TEST', ext_msg_ind='WWWWWW')

    def test_encrypt_bad_sys_ind(self):
        proc = StdProcedure(key_list=self.fm)
        self.assertRaises(ProcedureError, proc.encrypt, 'TEST', sys_ind='!')

    def test_decrypt_invalid_msg(self):
        proc = StdProcedure(key_list=self.fm)
        self.assertRaisesRegex(ProcedureError, 'message format',
                proc.set_decrypt_message, 'TEST')

    def test_decrypt_invalid_sys_ind(self):
        proc = StdProcedure(key_list=self.fm)

        ciphertext = 'GZABC DEFFM NQHNL CAARZ OLTVX GZABC DEFFM'
        self.assertRaisesRegex(ProcedureError, 'system indicator',
                proc.set_decrypt_message, ciphertext)

    def test_decrypt_no_params(self):
        proc = StdProcedure(key_list=self.fm)
        self.assertRaises(ProcedureError, proc.decrypt)

    def test_decrypt_no_key_list(self):
        proc = StdProcedure()
        proc.set_decrypt_message(CIPHERTEXT)
        self.assertRaisesRegex(ProcedureError, "key list 'FM' required", proc.decrypt)

    def test_decrypt_wrong_key_list(self):
        proc = StdProcedure(self.fm)
        ciphertext = 'GGABC DEFYL NQHNL CAARZ OLTVX GGABC DEFYL'
        proc.set_decrypt_message(ciphertext)
        self.assertRaisesRegex(ProcedureError, "key list 'YL' required", proc.decrypt)

