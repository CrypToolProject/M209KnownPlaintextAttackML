import json
import random

from key_vectorizer import k2v, v2k

WHEEL_PINS_COUNT = 131


class FlipWheelPins:
    """
    A Class to produce bit-flips pin-settings section of a keyfile.
    The constructor only needs the path of folder of the keyfiles
    and the path to save the flipped keyfiles as inputs.

    To work with the keyfiles in parallel, the concrete filename of the
    keyfile and the number of bits to flip are only required when
    calling flip().
    """
    def __init__(self, path_keys, path_keys_wheels_flipped):
        self.path_keys = path_keys
        self.path_keys_wheels_flipped = path_keys_wheels_flipped

    def flip(self, keyfile, bits):
        """
        Takes each key from a keyfile and flips random pins "bits"-times.
        :param keyfile: Filename of the keyfile to work with.
        :param bits: Number of Bits to flip.
        """

        swap = {"0": "1", "1": "0"}
        number_wheels = list(i for i in range(WHEEL_PINS_COUNT))

        with open(self.path_keys + keyfile, 'r') as infile:
            keys = json.load(infile)

        temp_keys = []
        for key in keys:
            temp_keys.append(k2v(key))

        for i, key in enumerate(temp_keys):
            flips = sorted(random.sample(number_wheels, k=bits))

            for flip in flips:
                temp_keys[i][1] = temp_keys[i][1][:flip - 1] + swap[temp_keys[i][1][flip - 1]] + temp_keys[i][1][flip:]

        for i, key in enumerate(temp_keys):
            temp_keys[i] = v2k(key)

        with open(self.path_keys_wheels_flipped+str(bits)+'_'+keyfile, 'w') as outfile:
            json.dump(temp_keys, outfile)
