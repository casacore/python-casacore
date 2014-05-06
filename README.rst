python-casacore
===============

A fork from pyrap with improvements like:

* No scons
* Python 3 support
* Project structure cleanup
* Backwards compatibility

*DO NOT USE THIS CODE*. Use the original Pyrap. This is my personal attempt to
make pyrap better.

Installation
============

`$ python setup.py install`

**note:** If you like to install your casacore and whatever in obscure
places checkout `python setup.py build_ext -h` and find out how
to set for example the include path.


Requirements
============

 * Casacore: https://code.google.com/p/casacore/
 * Boost-python: http://www.boost.org/doc/libs/1_55_0/libs/python/doc/
 * numpy: http://www.numpy.org/

About
=====

This is the python<->casacore wrapper project.

libpyrap contains the casacore to python data type conversions using boost::python.

pyrap_* contain the python bindings to various casacore packages using libpyrap

To build and install everything run 'batchbuild.py'.
