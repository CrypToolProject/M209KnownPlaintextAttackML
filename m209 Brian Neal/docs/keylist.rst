Key lists
---------

Key lists are represented as a named tuple called ``KeyList``.

.. class:: m209.keylist.KeyList(indicator, lugs, pin_list, letter_check)

   As a named tuple, ``KeyList`` has the following attributes:

   * ``indicator`` - the string name for the ``KeyList``; must be 2 letters in
     the range ``AA`` - ``ZZ``
   * ``lugs`` - a string representing the drum lug settings; see below
   * ``pin_list`` - a list of six strings which represent key wheel pin
     settings; see below
   * ``letter_check`` - a string representing the letter check used to verify
     operator settings; if unknown this can be ``None`` or an empty string
   
.. _lug-settings:

Lug settings format
~~~~~~~~~~~~~~~~~~~

Drum lug settings are often conveniently represented as strings consisting of
at most 27 whitespace-separated pairs of integers separated by dashes. For
example::

   lugs = '1-0 2-0 2-0 0-3 0-5 0-5 0-5 0-6 2-4 3-6'

Each integer pair must be in the form ``m-n`` where m & n are integers
between 0 and 6, inclusive. Each integer represents a lug position where
0 is a neutral position, and 1-6 correspond to key wheel positions. If
m & n are both non-zero, they cannot be equal.

If a string has less than 27 pairs, it is assumed all remaining bars have both
lugs in the neutral positions, i.e. ``0-0``.

The order of the pairs within the string does not matter.

To reduce typing and to aid in readability, an alternate shortcut notation is
supported::

   lugs = '1-0 2-0*2 0-3 0-5*3 0-6 2-4 3-6'

Any pair that is suffixed by ``*k``, where k is a positive integer, means there
are ``k`` copies of the preceeding lug pair combination. For example, these two
strings describe identical drum configurations::

   lugs1 = '2-4 2-4 2-4 0-1 0-1'
   lugs2 = '2-4*3 0-1*2'

.. _pin-settings:

Key wheel pin settings
~~~~~~~~~~~~~~~~~~~~~~

Key wheel pin settings are represented as iterables of letters whose pins are
slid to the "effective" position (to the right). Letters not appearing in this
sequence are considered to be in the "ineffective" position (to the left). If
None or empty, all pins are set to be ineffective.

Examples::

   all_ineffective = ''
   wheel1 = 'ABDEFHIJMQSUXZ'
   wheel2 = 'EINPQRTVXZ'
   wheel3 = 'DEFGIKNOSUX'
   wheel4 = 'BFGJKRS'
   wheel5 = 'ABCDFGHIJMPS'
   wheel6 = 'ADEFHIJKN'

Key list example
~~~~~~~~~~~~~~~~

An example of using the :class:`~m209.keylist.KeyList` is:

.. code-block:: python

   from m209.keylist import KeyList

   key_list1 = KeyList(
          indicator='AA',
          lugs='0-4 0-5*4 0-6*6 1-0*5 1-2 1-5*4 3-0*3 3-4 3-6 5-6',
          pin_list=[
              'FGIKOPRSUVWYZ',
              'DFGKLMOTUY',
              'ADEFGIORTUVX',
              'ACFGHILMRSU',
              'BCDEFJKLPS',
              'EFGHIJLMNP'
          ],
          letter_check='QLRRN TPTFU TRPTN MWQTV JLIJE J')

Key list file I/O
~~~~~~~~~~~~~~~~~

Key lists can be stored in files in config file ("INI") style format using
functions found in the ``m209.keylist.config`` module.

.. function:: m209.keylist.config.read_key_list(fname[, indicator=None])

    Reads key list information from the file given by ``fname``.

    Searches the config file for the key list with the given indicator. If
    found, returns a :class:`~m209.keylist.KeyList` object. Returns ``None`` if
    not found.

    If ``indicator`` is ``None``, a key list is chosen from the file at random.

.. function:: m209.keylist.config.write(fname, key_lists)

    Writes the key lists to the file named ``fname`` in config file format.

    ``key_lists`` must be an iterable of :class:`~m209.keylist.KeyList` objects.

.. _key-list-file-format-label:

Key list file format
~~~~~~~~~~~~~~~~~~~~

An example key list file in config file format is presented below. The label
for each section of the file is the key list indicator.

::

   [CA]
   lugs = 0-5*5 0-6*2 1-0*7 1-2 1-3*3 1-6 2-0 3-0*3 3-5*2 3-6 4-5
   wheel1 = ABCDFGHJLOPRVWYZ
   wheel2 = BCDEIJKPQSUVX
   wheel3 = ACDGLNQRSTUV
   wheel4 = FGHIJNQRSU
   wheel5 = DEIJOQS
   wheel6 = BCDEILMNOP
   check = RGPRO RTYOO TWYSN GXTPF PNWIH P

   [CD]
   lugs = 0-4*4 0-5 1-0*7 1-2*2 1-4*3 2-0*2 2-4*2 2-6*2 3-0*4
   wheel1 = AEFHIKMPQRSUVZ
   wheel2 = ABFGHINORSUVZ
   wheel3 = BDEHJKLMNOQRSU
   wheel4 = CDEFGHJKMRU
   wheel5 = FGHIJOQS
   wheel6 = EGIJKLP
   check = ZRLWL YRMIZ RZOPN UWMVZ DVGPM H

Generating key lists
~~~~~~~~~~~~~~~~~~~~

The ``m209`` library contains a function to pseudo-randomly generate a key list
that is based on the procedure described in the 1944 M-209 manual
(see :ref:`references-label` [4]).

.. function:: m209.keylist.generate.generate_key_list(indicator[, lug_selection=None[, max_lug_attempts=MAX_LUG_ATTEMPTS[, max_pin_attempts=MAX_PIN_ATTEMPTS]]])

   The only required parameter is ``indicator``, the two-letter indicator for
   the key list.

   If successful, a :class:`~m209.keylist.KeyList` object is returned.

   If a :class:`~m209.keylist.KeyList` could not be generated
   a ``KeyListGenError`` exception is raised.

   The algorithm is heuristic-based and makes random decisions based upon the
   1944 procedure. The actual procedure is loosely specified in the manual, and
   much is left up to the human operator. It is possible that the algorithm
   cannot find a solution to meet the key list requirements specified in the
   manual, in which case it simply tries again up to some set of limits. These
   limits can be tweaked using the optional parameters to the algorithm. If no
   solution is found after exhausting the limits, a ``KeyListGenError`` is
   raised.

   The optional parameters are:

   * ``lug_selection`` - a list of 6 integers used to drive the lug settings
     portion of the algorithm. If not supplied, a list of 6 integers is chosen
     from data tables that appear in the 1944 manual. For more information on
     the requirements for these integers, see the manual.

   * ``max_lug_attempts`` - the maximum number of times to attempt to create
     lug settings before giving up

   * ``max_pin_attempts`` - the maximum number of times to attempt to generate
     key wheel pin settings before giving up

