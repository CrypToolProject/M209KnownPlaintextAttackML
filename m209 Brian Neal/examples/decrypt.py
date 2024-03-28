"""Example of how to perform a decrypt operation using the standard
procedure. Assumes a key file named m209keys.cfg exists in the current directory
and contains the key list with indicator MB.

"""
from m209.procedure import StdProcedure
from m209.keylist.config import read_key_list

msg = ('IIPDU FHLMB LASGD KTLDO OSRMZ PWGEB HYMCB IKSPT IUEPF FUHEO NQTWI VTDPC'
      ' GSPQX IIPDU FHLMB')

proc = StdProcedure()
params = proc.set_decrypt_message(msg)
key_list = read_key_list('m209keys.cfg', params.key_list_ind)
if key_list:
    proc.set_key_list(key_list)
    plaintext = proc.decrypt()
    print(plaintext)
else:
    print("Key list '{}' not found".format(params.key_list_ind))
