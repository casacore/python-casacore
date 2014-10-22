python-casacore
===============

Python-casacore is a set of Python bindings for casacore,
a library used in radio astronomy. It hopefully will replace the old pyrap
some day.

Differences from pyrap:

* No scons
* Python 3 support
* Project structure cleanup
* Backwards compatibility

python-casacore is based on casacore 2.0, which is not released yet.

https://code.google.com/p/casacore/


Installation
============

`$ python setup.py install`

**note:** If you like to install your casacore and whatever in obscure
places checkout `python setup.py build_ext -h` and find out how
to set for example the include path.

This works for me:

```
$ python setup.py build_ext -I/usr/include/casacore:src
$ python setup.py install
```

We will make python-casacore installable by pypi when casacore 2.0 is
released.

Requirements
============

 * Casacore: https://code.google.com/p/casacore/
 * Boost-python: http://www.boost.org/doc/libs/1_55_0/libs/python/doc/
 * numpy: http://www.numpy.org/


Staying up to date
==================

Stay up to date by subscribing to the pyrap-devel mailinglist:


https://groups.google.com/forum/#!forum/pyrap-devel


About
=====

 * Ger van Diepen -  gervandiepen@gmail.com
 * Malte Marquarding - Malte.Marquarding@gmail.com
 * Gijs Molenaar - gijs@pythonic.nl
