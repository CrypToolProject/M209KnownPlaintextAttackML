# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module contains important key wheel data that makes our simulation
historically accurate and thus interoperable with actual M-209 units.

"""

# This list contains a 2-tuple for each key wheel in an M-209, in order from
# left to right as an operator faces the machine.
# The first element of each tuple is an iterable of letters for that wheel.
# The second element is the letter whose pin interacts with the guide arm when
# the letter "A" is being displayed to the operator.
#
# This information was taken from Wikipedia [1] and is understood to be
# unclassified at this point in time. :-)
#
# [1]: http://en.wikipedia.org/wiki/M-209

KEY_WHEEL_DATA = [
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "P"),
    ("ABCDEFGHIJKLMNOPQRSTUVXYZ", "O"),
    ("ABCDEFGHIJKLMNOPQRSTUVX", "N"),
    ("ABCDEFGHIJKLMNOPQRSTU", "M"),
    ("ABCDEFGHIJKLMNOPQRS", "L"),
    ("ABCDEFGHIJKLMNOPQ", "K"),
]

assert(len(KEY_WHEEL_DATA[0][0]) == 26)
assert(len(KEY_WHEEL_DATA[1][0]) == 25)
assert(len(KEY_WHEEL_DATA[2][0]) == 23)
assert(len(KEY_WHEEL_DATA[3][0]) == 21)
assert(len(KEY_WHEEL_DATA[4][0]) == 19)
assert(len(KEY_WHEEL_DATA[5][0]) == 17)
