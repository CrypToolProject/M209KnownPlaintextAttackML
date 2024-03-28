# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

"""This module contains the main() entry point for the command-line m209
utility.

"""
import argparse
import logging
import os.path
import random
import re
import sys

from m209 import M209Error
from m209.converter import M209_ALPHABET_SET
from m209.data import KEY_WHEEL_DATA
from m209.keylist.generate import generate_key_list
from m209.keylist.key_list import valid_indicator, IndicatorIter
from m209.keylist.config import write as write_config, read_key_list
from m209.procedure import StdProcedure

DESC = "M-209 simulator and utility program"
DEFAULT_KEY_LIST = 'm209keys.cfg'
LOG_CHOICES = ['debug', 'info', 'warning', 'error', 'critical']
SYS_IND_RE = re.compile(r'^[A-Z]{1}$')
M209_ALPHABET_LOWER = set(c.lower() for c in M209_ALPHABET_SET)


def validate_key_list_indicator(s):
    """Validation/conversion function for validating the supplied starting key
    list indicator.

    Returns the string value if valid, otherwise raises an ArgumentTypeError.

    """
    if len(s) == 2:
        s = s.upper()
        if valid_indicator(s):
            return s

    raise argparse.ArgumentTypeError('must be in the range AA-ZZ')


def validate_num_key_lists(s):
    """Validation/conversion function for validating the number of key lists to
    generate.

    Returns the integer value if valid, otherwise raises an ArgumentTypeError

    """
    bounds = (1, 26 ** 2)
    msg = "value must be in range {}-{}".format(*bounds)
    try:
        val = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(msg)

    if not (bounds[0] <= val <= bounds[1]):
        raise argparse.ArgumentTypeError(msg)
    return val


def validate_ext_indicator(s):
    """Validation function for the external message indicator option.

    Returns the string value if valid, otherwise raises an ArgumentTypeError.

    """
    if len(s) == 6:
        s = s.upper()
        for n, c in enumerate(s):
            if c not in KEY_WHEEL_DATA[n][0]:
                break
        else:
            return s

    raise argparse.ArgumentTypeError(
        "{} is not a valid external message indicator".format(s))


def validate_sys_indicator(s):
    """Validation function for the system message indicator option.

    Returns the string value if valid, otherwise raises an ArgumentTypeError.

    """
    if len(s) == 1:
        s = s.upper()
        if s in M209_ALPHABET_SET:
            return s

    raise argparse.ArgumentTypeError('value must be 1 letter')


def plaintext_filter(fp):
    """Generator function to filter input plaintext.

    * upper case letters are passed as-is.
    * lower case letters are converted to upper case.
    * Whitespace characters are converted to 'Z'.
    * All other characters are dropped from the input.

    """
    for line in fp:
        for c in line:
            if c in M209_ALPHABET_SET:
                yield c
            elif c in M209_ALPHABET_LOWER:
                yield c.upper()
            elif c.isspace():
                yield 'Z'


def encrypt(args):
    """Encrypt subcommand processor"""
    logging.info("Encrypting using key file %s", args.key_file)

    if args.text and args.file:
        sys.exit("Please supply either -f/--file or -t/--text, not both\n")
    elif not args.text and not args.file:
        sys.exit("Please supply either -f/--file or -t/--text\n")

    # Get a key list from the key list file
    if not os.path.isfile(args.key_file):
        sys.exit("key list file not found: {}\n".format(args.key_file))

    key_list = read_key_list(args.key_file, args.key_list_ind)
    if not key_list:
        sys.exit("key list not found in file: {}\n".format(args.key_file))

    # Get the plaintext
    if args.text:
        plaintext = plaintext_filter(args.text)
    else:
        infile = open(args.file, 'r') if args.file != '-' else sys.stdin
        plaintext = plaintext_filter(infile)

    proc = StdProcedure(key_list=key_list)
    ct = proc.encrypt(plaintext, ext_msg_ind=args.ext_ind, sys_ind=args.sys_ind)
    print(ct)


def decrypt(args):
    """Decrypt subcommand processor"""
    logging.info("Decrypting using key file %s", args.key_file)

    if args.text and args.file:
        sys.exit("Please supply either -f/--file or -t/--text, not both\n")
    elif not args.text and not args.file:
        sys.exit("Please supply either -f/--file or -t/--text\n")

    # Check for key list file
    if not os.path.isfile(args.key_file):
        sys.exit("key list file not found: {}\n".format(args.key_file))

    # Get the ciphertext to decrypt
    if args.text:
        msg = args.text
    else:
        # Read contents of ciphertext file
        if args.file == '-':
            msg = sys.stdin.read()
        else:
            with open(args.file, 'r') as fp:
                msg = fp.read()
        msg = msg.strip()

    # Start the decrypt procedure
    proc = StdProcedure()
    params = proc.set_decrypt_message(msg)

    # Find a key list for the message
    key_list = read_key_list(args.key_file, params.key_list_ind)
    if key_list is None:
        sys.exit("Could not find key list {} in {}\n".format(
            params.key_list_ind, args.key_file))

    # Install the key list and perform the decrypt operation
    proc.set_key_list(key_list)
    plaintext = proc.decrypt()
    print(plaintext)


