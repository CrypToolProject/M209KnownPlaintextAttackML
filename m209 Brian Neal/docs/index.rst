.. m209 documentation master file, created by
   sphinx-quickstart on Thu Jul  4 18:12:07 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to m209's documentation!
================================

:Author: Brian Neal <bgneal@gmail.com>
:Version: |release|
:Date: |today|
:Home Page: https://bitbucket.org/bgneal/m209/
:License: MIT License (see LICENSE.txt)
:Documentation: http://m209.readthedocs.org/
:Support: https://bitbucket.org/bgneal/m209/issues

Introduction
------------

The `M-209`_ is a mechanical cipher machine used by the US military during
World War II and up to the Korean War. The M-209 is also known as the CSP-1500
by the US Navy. The M-209 is an example of a Hagelin device, a family of
mechanical cipher machines created by Swedish inventor `Boris Hagelin`_, where
it is known as the C-38.

``m209`` is a complete `M-209`_ simulation library and command-line application
written in Python 3. ``m209`` is historically accurate, meaning that it can
exchange messages with an actual M-209 cipher machine.

It is hoped that this library will be useful to M-209 enthusiasts, historians,
and students interested in cryptography.

``m209`` strives to be Pythonic, easy to use, and comes with both unit tests
and documentation. ``m209`` is a library for building applications for
encrypting and decrypting M-209 messages. ``m209`` also ships with a simple
command-line application that can encrypt & decrypt messages for scripting and
experimentation.

Documentation
-------------

Contents:

.. toctree::
   :maxdepth: 2

   tutorial
   commandline
   library


Requirements
------------

``m209`` is written in Python_ 3, specifically Python 3.3. At this time it will
not run on Python 2.x.

``m209`` has no other requirements or dependencies.

Installation
------------

``m209`` is available on the `Python Package Index`_ (PyPI).

You can install it using pip_::

   $ pip install m209                  # install
   $ pip install --upgrade m209        # upgrade

You may also download an archive file of the latest code by visiting the `m209
Bitbucket page`_. Alternatively if you use Mercurial_, you can clone the
repository with the following command::

   $ hg clone https://bitbucket.org/bgneal/m209

If you did not use pip (you downloaded or cloned the code yourself), you can
install with::

   $ cd where-you-extracted-m209
   $ python setup.py install

To run the unit tests::

   $ cd where-you-extracted-m209
   $ python -m unittest discover -b

Support & Source
----------------

All support takes place at the `m209 Bitbucket page`_. Please enter any
feature requests or bugs into the `issue tracker`_.

.. _references-label:

References
----------

All of the resources listed below were useful to me in the creation of the
``m209`` library. In particular, I want to thank Mark J. Blair for his detailed
explanations of the M-209's operation and procedures. The official training
film was also highly instructive.

#. `M-209 at Wikipedia <http://en.wikipedia.org/wiki/M-209>`_
#. `Mark J. Blair's Converter M-209-B <http://www.nf6x.net/2009/02/converter-m-209-b/>`_
#. `1942 M-209 Manual <http://maritime.org/tech/csp1500inst.htm>`_
#. `1944 M-209 Manual <http://www.ilord.com/m209manual.html>`_
#. `Official M-209 Training Film <http://www.youtube.com/playlist?list=PLCPgncK_sTnEny2-uoTV-1_GC72zo-vKq>`_ - This is a 4 video YouTube playlist of an actual 1940's era US War Department training film. Demonstrates the M-209 and operational procedures. Very interesting!
#. `Transcript of Training Film <http://www.ilord.com/m209-training.html>`_ -
   Transcript of the above film.
#. `Mark J. Blair's M-209 Cipher Machine Group <http://www.nf6x.net/groups/m209group/>`_ -
   Informal club for M-209 enthusiasts. Includes detailed explanations of the
   device and how to use it. Very useful.
#. `Dirk Rijmenants' M-209 Simulator <http://users.telenet.be/d.rijmenants/en/m209sim.htm>`_ -
   Graphical M-209 simulator
#. `Mark J. Blair's Hagelin project suite at GitHub <https://github.com/NF6X/hagelin>`_
   - M-209 simulator written in C++
#. `Jean-François Bouchaudy's Crypto Pages <http://www.jfbouch.fr/crypto/>`_
   - Includes another Python-based M-209 simulator and a M-209 challenge. In French.
#. `The C-38 / M-209 Cipher Machine <http://hem.passagen.se/tan01/c38.html>`_
   - Another M-209 page. This one has useful info on creating key lists and a C-38 simulator written in C.

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. _M-209: http://en.wikipedia.org/wiki/M-209
.. _Boris Hagelin: http://en.wikipedia.org/wiki/Boris_Hagelin
.. _Python: http://www.python.org
.. _Python Package Index: http://pypi.python.org/pypi/m209/
.. _m209 Bitbucket page: https://bitbucket.org/bgneal/m209
.. _pip: http://www.pip-installer.org
.. _Mercurial: http://mercurial.selenic.com/
.. _issue tracker: https://bitbucket.org/bgneal/m209/issues
