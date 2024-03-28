"""Example of how to perform an encrypt operation using the standard
procedure. Assumes a key file named m209keys.cfg exists in the current directory
and contains the key list with indicator MB.

"""
from m209.procedure import StdProcedure
from m209.keylist.config import read_key_list

key_list = read_key_list('m209keys.cfg', 'MB')
if key_list:
    proc = StdProcedure(key_list=key_list)
    plaintext = "THE PIZZA HAS ARRIVED STOP NO SIGN OF ENEMY FORCES STOP"
    msg = proc.encrypt(plaintext, spaces=True, ext_msg_ind='PDUFHL', sys_ind='I')
    print(msg)
else:
    print("Key list MB not found")
