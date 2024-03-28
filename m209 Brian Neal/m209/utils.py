# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module contains various utility functions."""


def group_text(text, n=5):
    """Groups the given text into n-letter groups separated by spaces."""

    return ' '.join(''.join(text[i:i+n]) for i in range(0, len(text), n))
