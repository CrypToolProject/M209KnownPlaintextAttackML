import json
import sys

sys.path.append("../m209 Brian Neal")

from m209.procedure import StdProcedure
from m209.keylist import KeyList

OFFSET = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
          'M': 12, 'N': 13, 'O': 12, 'P': 11, 'Q': 10, 'R': 9, 'S': 8, 'T': 7, 'U': 6, 'V': 5, 'W': 4,
          'X': 3, 'Y': 2, 'Z': 1, ' ': 1
          }


# DRAFT!!!! #
class Decrypt_flipped_AAAAA:
    """
    A class to decrypt previously encrypted 'A's with a modified key.
    The goal is to calculate the mean error caused by the manipulations/errors in the keys.
    The calculated mean error gets appended to the keys in the keyfile.
    """
    def __init__(self, path_keys, path_ciphertexts):
        self.path_keys = path_keys
        self.path_ciphertexts = path_ciphertexts

    def decrypt(self, filename):

        with open(self.path_keys + filename, 'r') as infile:
            keys = json.load(infile)
        with open(self.path_ciphertexts + filename.split('_')[1] + "_cipher.json", 'r') as infile:
            ciphertexts = json.load(infile)

        if len(keys) != len(ciphertexts):
            raise Exception("length of keyfile and ciphertextfile not identical")
        # print(f"processing {filename}")
        for i in range(len(keys)):
            proc = StdProcedure()
            params = proc.set_decrypt_message(ciphertexts[i][2])
            key_list = KeyList(indicator=params.key_list_ind,
                               pin_list=keys[i][1],
                               lugs=keys[i][2],
                               letter_check=keys[i][3]
                               )

            proc.set_key_list(key_list)
            plaintext = proc.decrypt(int_msg_ind=ciphertexts[i][1])

            # calc mean error
            n = len(plaintext)
            summation = 0
            for p in plaintext:
                summation += OFFSET[p]

            mean_error = summation / n

            keys[i].append(float(mean_error))

        json.dump(keys, open(self.path_keys + filename, 'w'))
