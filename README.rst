python-casacore
===============

Python-casacore is a set of Python bindings for `casacore <https://code.google.com/p/casacore/>`_,
a c++ library used in radio astronomy. Python-casacore replaces the old
`pyrap <https://code.google.com/p/pyrap/>`_.


The python-casacore documentation can be found on `casacore.github.io/python-casacore <http://casacore.github.io/python-casacore>`_.

Build status
------------

.. image:: https://github.com/casacore/python-casacore/actions/workflows/linux.yml/badge.svg
    :target: https://github.com/casacore/python-casacore/actions/workflows/linux.yml
.. image:: https://github.com/casacore/python-casacore/actions/workflows/osx.yml/badge.svg
    :target: https://github.com/casacore/python-casacore/actions/workflows/osx.yml


Installation
============

Binary wheels
-------------

We distribute binary manylinux2014 for Linux, which requires pip >= 19.3. To
install python-casacore from a binary wheel run::

    $ pip install python-casacore


Debian & Ubuntu
---------------

python-casacore is now part of Debian and Ubuntu and can be installed using apt::

    $ sudo apt-get install python-casacore


from source
-----------

install these requirements:

* `Casacore <https://github.com/casacore/casacore/>`__
* `Boost-python <http://www.boost.org/libs/python/doc/>`_
* `numpy <http://www.numpy.org/>`_
* `cfitsio <http://heasarc.gsfc.nasa.gov/fitsio/>`_
* `wcslib <https://www.atnf.csiro.au/people/mcalabre/WCS/>`_
* `pip <https://bootstrap.pypa.io/get-pip.py>`_

On ubuntu you can install these with::

    $ apt-get install casacore-dev libboost-python-dev python3-numpy \
        libcfitsio3-dev wcslib-dev python3-pip

* compile and install::

    $ pip install --no-binary python-casacore python-casacore

* or if you are installing from the source repository::

    $ pip install .

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
* `Tammo Jan Dijkema <dijkema@astron.nl>`_
