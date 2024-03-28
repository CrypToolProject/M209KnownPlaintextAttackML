# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module defines the KeyList class and related functions"""

import collections
import re


VALID_IND_RE = re.compile('^[A-Z]{2}$')


KeyList = collections.namedtuple('KeyList',
                ['indicator', 'lugs', 'pin_list', 'letter_check'])


def valid_indicator(indicator):
    """Returns True if the given indicator is valid and False otherwise."""
    return True if VALID_IND_RE.match(indicator) else False


class IndicatorIter:
    """Iterator class for key list indicators AA-ZZ"""

    MAX_N = 26 ** 2

    def __init__(self, start='AA'):
        if not valid_indicator(start):
            raise ValueError('invalid key list indicator')
        self.n = (ord(start[0]) - ord('A')) * 26 + ord(start[1]) - ord('A')

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.MAX_N:
            x, y = self.n // 26, self.n % 26
            s = chr(x + ord('A')) + chr(y + ord('A'))
            self.n += 1
            return s
        raise StopIteration

    def __len__(self):
        """Returns how many indicators are available"""
        return self.MAX_N - self.n

