python-casacore
===============

Python-casacore is a set of Python bindings for `casacore <https://code.google.com/p/casacore/>`_,
a c++ library used in radio astronomy. Python-casacore replaces the old
`pyrap <https://code.google.com/p/pyrap/>`_.


The python-casacore documentation can be found on `readthedocs <http://python-casacore.readthedocs.org/>`_.

.. image:: https://travis-ci.org/casacore/python-casacore.svg?branch=master
    :target: https://travis-ci.org/casacore/python-casacore

Installation
============

Ubuntu 14.04
------------

This is most simple way to get started with python-casacore::

    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:radio-astro/main
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

* enable the `radio astronomy launchpad PPA <https://launchpad.net/~radio-astro/+archive/ubuntu/main>`_ 

* install build dependencies::

    $ apt-get install libcasacore2-dev python-numpy \
        python-setuptools libboost-python-dev libcfitsio3-dev

* compile and install::

    $ python ./setup.py install
    
* if you need to supply compile parameters, for example if you have your casacore
  library installed in a different location have a loook at the  `build_ext` help::
  
   $ python ./setup.py build_ext -h


Using pip
---------

python-casacore is also available trough pip. Note that you need to manually satisfy
the requirements mentioned above::
    $ pip install python-casacore


Support
=======

if you have any problems, suggestions or questions please open an issue on the
python-casacore github issue tracker.

Credits
=======

* `Ger van Diepen <gervandiepen@gmail.com>`_
* `Malte Marquarding <Malte.Marquarding@gmail.com>`_
* `Gijs Molenaar <gijs@pythonic.nl>`_
