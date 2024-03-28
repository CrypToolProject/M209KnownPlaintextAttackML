# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module contains the encrypt & decrypt procedures as described in "War
Department, Official Training Film, T.F. 11 - 1400, Army, Service Forces."
A YouTube playlist of this film can be found here:

http://www.youtube.com/playlist?list=PLCPgncK_sTnEny2-uoTV-1_GC72zo-vKq

This procedure is also described on Mark J. Blair's pages:

http://www.nf6x.net/2013/04/practical-use-of-the-m-209-cipher-machine-chapter-4/
http://www.nf6x.net/2013/04/practical-use-of-the-m-209-cipher-machine-chapter-5/

If other procedures are discovered, this module can be expanded to a package and
the new procedures can be added as different modules. For now, this is the only
procedure known to the author.

"""
from collections import namedtuple
import random
import re

from . import M209Error
from .converter import M209, M209_ALPHABET_SET, M209_ALPHABET_LIST
from .key_wheel import KeyWheelError
from .utils import group_text


class ProcedureError(M209Error):
    pass


DecryptParams = namedtuple('DecryptParams',
                    ['sys_ind', 'ext_msg_ind', 'key_list_ind', 'ciphertext'])


MSG_RE = re.compile(r'^([A-Z]{5}) ([A-Z]{5}) ((?:[A-Z]{5} )+)\1 \2$')


class StdProcedure:
    """This class encapsulates the "standard" encrypt/decrypt procedure for the
    M-209 as found in the training film T.F. 11 - 1400.

    The procedure can be configured with an optional M-209, and optional key
    list to be used for the day. If the M-209 is not supplied, one will be
    created internally. Before an encrypt() operation can be performed, a key
    list must be supplied. This can be done at construction time or via the
    set_key_list() method.

    To perform a decrypt operation, a 3-step process must be used:
        1) Call set_decrypt_message(msg) - this passes the message to be
           decrypted to the procedure and establishes the parameters to be used
           for the actual decrypt() operation. These decrypt parameters are
           returned to the caller.
        2) The caller can examine the decrypt parameters to determine which key
           list must be installed before a successful decrypt() operation can be
           carried out. The caller may call get_key_list() to examine the
           current key list. It is up to the caller to obtain the required key
           list and install it with set_key_list(), if necessary. This is done
           by ensuring the installed key list indicator matches the key_list_ind
           field of the decrypt parameters.
        3) Finally decrypt() can be called. If the procedure does not have the
           key list necessary to decrypt the message, a ProcedureError is
           raised.

    """
    def __init__(self, m_209=None, key_list=None):
        self.m_209 = m_209 if m_209 else M209()
        self.decrypt_params = None

        if key_list:
            self.set_key_list(key_list)
        else:
            self.key_list = None

    def get_key_list(self):
        """Returns the currently installed key list object or None if one has
        not been set.

        """
        return self.key_list

    def set_key_list(self, key_list):
        """Use the supplied key list for all future encrypt/decrypt operations.

        Configure the M209 with the key list parameters.

        """
        if len(key_list.indicator) != 2:
            raise ProcedureError("invalid key list indicator")

        self.key_list = key_list
        self.m_209.set_drum_lugs(key_list.lugs)
        self.m_209.set_all_pins(key_list.pin_list)

    def encrypt(self, plaintext, spaces=True, ext_msg_ind=None, sys_ind=None, int_msg_ind=None):
        """Encrypts a plaintext message using standard procedure. The encrypted text
        with the required message indicators are returned as one string.

        The encrypt function accepts these parameters:

        plaintext - Input string of text to be encrypted
        spaces - If True, space characters in the input plaintext will automatically
            be replaced with 'Z' characters before encrypting.
        ext_msg_ind - This is the external message indicator, which, if supplied,
            must be a valid 6 letter string of key wheel settings. If not supplied,
            one will be generated randomly.
        sys_ind - This is the system indicator, which must be a string of length
            1 in the range 'A'-'Z', inclusive. If None, one is chosen at random.

        A ProcedureError will be raised if the procedure does not have a key
        list to work with.

        """
        # Ensure we have a key list indicator and there is no ambiguity:

        if not self.key_list:
            raise ProcedureError("encrypt requires a key list")

        self.m_209.letter_counter = 0

        # Set key wheels to external message indicator
        if ext_msg_ind:
            try:
                self.m_209.set_key_wheels(ext_msg_ind)
            except M209Error as ex:
                raise ProcedureError(
                    "invalid external message indicator {} - {}".format(ext_msg_ind, ex))
        else:
            ext_msg_ind = self.m_209.set_random_key_wheels()

        # Ensure we have a valid system indicator
        if sys_ind and sys_ind not in M209_ALPHABET_SET:
            raise ProcedureError("invalid system indicator {}".format(sys_ind))
        elif sys_ind is None:
            sys_ind = random.choice(M209_ALPHABET_LIST)

        # Generate internal message indicator.

        if int_msg_ind is None:
            int_msg_ind = self.m_209.encrypt(sys_ind * 12, group=False)

        self.m_209.letter_counter = 0

        # Set the key wheels to the internal message indicator
        self._set_int_message_indicator(int_msg_ind)

        # Now encipher the message on the M209
        ciphertext = self.m_209.encrypt(plaintext, group=True, spaces=spaces)

        # If the final group in the ciphertext has less than 5 letters, pad with
        # X's to make a complete group:

        i = ciphertext.rfind(' ')
        if i != -1:
            x_count = 6 - (len(ciphertext) - i)
        else:   # only 1 group
            x_count = 5 - len(ciphertext)

        if x_count:
            ciphertext = ciphertext + 'X' * x_count

        # Add the message indicators to pad each end of the message

        pad1 = sys_ind * 2 + ext_msg_ind[:3]
        pad2 = ext_msg_ind[3:] + self.key_list.indicator

        msg_parts = [pad1, pad2, ciphertext, pad1, pad2]

        # Assemble the final message
        return ' '.join(msg_parts)

    def set_decrypt_message(self, msg):
        """Prepare to decrypt the supplied message.

        The messsage can be grouped into 5-letter groups separated by spaces or
        accepted without spaces.

        Returns a DecryptParams tuple to the caller. The caller should ensure
        the procedure instance has the required key list before calling decrypt.

        """
        # See if we need to group the message.
        if ' ' not in msg:
            msg = group_text(msg)

        # Perform some basic checks on the message to see if it looks like an
        # M209 message.

        # Ensure the message passes a regex format check
        m = MSG_RE.match(msg)
        if not m:
            raise ProcedureError("invalid decrypt message format")

        group1 = m.group(1)
        group2 = m.group(2)

        # Check system indicator is repeated twice
        if group1[0] != group1[1]:
            raise ProcedureError("missing system indicator")

        sys_ind = group1[0]
        ext_msg_ind = group1[2:] + group2[:3]
        key_list_ind = group2[3:]
        ciphertext = m.group(3).rstrip()

        self.decrypt_params = DecryptParams(sys_ind=sys_ind,
                                    ext_msg_ind=ext_msg_ind,
                                    key_list_ind=key_list_ind,
                                    ciphertext=ciphertext)

        return self.decrypt_params

    def decrypt(self, int_msg_ind=None):
        """Decrypt the message set in a previous set_decrypt_message() call. The
        resulting plaintext is returned as a string.

        A ProcedureError will be raised if the procedure instance has not been
        configured with the required key list.

        """
        if not self.decrypt_params:
            raise ProcedureError("no prior call to set_decrypt_message")

        if not self.key_list or (
                self.key_list.indicator != self.decrypt_params.key_list_ind):
            raise ProcedureError("key list '{}' required".format(
                        self.decrypt_params.key_list_ind))

        # We assume the caller called set_key_list() if necessary, so the M209
        # has been keyed.

        self.m_209.letter_counter = 0
        self.m_209.set_key_wheels(self.decrypt_params.ext_msg_ind)

        # Generate internal message indicator
        if int_msg_ind == None:
            int_msg_ind = self.m_209.encrypt(self.decrypt_params.sys_ind * 12,
                                         group=False)

        # set key wheels to internal message indicator
        self._set_int_message_indicator(int_msg_ind)

        self.m_209.letter_counter = 0
        plaintext = self.m_209.decrypt(self.decrypt_params.ciphertext,
                                       spaces=True, z_sub=True)
        return plaintext

    def _set_int_message_indicator(self, indicator):
        """Sets the key wheels to the given internal message indicator as per
        the standard procedure.

        """
        # Set wheels to internal message indicator from left to right. We must skip
        # letters that aren't valid for a given key wheel.
        it = iter(indicator)
        n = 0
        while n != 6:
            try:
                self.m_209.set_key_wheel(n, next(it))
            except KeyWheelError:
                pass
            except StopIteration:
                assert False, "Ran out of letters building internal message indicator"
            else:
                n += 1
