python-casacore
===============

Python-casacore is a set of Python bindings for `casacore <https://code.google.com/p/casacore/>`_,
a library used in radio astronomy. It hopefully will replace the old `pyrap <https://code.google.com/p/pyrap/>`_
some day.

Please don't use yet, unless you want to be involved in the development and testing.


Installation
============

Ubuntu 14.04
------------

This is most simple way to get started with python-casacore::

    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:ska-sa/beta
    $ sudo apt-get update
    $ sudo apt-get install python-casacore


from source
-----------

install these requirements:

* `setuptools <https://pypi.python.org/pypi/setuptools>`_
* `Casacore <https://code.google.com/p/casacore/>`_ >= 2.0
* `Boost-python <http://www.boost.org/libs/python/doc/>`_
* `numpy <http://www.numpy.org/>`_ 
* `cfitsio <http://heasarc.gsfc.nasa.gov/fitsio/>`_

On ubuntu you can install these with:

* enable the `SKA-SA launchpad PPA <https://launchpad.net/~ska-sa/+archive/ubuntu/main>`_ 

* install build dependencies::

    $ apt-get install libcasacore-devpython-numpy python-nose \
        python-setuptools libboost-python-dev libcfitsio3-dev

Then to compile install run (change the include path to your casacore headers path)::

    $ python setup.py build_ext -I/usr/include/casacore
    $ python setup.py install


Using pip
-----------------

Due to a bug in casacore you need to manually set the include path. Unfortunatly you
can't do this with pip command line arguments, so you need to do this with a workaround.

create and modify the file *~/.pydistutils.cfg*::

    [build_ext]
    include_dirs=/usr/include/casacore
    
Now you can pip install python-casacore::

    $ pip install python-casacore


Staying up to date
==================

Stay up to date by subscribing to the
`pyrap-devel mailinglist <https://groups.google.com/forum/#!forum/pyrap-devel>`_.


Credits
=======

* `Ger van Diepen <gervandiepen@gmail.com>`_
* `Malte Marquarding <Malte.Marquarding@gmail.com>`_
* `Gijs Molenaar <gijs@pythonic.nl>`_
