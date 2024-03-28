# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module contains routines to read & write key lists in config (aka INI)
file format.

In the config file format, multiple key lists are stored in one file. Each key
list is stored in a section named for its indicator. In this example, the file
contains settings for 2 key lists, one with indicator AA and one with indicator
YL.

[AA]
lugs = 0-4 0-5*4 0-6*6 1-0*5 1-2 1-5*4 3-0*3 3-4 3-6 5-6
wheel1 = FGIKOPRSUVWYZ
wheel2 = DFGKLMOTUY
wheel3 = ADEFGIORTUVX
wheel4 = ACFGHILMRSU
wheel5 = BCDEFJKLPS
wheel6 = EFGHIJLMNP
check = QLRRN TPTFU TRPTN MWQTV JLIJE J

[YL]
lugs = 1-0 2-0*4 0-3 0-4*3 0-5*2 0-6*11 2-5 2-6 3-4 4-5
wheel1 = BFJKLOSTUWXZ
wheel2 = ABDJKLMORTUV
wheel3 = EHJKNPQRSX
wheel4 = ABCHIJLMPQR
wheel5 = BCDGJLNOPQS
wheel6 = AEFHIJP
check = OZGPK AFVAJ JYRZW LRJEG MOVLU M

"""
import configparser
import random

from .key_list import KeyList

WHEELS = ['wheel{}'.format(n) for n in range(1, 7)]


def read_key_list(fname, indicator=None):
    """Reads key list information from the file given by fname.

    Searches the config file for the key list with the given indicator. If
    found, returns a KeyList object. Returns None if not found.

    If indicator is None, a key list is chosen from the file at random.

    """
    config = configparser.ConfigParser(interpolation=None)
    try:
        config.read(fname)
    except configparser.Error:
        return None

    if not config.sections():
        return None

    if indicator and indicator not in config.sections():
        return None
    elif indicator is None:
        # choose one at random
        indicator = random.choice(config.sections())

    section = config[indicator]
    return KeyList(
            indicator=indicator,
            lugs=section['lugs'],
            pin_list=[section[w] for w in WHEELS],
            letter_check=section['check'])


def write(fname, key_lists):
    """Writes the key lists to the file named fname in config file format.

    key_lists must be an iterable of KeyList objects.

    """
    config = configparser.ConfigParser(interpolation=None)

    for key_list in key_lists:
        config[key_list.indicator] = {}
        config[key_list.indicator]['lugs'] = key_list.lugs
        for n, wheel in enumerate(WHEELS):
            config[key_list.indicator][wheel] = key_list.pin_list[n]
        config[key_list.indicator]['check'] = key_list.letter_check

    with open(fname, 'w') as fp:
        config.write(fp)
