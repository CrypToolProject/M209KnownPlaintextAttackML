import json
import sys
from collections import Counter
import random

sys.path.append("../m209 Brian Neal")
from m209.keylist.generate import generate_key_list, KeyListGenError, generate_lugs, generate_pin_list
from m209.keylist.data import GROUP_A, GROUP_B
DEFAULT_FILENAME = "key.json"



def _lug_selection(min_overlaps=None, max_overlaps=None):
    while True:
        rn = random.randint(0, 100)
        group = GROUP_A if rn > 10 else GROUP_B
        selection = random.choice(group)

        if min_overlaps is None and max_overlaps is None:
            break
        if min_overlaps is None:
            if sum(selection) - 27 <= max_overlaps:
                break
        if max_overlaps is None:
            if sum(selection) - 27 >= min_overlaps:
                break
        else:
            if min_overlaps <= sum(selection) - 27 <= max_overlaps:
                break

    random.shuffle(selection)
    return selection


class KeyGen:

    def __init__(self, count=10_000, path="keys/"):
        self.count = count
        self.path = path
        self.min_overlaps = None
        self.max_overlaps = None

    def keygen_json(self, filename, interactive=False):
        key_lists = None

        if interactive:
            print(f"\nGenerating file {filename} ")
        while True:
            try:
                key_lists = [generate_key_list("AA", max_lug_attempts=10000) for _ in range(self.count)]
                break
            except KeyListGenError as err:
                if interactive:
                    print('Handling run-time error: ', err)
                continue

        json_dict = []

        for key_list in key_lists:
            json_dict.append(
                {"pin_list": key_list.pin_list,
                 "lugs": key_list.lugs,
                 "letter_check": key_list.letter_check
                 }
            )

        with open(self.path + filename, 'w') as outfile:
            json.dump(json_dict, outfile)

    def keygen_json_lugs(self, filename):
        lugs = []

        for _ in range(self.count):
            while True:
                try:
                    lugs.append(generate_lugs(lug_selection=_lug_selection(self.min_overlaps, self.max_overlaps),
                                              max_attempts=10000))
                    break
                except KeyListGenError as err:
                    continue

        json_dict = []

        for lug in lugs:
            json_dict.append(lug)

        with open(self.path + filename, 'w') as outfile:
            json.dump(json_dict, outfile)

    def keygen_json_pins(self, filename):
        pin_list = None

        while True:
            try:
                pin_list = (generate_pin_list(max_attempts=10000) for _ in range(self.count))
                break
            except KeyListGenError as err:
                continue

        json_dict = []

        for pins in pin_list:
            json_dict.append(pins)

        with open(self.path + filename, 'w') as outfile:
            json.dump(json_dict, outfile)


def generate_JFB_lug_Settings(key):
    new_lug_data = inflate_lugs(key[2])

    overlaps = Counter(list([x for x in new_lug_data if '0' not in x]))
    count = Counter(''.join(new_lug_data))
    lug_selection = [count.get('1'), count.get('2'), count.get('3'), count.get('4'), count.get('5'), count.get('6')]

    return lug_selection, overlaps.__len__(), [f"{x}:{overlaps.get(x)}" for x in overlaps]


def inflate_lugs(lug_setting):
    """
    Inflates lug-settings in the short form like:
        "0-4*2 0-5*4 0-6*7 1-0*3 2-0*9 3-0 5-6"
    to the long form like:
        [0-4, 0-4, 0-5, 0-5, 0-5, 0-5, 0-6, 0-6, 0-6,
         0-6, 0-6, 0-6, 0-6, 1-0, 1-0, 1-0, 2-0, 2-0,
         2-0, 2-0, 2-0, 2-0, 2-0, 2-0, 2-0, 3-0, 5-6]
    :param lug_setting: lug-settings in short form.
    :return: lug-settings in long form.
    """

    lug_setting = sorted(lug_setting.split(' '))
    inflated_lug_setting = []
    for i, k in enumerate(lug_setting):
        k = k.split('*')

        if len(k) == 1:
            k.append('1')

        for _ in range(int(k[1])):
            inflated_lug_setting.append(k[0])

    return inflated_lug_setting


def deflate_lugs(lug_setting):
    """
    Deflates lug-settings in the long form like:
        [0-4, 0-4, 0-5, 0-5, 0-5, 0-5, 0-6, 0-6, 0-6,
         0-6, 0-6, 0-6, 0-6, 1-0, 1-0, 1-0, 2-0, 2-0,
         2-0, 2-0, 2-0, 2-0, 2-0, 2-0, 2-0, 3-0, 5-6]
    to the short form like:
        "0-4*2 0-5*4 0-6*7 1-0*3 2-0*9 3-0 5-6"
    :param lug_setting: lug-settings in long form.
    :return: lug-settings in short form.
    """

    lug_setting = Counter(lug_setting)
    deflated_lug_setting = []
    for lug in lug_setting.keys():
        if lug_setting[lug] > 1:
            deflated_lug_setting.append(f"{lug}*{lug_setting[lug]}")
        else:
            deflated_lug_setting.append(f"{lug}")

    return ' '.join(sorted(deflated_lug_setting))
