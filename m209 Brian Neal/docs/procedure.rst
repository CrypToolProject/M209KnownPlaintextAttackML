StdProcedure Class
==================

The ``StdProcedure`` class encapsulates the encrypting and decrypting
procedures outlined in :ref:`references-label`. In particular, see
references [5] and [7]. This class takes care of the high level details of
inserting various message indicators into an encrypted message, and stripping
them off during decrypt. These message indicators tell the recipient what key
list and initial key wheel settings to use when configuring their M-209 for
decrypt.

.. class:: m209.procedure.StdProcedure([m_209=None[, key_list=None]])

   :param m_209: an instance of a :class:`~m209.converter.M209` can optionally be
      provided to the procedure object. If ``None`` the procedure object
      will create one for internal use.
   :param key_list: an instance of a :class:`~m209.keylist.KeyList` can be
      provided if known ahead of time. Before an encrypt or decrypt operation
      can be performed, a key list must be provided. This can be done after
      object creation via :meth:`set_key_list`. Note that the ``letter_check``
      attribute of the :class:`~m209.keylist.KeyList` is not accessed by the
      procedure object, and can be ``None`` if not known.

Before an :meth:`encrypt` operation can be performed, a valid key list must be
installed, either during procedure object construction, or by the
:meth:`set_key_list` method.

Decrypt operations are performed in a 3-step process.

#. First, a call to the :meth:`set_decrypt_message` method passes the message
   to be decrypted to the procedure and establishes the parameters to be used
   for the actual :meth:`decrypt` operation. These decrypt parameters are
   returned to the caller.

#. The caller can examine the decrypt parameters to determine which key list
   must be installed before a successful :meth:`decrypt` operation can be
   carried out. The caller may call :meth:`get_key_list` to examine the
   currently installed key list. It is up to the caller to obtain the required
   key list and install it with :meth:`set_key_list`, if necessary. This is
   done by ensuring the installed key list indicator matches the
   ``key_list_ind`` field of the decrypt parameters.

#. Finally :meth:`decrypt` can be called. If the procedure does not have the
   key list necessary to decrypt the message, a ``ProcedureError`` is
   raised.

``StdProcedure`` objects have the following methods:

   .. method:: get_key_list()

      :returns: the currently installed :class:`~m209.keylist.KeyList` object
         or ``None`` if one has not been set

   .. method:: set_key_list(key_list)

      Establishes the :class:`~m209.keylist.KeyList` to be used for future
      :meth:`encrypt` and :meth:`decrypt` operations

      :param key_list: the new :class:`~m209.keylist.KeyList` to use

   .. method:: encrypt(plaintext[, spaces=True[, ext_msg_ind=None[, sys_ind=None]]])
      :noindex:

      Encrypts a plaintext message using the installed
      :class:`~m209.keylist.KeyList` and by following the standard procedure.
      The encrypted text with the required message indicators are returned as
      a string.

      :param plaintext: the input string to be encrypted
      :param spaces: if ``True``, space characters in the input plaintext are
         allowed and will be replaced with ``Z`` characters before encrypting
      :param ext_msg_ind: this is the external message indicator, which, if
         supplied, must be a valid 6-letter string of key wheel settings. If not
         supplied, one will be generated randomly.
      :param sys_ind: this is the system indicator, which must be a string of length
         1 in the range ``A`` - ``Z``, inclusive. If ``None``, one is chosen at random.
      :returns: the encrypted text with the required message indicators
      :raises ProcedureError: if the procedure does not have
         a :class:`~m209.keylist.KeyList` or the input indicators are invalid
         
   .. method:: set_decrypt_message(msg)

      Prepare to decrypt the supplied message.

      :param msg: the messsage to decrypt. The message can be grouped into
         5-letter groups separated by spaces or accepted without spaces.
      :returns: a ``DecryptParams`` named tuple to the caller (see below)
      
      The ``DecryptParams`` named tuple has the following attributes:

      * ``sys_ind`` - the system indicator
      * ``ext_msg_ind`` - the external message indicator
      * ``key_list_ind`` - the key list indicator
      * ``ciphertext`` - the cipher text with all indicators removed

      The caller should ensure the procedure instance has the required
      :class:`~m209.keylist.KeyList` before calling :meth:`decrypt`. The
      ``key_list_ind`` attribute of the returned ``DecryptParams`` named tuple
      identifies the key list that should be installed with
      :meth:`set_key_list`.

   .. method:: decrypt()
      :noindex:

      Decrypt the message set in a previous :meth:`set_decrypt_message` call. The
      resulting plaintext is returned as a string.

      :returns: the decrypted plaintext as a string
      :raises ProcedureError: if the procedure instance has not been
         previously configured with the required :class:`~m209.keylist.KeyList`
         via :meth:`set_key_list`

Here is a simple interactive example of performing an encrypt operation. Here
we choose a random key list from our key list file, and use random indicators:

>>> from m209.keylist.config import read_key_list
>>> from m209.procedure import StdProcedure
>>> 
>>> key_list = read_key_list('m209keys.cfg')
>>> proc = StdProcedure(key_list=key_list)
>>> ct = proc.encrypt('ORDER THE PIZZA AT TWELVE HUNDRED HOURS')
>>> ct
'YYGBM ENNHT VBMTJ PEEFV JWLUU PAFTS VOHEA QEPEQ OKVUA XDAUX YYGBM ENNHT'
>>>

The first and last two groups of this message contain the indicators. Here we
can see the system indicator was ``Y``, the external message indicator is
``GBMENN``, and the key list indicator is ``HT``.

An example session for decrypting the above message might look like:

>>> proc = StdProcedure()
>>> ct = 'YYGBM ENNHT VBMTJ PEEFV JWLUU PAFTS VOHEA QEPEQ OKVUA XDAUX YYGBM ENNHT'
>>> params = proc.set_decrypt_message(ct)
>>> params
DecryptParams(sys_ind='Y', ext_msg_ind='GBMENN', key_list_ind='HT', ciphertext='VBMTJ PEEFV JWLUU PAFTS VOHEA QEPEQ OKVUA XDAUX')
>>> key_list = read_key_list('m209keys.cfg', params.key_list_ind)
>>> proc.set_key_list(key_list)
>>> pt = proc.decrypt()
>>> pt
'ORDER THE PI  A AT TWELVE HUNDRED HOURS '
>>> 

