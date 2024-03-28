#!/usr/bin/env python
# Copyright (C) 2013 by Brian Neal.
# This file is part of m209, the M-209 simulation.
# m209 is released under the MIT License (see LICENSE.txt).

from distutils.core import setup
from os.path import join, dirname

import m209

setup(
    name='m209',
    version=m209.__version__,
    author='Brian Neal',
    author_email='bgneal@gmail.com',
    url='https://bitbucket.org/bgneal/m209/',
    license='MIT',
    description='A historically accurate M-209 simulation library.',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    packages=['m209', 'm209.tests', 'm209.keylist', 'm209.keylist.tests'],
    scripts=['scripts/m209'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
