python-casacore
===============

Python-casacore is a set of Python bindings for `casacore <https://code.google.com/p/casacore/>`_,
a c++ library used in radio astronomy. Python-casacore replaces the old
`pyrap <https://code.google.com/p/pyrap/>`_.


The python-casacore documentation can be found on `casacore.github.io/python-casacore <http://casacore.github.io/python-casacore>`_.

.. image:: https://travis-ci.org/casacore/python-casacore.svg?branch=master
    :target: https://travis-ci.org/casacore/python-casacore
.. image:: https://coveralls.io/repos/github/casacore/python-casacore/badge.svg?branch=master
    :target: https://coveralls.io/github/casacore/python-casacore?branch=master

Installation
============

Ubuntu 16.04
------------

The easiest way to start using python-casacore is to enable the `KERN suite <http://kernsuite.info>`_ repository and install the binary package ::

    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:kernsuite/kern-1
    $ sudo apt-get update
    $ sudo apt-get install python-casacore


from source
-----------

install these requirements:

* `setuptools <https://pypi.python.org/pypi/setuptools>`_
* `Casacore <https://code.google.com/p/casacore/>`_ >= 2.3
* `Boost-python <http://www.boost.org/libs/python/doc/>`_
* `numpy <http://www.numpy.org/>`_ 
* `cfitsio <http://heasarc.gsfc.nasa.gov/fitsio/>`_

On ubuntu you can install these with:

* enable the `KERN suite <http://kernsuite.info>`_ 

* install build dependencies::

    $ apt-get install libcasacore2-dev python-numpy \
        python-setuptools libboost-python-dev libcfitsio3-dev

* compile and install::

    $ python ./setup.py install
    
* if you need to supply compile parameters, for example if you have your casacore
  library installed in a different location have a look at the  `build_ext` help::
  
   $ python ./setup.py build_ext -h
   
  For example, if `casacore` is installed in `/opt/local/`, you can specify the
  library path and include path with::
  
   $ python ./setup.py build_ext -I/opt/local/include -L/opt/local/lib
   
   $ python ./setup.py install


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
