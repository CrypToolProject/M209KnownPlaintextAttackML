Command-line Reference
======================

Overview
--------

The ``m209`` command-line utility performs three functions:

* Creates key list files
* Encrypts text, either given on the command line or read from a file
* Decrypts text, either given on the command line or read from a file
 
These functions are implemented as sub-commands. To see the list of
sub-commands and options common to all sub-commands, use the ``-h`` or
``--help`` option::

   $ m209 --help
   usage: m209 [-h] [-l {debug,info,warning,error,critical}]
               {encrypt,enc,decrypt,dec,keygen,key} ...

   M-209 simulator and utility program

   optional arguments:
     -h, --help            show this help message and exit
     -l {debug,info,warning,error,critical}, --log {debug,info,warning,error,critical}
                           set log level [default: warning]

   list of commands:
     type m209 {command} -h for help on {command}

     {encrypt,enc,decrypt,dec,keygen,key}
       encrypt (enc)       encrypt text from file or command-line
       decrypt (dec)       decrypt text from file or command-line
       keygen (key)        generate key list

The ``-l`` / ``--log`` options control the verbosity of output. Currently only
the ``keygen`` sub-command makes use of this option.

Each sub-command has an alias for those who prefer shorter commands.

Keygen sub-command
------------------

``keygen``, or ``key`` for short, is the sub-command that pseudo-randomly
creates key list files for use by the ``encrypt`` and ``decrypt`` sub-commands,
as well as by the ``m209`` library routines. 

Help on the ``keygen`` sub-command can be obtained with the following
invocation::

   $ m209 keygen --help
   usage: m209 keygen [-h] [-z KEY_FILE] [-o] [-s XX] [-n NUMBER]

   Generate key list file

   optional arguments:
     -h, --help            show this help message and exit
     -z KEY_FILE, --key-file KEY_FILE
                           path to key list file [default: m209keys.cfg]
     -o, --overwrite       overwrite key list file if it exists
     -s XX, --start XX     starting indicator; if omitted, random indicators are
                           used
     -n NUMBER, --number NUMBER
                           number of key lists to generate [default: 1]

The options for ``keygen`` are described below.

``-z`` or ``--key-file``
   This option names the key list file. If not supplied, this defaults to
   ``m209keys.cfg``. Note that the other sub-commands also have this option,
   and they too use the same default value.

``-o`` or ``--overwrite``
   This switch must be present if the key list file already exists. It provides
   confirmation that the user wants to overwrite an existing file. If the key
   list file already exists, and this option is not supplied, this sub-command
   will exit with an error message and the original key list file will be
   unchanged.

``-s`` or ``--start``
   This option sets the starting indicator for the key list file. Key list
   indicators are two letters in the range ``AA`` to ``ZZ``. For example,
   ``keygen`` can be told to create 3 key lists, starting with indicator
   ``AA``.  In this case the key lists ``AA``, ``AB``, and ``AC`` would be
   written to the file. If this parameter is omitted, ``keygen`` picks
   indicators at random. Key list indicators simply name the key list, and are
   placed in the leading and trailing groups of encrypted messages to tell the
   receiver which key list was used to create the message. Both sender and
   receiver must have the same key list (name and contents) to communicate.

``-n`` or ``--number``
   This option specifies the number of key lists to generate. The default value
   is 1.

.. NOTE:: 

   The algorithm the ``keygen`` sub-command uses to generate key lists is based
   on the actual US Army procedure taken from the 1944 manual. This procedure
   is somewhat loosely specified and a lot is left up to the soldier creating
   the key list. The ``keygen`` algorithm is ad-hoc and uses simple heuristics
   and random numbers to make decisions.  Occasionally this algorithm may fail
   to generate a key list that meets the final criteria defined in the manual.
   If this happens an error message will be displayed and no key list file will
   be created. It is suggested to simply run the command again as it is not
   likely to happen twice in a row.

Keygen examples
+++++++++++++++

To generate 30 key lists in the default key list file (``m209keys.cfg``) with
random indicators, and overwriting the key list file if it exists::

   $ m209 keygen -o -n 30
   $ m209 key --overwrite --number=30

To generate 5 key lists that sequentially start with the indicator ``BN`` in
the key list file ``m209/keys/november/keys.cfg``::

   $ m209 keygen -z m209/keys/november/keys.cfg -s BN -n 5


Encrypt sub-command
-------------------

``encrypt``, or ``enc``, is the sub-command used to encrypt text. To get help
on the ``encrypt`` command, type the following::

   $ m209 encrypt -h
   usage: m209 encrypt [-h] [-z KEY_FILE] [-f FILE] [-t TEXT] [-k XX] [-e ABCDEF]
                       [-s S]

   Encrypt text from a file or command-line

   optional arguments:
     -h, --help            show this help message and exit
     -z KEY_FILE, --key-file KEY_FILE
                           path to key list file [default: m209keys.cfg]
     -f FILE, --file FILE  path to plaintext file or - for stdin
     -t TEXT, --text TEXT  text string to encrypt
     -k XX, --key-list-ind XX
                           2-letter key list indicator; if omitted a random one
                           is used
     -e ABCDEF, --ext-ind ABCDEF
                           6-letter external message indicator; if omitted a
                           random one is used
     -s S, --sys-ind S     1-letter system indicator; if omitted a random one is
                           used

   Either the -f/--file or -t/--text arguments must be supplied

The options to the ``encrypt`` command are described below.

``-z`` or ``--key-file``
   This option names the key list file. If not given, the default of
   ``m209keys.cfg`` is used.

