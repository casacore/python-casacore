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

Binary wheels
-------------

We distribute binary manylinux2010 for Linux, which requires pip > 10.x. To
install python-casacore from a binary wheel run::

    $ pip install python-casacore


Debian & Ubuntu
---------------

python-casacore is now part of Debian and Ubuntu and can be installed using apt::

    $ sudo apt-get install python-casacore


Kern
----

If you want a more up to date version of python-casacore and you are running the latest
Ubuntu LTS you can enable the  `KERN suite <http://kernsuite.info>`_ repository and
install the binary package ::

    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:kernsuite/kern-5
    $ sudo apt-get update
    $ sudo apt-get install python-casacore


from source
-----------

install these requirements:

* `setuptools <https://pypi.python.org/pypi/setuptools>`_
* `Casacore <https://github.com/casacore/casacore/>`__
* `Boost-python <http://www.boost.org/libs/python/doc/>`_
* `numpy <http://www.numpy.org/>`_ 
* `cfitsio <http://heasarc.gsfc.nasa.gov/fitsio/>`_

On ubuntu you can install these with::

    $ apt-get install casacore-dev python-numpy \
        python-setuptools libboost-python-dev libcfitsio3-dev wcslib-dev

* compile and install::

    $ pip install --no-binary python-casacore python-casacore

* or if you are installing from the source repository::

    $ python ./setup.py install
    
* If the compilation fails you might need to help the compiler find the paths to the
  boost and casacore libraries and headers. You can control this with the `CFLAGS` environment
  variable. For example on OS X when using homebrew and clang you need to do something like
  this::
  
    CFLAGS="-std=c++11 \
            -I/usr/local/Cellar/boost/1.68.0/include/ \
            -I/usr/local/include/  \
            -L/usr/local/Cellar/boost/1.68.0/lib \
            -L/usr/local/lib/" \
            pip install python-casacore

Support
=======

if you have any problems, suggestions or questions please open an issue on the
python-casacore github issue tracker.

Credits
=======

* `Ger van Diepen <gervandiepen@gmail.com>`_
* `Malte Marquarding <Malte.Marquarding@gmail.com>`_
* `Gijs Molenaar <gijs@pythonic.nl>`_
