python-casacore
===============

A fork from pyrap with improvements like:

 * No scons dependency
 * Python 3 support
 * Project structure cleanup
 * Backwards compatibility

*DO NOT USE THIS CODE*. Use the original Pyrap. This is my personal attempt to
make pyrap better.

Installation
============

```
$ python setup.py install
```

About
=====

This is the python<->casacore wrapper project.

libpyrap contains the casacore to python data type conversions using boost::python.

pyrap_* contain the python bindings to various casacore packages using libpyrap

To build and install everything run 'batchbuild.py'.
