import json
import random
import os
import sys
import string

sys.path.append("../m209 Brian Neal")

from m209.procedure import StdProcedure
from m209.keylist import KeyList
from m209.keylist.generate import generate_letter_check
from m209.converter import M209_ALPHABET_LIST
from m209.data import KEY_WHEEL_DATA

CIPHER_TABLE = list(reversed(string.ascii_uppercase))


def _create_indicators(proc):
    while True:
        try:
            ext_msg_ind = proc.m_209.set_random_key_wheels()
            sys_ind = random.choice(M209_ALPHABET_LIST)
            sys_ind_enc = proc.m_209.encrypt(sys_ind * 12, group=False)

            it = iter(sys_ind_enc)
            n = 0
            int_msg_ind = ""
            while n != 6:
                indicator = next(it)
                if indicator in KEY_WHEEL_DATA[n][0]:
                    int_msg_ind += indicator
                    n += 1
            break

        except StopIteration:
            continue

    return sys_ind, ext_msg_ind, int_msg_ind


class EncryptSorted:

    def __init__(self, key_path="keys/", destin_path="ciphertexts_Gut/", count_a=200,
                 append_plaintext=False, append_ciphertext=True, append_keystream=False,
                 append_lugs=False, append_pins=False):
        self.int_msg_ind = None
        self.gutenberg_en = None
        self.key_path = key_path
        self.destin_path = destin_path
        self.count_a = count_a
        self.append_plaintext = append_plaintext
        # self.append_ciphertext = append_ciphertext
        self.append_keystream = append_keystream
        self.append_lugs = append_lugs
        self.append_pins = append_pins
        self.int_msg_ind_preset = False
        self.keys = None

    def load_gutenberg(self, gutenberg_path):
        """
        Loads all files of the prepared Gutenberg dataset one after the other into a list.
        :param gutenberg_path: Path to the prepared Gutenberg dataset.
        """
        self.gutenberg_en = []
        for file in os.listdir(gutenberg_path)[:1]:
            with open(gutenberg_path + file, 'r') as infile:
                self.gutenberg_en += (json.load(infile))

    def set_int_msg_ind(self, int_msg_ind):
        """
        Setter for the Internal Message Indicator. If int_msg_ind_preset == True,
        the value is not randomly generated later on.
        :param int_msg_ind: Internal Message Indicator in the form of a String like "AAAAAA"
        """
        self.int_msg_ind = int_msg_ind
        self.int_msg_ind_preset = True

    def _plaintext(self, ):
        """
        An implementation of a plaintext generator.
        :return: IF the Gutenberg dataset has been loaded, a random record will be returned.
                 Otherwise, a string of "A "s the length of count_a
        """
        if self.gutenberg_en is None:
            while True:
                yield "A" * self.count_a
        else:
            while True:
                yield random.choice(self.gutenberg_en)

    def load_keys(self, source, filetype):
        if filetype == "single_json":
            with open(source, 'r') as infile:
                self.keys = json.load(infile)
        if filetype == "pins_n_lugs":
            with open(source[0], 'r') as infile:
                lugs = json.load(infile)
                random.shuffle(lugs)
            with open(source[1], 'r') as infile:
                pins = json.load(infile)
                random.shuffle(pins)
            self.keys = []
            for x in enumerate(zip(pins, lugs)):
                letter_check = generate_letter_check(x[1][1], x[1][0])
                self.keys.append([x[0], x[1][0], x[1][1], letter_check])

    def encrypt_sorted(self, keyfile,dest_file):
        """
        Encrypts a plaintext with each key in the specified key file.
        :param keyfile: Name of the keyfile in key_path.
        """

        destination = self.destin_path + dest_file

        ciphertexts = []

        # loads Keys if not already loaded.
        if self.keys is None:
            self.load_keys(self.key_path+keyfile, "single_json")
            # raise Exception("Keys not loaded")


        for setting in self.keys:
            x = random.randint(0, 25)
            y = random.randint(0, 25)

            """ The indicator is always "AA" because it has no meaning for this
                project and there will be more ciphertexts than 26*26 anyway. """

            key_list = KeyList(
                indicator=chr(x + ord('A')) + chr(y + ord('A')),
                pin_list=setting[1],
                lugs=setting[2],
                letter_check=setting[3])

            proc = StdProcedure(key_list=key_list, )

            plaintext = self._plaintext().__next__()

            sys_ind, ext_msg_ind, int_msg_ind = _create_indicators(proc)

            """ Overwrites the calculated int_msg_ind with the preset value """
            if self.int_msg_ind_preset:
                int_msg_ind = self.int_msg_ind

            ciphertexts.append([setting[0], int_msg_ind])

            """ Appends the Plaintext if needed """
            if self.append_plaintext:
                ciphertexts[-1].append(plaintext)

            ciphertext = proc.encrypt(plaintext, ext_msg_ind=ext_msg_ind, sys_ind=sys_ind, int_msg_ind=int_msg_ind)

            """ Appends the Ciphertext if needed """
            # if self.append_ciphertext:
            ciphertexts[-1].append(ciphertext)

            """ Appends the Keystream if needed """
            if self.append_keystream:
                keystream = []
                for p, c in zip(plaintext.replace(" ", "Z"), ciphertext.replace(" ", "")):
                    p = string.ascii_uppercase.index(p)
                    c = CIPHER_TABLE.index(c)
                    keystream.append((p-c) % 26)

                # Keystream as String to save Diskspace
                ciphertexts[-1].append("".join([chr(a + ord('A')) for a in keystream]))

            """ Appends the Pin-Settings if needed """
            if self.append_pins:
                ciphertexts[-1].append(setting[1])

            """ Appends the Lug-Settings if needed """
            if self.append_lugs:
                ciphertexts[-1].append(setting[2])

        """ Saves the Ciphertexts and the selected metadata to disk"""
        with open(destination, 'w') as outfile:
            json.dump(ciphertexts, outfile)
