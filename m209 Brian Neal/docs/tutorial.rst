Tutorials
=========

Command-line Tutorial
---------------------

In order for two parties to exchange M-209 messages, each must set up their
device in exactly the same manner. This was accomplished by publishing key
lists in code books which were distributed to end users. A code book instructed
users on what key list to use on any given day in a given month.  Each key list
detailed the numerous wheel pin and lug settings that needed to be made for
a given day. Because there are so many settings, the ``m209`` utility allows
users to store key lists in a key file for convenience. So let us first create
a key file that holds 30 key lists::

   $ m209 keygen -n 30

This command randomly creates 30 key lists and stores them in a file called
``m209keys.cfg`` by default. We did not specify a starting key list indicator, so
30 random ones were chosen. The first 13 lines of our new key file are
displayed below::

   $ head -n 13 m209keys.cfg 
   [AB]
   lugs = 0-4*4 0-5*6 1-0*10 2-0*2 3-0 3-5*2 3-6 4-5
   wheel1 = BDFGIKRSTUWX
   wheel2 = BCEJKLORSUX
   wheel3 = CFHJKLMQSTU
   wheel4 = ABCDHIJMOPRTU
   wheel5 = BCEFINPS
   wheel6 = ACDEHJN
   check = GZWUU SFYQN NFAKK FXSEN FAFMF B

   [AK]
   lugs = 0-4*2 0-5*9 0-6 1-0*3 1-2 1-5 1-6*2 3-0*8
   wheel1 = ABDEFHIJMQSUXZ

.. NOTE:: 
   If you are following along at home, you'll probably get different
   output than what is shown here. This is because the key lists are generated
   at random, and it is very unlikely that your key list will match mine!

Here we can see that the first key list in our file has the indicator ``AB``
(shown in square brackets), and we can see the settings for the lugs and six
wheels. This notation is explained later (see :ref:`key-list-file-format-label`).
Also included is a so-called check string. Because there are so many settings,
it is quite error-prone to set up an M-209. This check string allows the
operator to verify their work.  After configuring the M-209 with the given
settings, the operator can set the six key wheels to ``AAAAAA``, then encipher
the letter ``A`` 26 times. If the message that appears on the paper tape
matches the check string, the operator knows the machine is set up correctly
for the day.

After the key list ``AB``, the key list ``AK`` starts, and so on for all 30 key
lists.

Now that we have created a key file, we can encrypt our first message. The
``m209`` utility has many options to let you have fine control over the various
encryption parameters. These are explained in detail later. If you omit these
parameters they are simply chosen at random. Here is the simplest example of
encrypting a message::

   $ m209 encrypt -t "THE PIZZA HAS ARRIVED STOP NO SIGN OF ENEMY FORCES STOP"
   IIPDU FHLMB LASGD KTLDO OSRMZ PWGEB HYMCB IKSPT IUEPF FUHEO NQTWI VTDPC GSPQX IIPDU FHLMB

What just happened here? Since we did not specify a key file, the default
``m209keys.cfg`` was used. Since we did not specify a key list indicator, one
was chosen randomly from the key file. Other encryption parameters, explained
later, were also randomly chosen. Next, the message given on the command-line
was encrypted using the standard US Army procedure described in
:ref:`references-label` (see [5] and [7]). This resulted in the encrypted
message, which is displayed in 5-letter groups.  Notice that the first and last
2 groups are identical. These are special indicators that tell the receiver how
to decrypt the message. In particular note that the last 2 letters in the
second and last groups are ``MB``. This is the key list indicator and tells
the receiver what key list was used. The remaining groups in the middle make
up the encrypted message.

Astute M-209 enthusiasts will note that our message included spaces. Actual
M-209 units only allow the input of the letters ``A`` through ``Z``. Whenever
a space was needed, the operator inserted the letter ``Z``. The ``m209``
utility automatically performs this substitution for convenience.

Let's suppose our message was then sent to our recipient, either by courier,
Morse code over radio, or in the modern age, email or even Twitter. In order
for our receiver to decrypt our message they must also have the identical key
list named ``MB``. We will assume for now that our key file, ``m209keys.cfg``
was sent to our receiver earlier in some secure manner. The receiver then
issues this command::

   $ m209 decrypt -t "IIPDU FHLMB LASGD KTLDO OSRMZ PWGEB HYMCB IKSPT IUEPF FUHEO NQTWI VTDPC GSPQX IIPDU FHLMB"
   THE PI  A HAS ARRIVED STOP NO SIGN OF ENEMY FORCES STOP

Here again, since no key file was explicitly specified, the file
``m209keys.cfg`` was used. The file was searched for the key list ``MB``. Then
the standard Army procedure was followed, making use of the indicator groups to
decrypt the message, which is displayed as output.

But wait, what happened to our Pizza? Why are the ``Z``'s missing? This is how
an actual M-209 operates. Recall that an operator must substitute a letter
``Z`` whenever a space is needed. The M-209 helpfully replaces the letter ``Z``
in the decrypt output with a space as an aid to the operator. As a side effect,
legitimate uses of the letter ``Z`` are blanked out. Usually it is clear from
context what has happened, and the operator has to put the ``Z``'s back into
the message before passing it up the chain of command.

It may also happen that the original message did not fit perfectly into an even
number of 5-letter groups. In that case the encrypted message would be padded
with ``X`` characters according to procedure. Upon decrypt, these ``X``
characters would appear as garbage characters on the end of the message. The
receiving operator would simply ignore these letters. Note that our message did
not exhibit this behavior.

This is all you need to know to start creating your own M-209 messages! For
more details, consult the :doc:`commandline`.

Library Tutorial
----------------

Here is one way to perform the encrypt and decrypt operations from the
command-line tutorial, above. In order to produce the same output, we explicitly
specify the encryption parameters: the key list, the external message
indicator, and the system indicator. These parameters are explained in
:ref:`references-label` [5] & [7].

.. literalinclude:: ../examples/encrypt.py

This program outputs::

   IIPDU FHLMB LASGD KTLDO OSRMZ PWGEB HYMCB IKSPT IUEPF FUHEO NQTWI VTDPC GSPQX IIPDU FHLMB

A decrypt is just a bit more complicated. After constructing
a :class:`~m209.procedure.StdProcedure` object, you hand it the encrypted
message to analyze. The procedure object examines the groups in the message and
extracts all the indicators. These are returned as a ``DecryptParams`` named
tuple which indicates, amongst other things, what key list is required. It is
then up to you to obtain this key list somehow. Here we use the
:func:`~m209.keylist.config.read_key_list` function to do so. After installing
the key list into the procedure object with :meth:`~.StdProcedure.set_key_list`,
you can finally call :meth:`~.StdProcedure.decrypt`:

.. literalinclude:: ../examples/decrypt.py

This program prints::

   THE PI  A HAS ARRIVED STOP NO SIGN OF ENEMY FORCES STOP
