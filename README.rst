python-casacore
===============

Python-casacore is a set of Python bindings for casacore,
a library used in radio astronomy. It hopefully will replace the old pyrap
some day.

* https://code.google.com/p/casacore/
* https://code.google.com/p/pyrap/

Please don't use yet, unless you want to be involved in the development and testing.


Installation
============

to install run (change the include path to your casacore headers path)::

    $ python setup.py build_ext -I/usr/include/casacore
    $ python setup.py install


Requirements
============

* setuptools
* Casacore >= 2.0: https://code.google.com/p/casacore/
* Boost-python: http://www.boost.org/doc/libs/1_55_0/libs/python/doc/
* numpy: http://www.numpy.org/
* cfitsio: http://heasarc.gsfc.nasa.gov/fitsio/

on ubuntu:

* enable the SKA-SA launchpad PPA: https://launchpad.net/~ska-sa/+archive/ubuntu/main
* enable the SKA-sa launchpas BETA PPA: https://launchpad.net/~ska-sa/+archive/ubuntu/beta
* install build dependencies::

    $ apt-get install libcasacore-dev casacore-data python-numpy python-nose \
        python-setuptools libboost-python-dev libcfitsio3-dev


Staying up to date
==================

Stay up to date by subscribing to the pyrap-devel mailinglist:


https://groups.google.com/forum/#!forum/pyrap-devel


About
=====

* Ger van Diepen -  gervandiepen@gmail.com
* Malte Marquarding - Malte.Marquarding@gmail.com
* Gijs Molenaar - gijs@pythonic.nl
