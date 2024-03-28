# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module contains the key wheel related classes for the M209
simulation.

"""
import random

from . import M209Error


class KeyWheelError(M209Error):
    """Exception class for all key wheel errors"""
    pass


class KeyWheel:
    """Simulates a key wheel in a M209 converter"""

    def __init__(self, letters, guide_letter, effective_pins=None):
        """Initialize a KeyWheel instance:

        letters - an iterable of letters which appear on the wheel face

        guide_letter - must be a letter that appears within the letters
        parameter. It indicates which letter affects the guide arm when the
        first letter in letters is displayed to the operator.

        effective_pins - see the description of set_pins(), below.

        """
        self.letters = list(letters)
        self.num_pins = len(self.letters)

        self.letter_offsets = {letter : n for n, letter in enumerate(self.letters)}

        if self.num_pins < 1:
            raise KeyWheelError("Too few key wheel letters")

        # pin effectivity list:
        if effective_pins:
            self.set_pins(effective_pins)
        else:
            self.reset_pins()

        try:
            self.guide_offset = self.letter_offsets[guide_letter]
        except KeyError:
            raise KeyWheelError("Invalid guide_letter")

        # rotational position; 0 means first letter shown to operator
        self.pos = 0

    def __str__(self):
        parts = []
        for n, c in enumerate(self.letters):
            if self.pins[n]:
                parts.append(c + '-')
            else:
                parts.append('-' + c)
        return ' '.join(parts)

    def reset_pins(self):
        """Reset all pins to the ineffective state."""
        self.pins = [False] * self.num_pins
        self.effective_pins = ''

    def set_pins(self, effective_pins):
        """Sets which pins are effective.

        effective_pins - must be an iterable of letters whose pins are slid to
        the "effective" position (to the right). Letters not appearing in this
        sequence are considered to be in the "ineffective" position (to the
        left). If None or empty, all pins are set to be ineffective.

        """
        self.reset_pins()
        if not effective_pins:
            return

        for letter in effective_pins:
            try:
                n = self.letter_offsets[letter]
            except KeyError:
                raise KeyWheelError("Invalid pin: {}".format(letter))
            self.pins[n] = True

        self.effective_pins = effective_pins

    def rotate(self, steps=1):
        """Rotate the key wheel the given number of steps."""
        self.pos = (self.pos + steps) % self.num_pins

    def display(self):
        """Returns the letter shown to the operator based on the current key
        wheel position.

        """
        return self.letters[self.pos]

    def guide_letter(self):
        """Returns the letter of the pin that is in position to effect the guide
        arm. To check to see if this pin will effect the guide arm, call
        is_effective().

        """
        n = (self.pos + self.guide_offset) % self.num_pins
        return self.letters[n]

    def is_effective(self):
        """Returns True if the key wheel, in the current position, has a pin in
        the effective position, and False otherwise.

        """
        n = (self.pos + self.guide_offset) % self.num_pins
        return self.pins[n]

    def set_pos(self, c):
        """Sets the position of the key wheel to the letter c."""
        try:
            self.pos = self.letter_offsets[c]
        except KeyError:
            raise KeyWheelError("Invalid position {}".format(c))

    def set_random(self):
        """Sets the position of the key wheel to a random letter.

        The random letter is returned as a string.

        """
        c = random.choice(self.letters)
        self.set_pos(c)
        return c
