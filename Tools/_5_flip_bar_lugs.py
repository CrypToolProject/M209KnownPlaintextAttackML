import json
import random
from _1_keygen_json import inflate_lugs, deflate_lugs

"""
Lug settings and there neighbours:

# Each non '-' represents a possible position of the two Lugs on a bar.
# The position 0-0 is technically possible. But because every bar MUST have
  one lug set to non 0, it is against the rules.
# The position 1-0 (the Ts) and 0-6 (the Hs) are one the board twice. 
  To find there neighbours one have to consider both occurrences.
┌───────────────────────┐
│         2. LUG        │
│      1 0 2 3 4 5 0 6  │
│        ┌─────────┐    │
│    1 - T X X X X T X  │
│ 1  0 - - X X X X 0 H┐ │
│ .  2 - - - X X X X X│ │
│    3 - - - - X X X X│ │
│ L  4 - - - - - X X X│ │
│ U  5 - - - - - - X X│ │
│ G  0 - - - - - - - H┘ │
│    6 - - - - - - - -  │
└───────────────────────┘
"""

""" Dictionary of possible lug-setting and the neighbours (a directed graph) """
LUG_SETTING_NEIGHBOURS = {
    '0-2': ['1-2', '0-3'],
    '0-3': ['1-3', '2-3', '0-2', '0-4'],
    '0-4': ['1-4', '2-4', '0-3', '0-5'],
    '0-5': ['1-5', '2-5', '0-4'],
    '0-6': ['5-6', '1-6', '2-6'],
    '1-0': ['1-2', '1-5', '1-6'],
    '1-2': ['0-2', '1-0', '1-3'],
    '1-3': ['0-3', '1-2', '1-4'],
    '1-4': ['0-4', '0-3', '0-5'],
    '1-5': ['0-5', '1-4', '1-0'],
    '1-6': ['0-6', '1-0'],
    '2-0': ['3-0', '2-5', '2-6'],
    '2-3': ['0-3', '2-4'],
    '2-4': ['0-4', '3-4', '2-3', '2-5'],
    '2-5': ['0-5', '3-5', '2-4', '2-0'],
    '2-6': ['0-6', '3-6', '2-0'],
    '3-0': ['2-0', '4-0', '3-5', '3-6'],
    '3-4': ['2-4', '3-5'],
    '3-5': ['2-5', '4-5', '3-4', '3-0'],
    '3-6': ['2-6', '4-6', '3-0'],
    '4-0': ['3-0', '5-0', '4-5', '4-6'],
    '4-5': ['3-5', '4-0'],
    '4-6': ['3-6', '5-6', '4-0'],
    '5-0': ['4-0', '5-6'],
    '5-6': ['4-6', '0-6', '5-0']
}


class FlipBarLugs:
    """
    A Class to produce bit-flips lug-settings section of a keyfile.
    The constructor only needs the path of folder of the keyfiles
    and the path to save the flipped keyfiles as inputs.

    To work with the keyfiles in parallel, the concrete filename of the
    keyfile and the number of bits to flip are only required when
    calling flip().
    """
    def __init__(self, path_keys, path_keys_lugs_flipped):
        self.path_keys = path_keys
        self.path_keys_lugs_flipped = path_keys_lugs_flipped

    def flip(self, keyfile, bits):
        """
        Takes each key from a keyfile and moves random lugs "bits"-times.
        :param keyfile: Filename of the keyfile to work with.
        :param bits: Number of times to move lugs.
        """

        with open(self.path_keys + keyfile, 'r') as infile:
            keys = json.load(infile)

        for j, key in enumerate(keys):
            new_lug_data = inflate_lugs(key[2])

            for _ in range(bits):
                choice = random.randint(0, 26)
                new_lug_data[choice] = random.choice(LUG_SETTING_NEIGHBOURS[new_lug_data[choice]])

            keys[j][2] = deflate_lugs(new_lug_data)

        filename = self.path_keys_lugs_flipped + f"{str(bits)}_" + keyfile
        with open(filename, 'w') as outfile:
            json.dump(keys, outfile)