def keygen(args):
    """Key list generation subcommand processor"""
    logging.info("Creating key list file: %s", args.key_file)

    if not args.overwrite and os.path.exists(args.key_file):
        sys.exit("File '{}' exists. Use -o to overwrite\n".format(args.key_file))

    if args.start is None:  # random indicators
        indicators = random.sample([i for i in IndicatorIter()], args.number)
        indicators.sort()
    else:
        it = IndicatorIter(args.start)
        n = len(it)
        if n < args.number:
            sys.exit("Error: can only produce {} key lists when starting at {}\n".format(
                n, args.start))

        indicators = (next(it) for n in range(args.number))

    key_lists = (generate_key_list(indicator) for indicator in indicators)

    write_config(args.key_file, key_lists)


def main(argv=None):
    """Entry point for the m209 command-line utility."""

    # create the top-level parser
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-l', '--log', choices=LOG_CHOICES, default='warning',
                        help='set log level [default: %(default)s]')
    subparsers = parser.add_subparsers(title='list of commands',
                                       description='type %(prog)s {command} -h for help on {command}')

    # create the sub-parser for encrypt
    enc_parser = subparsers.add_parser('encrypt', aliases=['enc'],
                                       description='Encrypt text from a file or command-line',
                                       help='encrypt text from file or command-line',
                                       epilog='Either the -f/--file or -t/--text arguments must be supplied')
    enc_parser.add_argument('-z', '--key-file', default=DEFAULT_KEY_LIST,
                            help='path to key list file [default: %(default)s]')
    enc_parser.add_argument('-f', '--file',
                            help='path to plaintext file or - for stdin')
    enc_parser.add_argument('-t', '--text',
                            help='text string to encrypt')
    enc_parser.add_argument('-k', '--key-list-ind', metavar='XX',
                            type=validate_key_list_indicator,
                            help='2-letter key list indicator; if omitted a random one is used')
    enc_parser.add_argument('-e', '--ext-ind', metavar='ABCDEF',
                            type=validate_ext_indicator,
                            help='6-letter external message indicator; if omitted a random one is used')
    enc_parser.add_argument('-s', '--sys-ind', metavar='S',
                            type=validate_sys_indicator,
                            help='1-letter system indicator; if omitted a random one is used')
    enc_parser.set_defaults(subcommand=encrypt)

    # create the sub-parser for decrypt
    dec_parser = subparsers.add_parser('decrypt', aliases=['dec'],
                                       description='Decrypt text from a file or command-line',
                                       help='decrypt text from file or command-line',
                                       epilog='Either the -f/--file or -t/--text arguments must be supplied')
    dec_parser.add_argument('-z', '--key-file', default=DEFAULT_KEY_LIST,
                            help='path to key list file [default: %(default)s]')
    dec_parser.add_argument('-f', '--file',
                            help='path to ciphertext file or - for stdin')
    dec_parser.add_argument('-t', '--text',
                            help='text string to decrypt')
    dec_parser.set_defaults(subcommand=decrypt)

    # create the sub-parser for generating key lists

    kg_parser = subparsers.add_parser('keygen', aliases=['key'],
                                      description='Generate key list file',
                                      help='generate key list')
    kg_parser.add_argument('-z', '--key-file', default=DEFAULT_KEY_LIST,
                           help='path to key list file [default: %(default)s]')
    kg_parser.add_argument('-o', '--overwrite', action='store_true',
                           help='overwrite key list file if it exists')
    kg_parser.add_argument('-s', '--start', metavar='XX',
                           type=validate_key_list_indicator,
                           help='starting indicator; if omitted, random indicators are used')
    kg_parser.add_argument('-n', '--number', type=validate_num_key_lists, default=1,
                           help='number of key lists to generate [default: %(default)s]')
    kg_parser.set_defaults(subcommand=keygen)

    args = parser.parse_args(args=argv)

    log_level = getattr(logging, args.log.upper())
    logging.basicConfig(level=log_level, format='%(message)s')

    try:
        args.subcommand(args)
    except EnvironmentError as ex:
        sys.exit('{}\n'.format(ex))
    except KeyboardInterrupt:
        sys.exit('Interrupted\n')
    except M209Error as ex:
        sys.exit('{}\n'.format(ex))


if __name__ == '__main__':
    main()