``-f`` or ``--file``
   This option specifies the file that contains the text to encrypt. If the
   filename is given as ``-`` then input is read directly from ``stdin``. Note
   that either this option or the ``-t`` option must be specified, but not
   both.

``-t`` or ``--text``
   This option specifies the text to encrypt on the command-line. Depending
   upon your system, you'll probably have to quote or escape your text. Note
   that you must either specify this option or the ``-f`` option, but not both.

``-k`` or ``--key-list-ind``
   This option specifies the two-letter key list indicator to use. Valid values
   range from ``AA`` to ``ZZ``. The key list with this indicator must be in the
   key list file given by the ``-z`` option. If this option is omitted, a key
   list from the key list file is chosen at random.

``-e`` or ``--ext-ind``
   This option specifies the six-letter external message indicator, which is an
   encryption parameter as explained in the 1944 manual (see
   :ref:`references-label` [5] & [7]). Each letter must exist on the key wheels
   from left to right. If this option is omitted, an external message indicator
   is chosen at random.

``-s`` or ``--sys-ind``
   This option specifies the one-letter system indicator, which is an
   encryption parameter as explained in the 1944 manual (see 
   :ref:`references-label` [5] & [7]). This must be a letter from ``A`` to ``Z``.
   If not given, one is chosen at random.

.. NOTE:: 

   An actual M-209 can only accept the letters ``A-Z``. When using an actual
   M-209, space characters must be input as the letter ``Z``. Numbers must
   typically be spelled out as words or some other agreed-upon convention.
   Likewise with punctuation. To make encryption more convenient, the ``m209``
   program will accept spaces and automatically convert them to the letter
   ``Z``. Lowercase letters will automatically be converted to uppercase. All
   other characters will be silently dropped from the input. This applies to
   both text read on the command-line with the ``-t`` option and text read from
   files (``-f``).

Encrypt examples
++++++++++++++++

To encrypt a simple string on the command-line using the default key file and
random encryption parameters::

   $ m209 encrypt -t "Rendezvous at zero seven thirty"
   BBEPH SSLBY RKHWO OBAJB VYQEQ NJHGV FWRCJ UZHMB PXXXX BBEPH SSLBY

To save the encrypted text to a file::

   $ m209 encrypt -t "Rendezvous at zero seven thirty" > secret.txt

To read the contents of a file and encrypt it, saving it to a new file::

   $ m209 enc -f message.txt > secret.txt

To explicitly specify encryption parameters, and read text from ``stdin``::

   $ cat message.txt | m209 enc --file=- -k SU -e ZQGMFO -s A 


Decrypt sub-command
-------------------

``decrypt``, or ``dec``, is the sub-command used to decrypt text. To get help
on the ``decrypt`` command, type the following::

   $ m209 decrypt --help
   usage: m209 decrypt [-h] [-z KEY_FILE] [-f FILE] [-t TEXT]

   Decrypt text from a file or command-line

   optional arguments:
     -h, --help            show this help message and exit
     -z KEY_FILE, --key-file KEY_FILE
                           path to key list file [default: m209keys.cfg]
     -f FILE, --file FILE  path to ciphertext file or - for stdin
     -t TEXT, --text TEXT  text string to decrypt

   Either the -f/--file or -t/--text arguments must be supplied

The options to the ``decrypt`` command are described below.

``-z`` or ``--key-file``
   This option names the key list file. If not given, the default of
   ``m209keys.cfg`` is used.

``-t`` or ``--file``
   This option specifies the file that contains the text to decrypt. If the
   filename is given as ``-`` then input is read directly from ``stdin``. Note
   that either this option or the ``-t`` option must be specified, but not
   both.

``-t`` or ``--text``
   This option specifies the text to decrypt on the command-line. Depending
   upon your system, you'll probably have to quote or escape your text. Note
   that you must either specify this option or the ``-f`` option, but not both.

.. NOTE::

   The first and last 2 groups of an encrypted message contain the information
   needed to decrypt the message: the system indicator, the external message
   indicator, and the key list indicator. If the key list file given to the
   decrypt command does not contain the key list used to encrypt the message,
   then the message cannot be decrypted and an error message will be displayed.

Decrypt examples
++++++++++++++++

To decrypt a simple string on the command-line using the default key file::

   $ m209 decrypt -t "BBEPH SSLBY RKHWO OBAJB VYQEQ NJHGV FWRCJ UZHMB PXXXX BBEPH SSLBY"
   RENDE VOUS AT  ERO SEVEN THIRTYXSJQ

To save the decrypted text to a file::

   $ m209 decrypt -t "BBEPH SSLBY RKHWO OBAJB VYQEQ NJHGV FWRCJ UZHMB PXXXX BBEPH SSLBY" > msg.txt

To read the contents of a file and decrypt it, saving it to a new file::

   $ m209 dec -f secret.txt > msg.txt

To decrypt from ``stdin``::

   $ cat secret.txt | m209 dec -f -
   RENDE VOUS AT  ERO SEVEN THIRTYXSJQ


.. NOTE::

   In this example, the last group of the encrypted message only has one
   letter. It was padded out to five letters with ``X``'s by the encryption
   process, and thus four "garbage" letters appear at the end in the decrypted
   output.

   Note also that the ``Z`` in ``RENDEZVOUS`` and ``ZERO`` were converted to
   spaces by the decrypt process.

   In both of these cases the operator would have to "fix up" the message
   before passing it up the chain of command.
