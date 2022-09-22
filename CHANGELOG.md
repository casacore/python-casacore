# 3.5.2

The binary wheels have now been built with `-DPORTABLE=True`. This should fix issues with Dysco crashing on some platforms (due to missing AVX instructions). Otherwise nothing has changed.


# 3.5.1

The binary wheel for python 3.10 is now based on numpy 1.22.4. Otherwise nothing has changed.


# 3.5.0

This version as a binary wheel ships with underlying casacore v3.5.0

Binary wheels are now `manylinux2014` which will only work with pip >= 19.3

The license has changed to LGPL.


# 3.4.0

This version as a binary wheel ships with underlying casacore v3.4.0

There are no changes to python-casacore itself


# 3.3.0

This version as a binary wheel ships with underlying casacore v3.3.0.

Ony a few changes in python-casacore itself:

 - Expose complete MS and subtable definitions (#183)
 - Miminum casacore version is now 3.2.0 (#195)
 - Several improvements to library handling in setup.py (#194)


# 3.2.0

This version as a binary wheel ships with underlying casacore v3.2.0.

Changes are only in the underlying casacore.


# 3.1.1

This is the first release that will be supplied as binary wheels
(manylinux2010). Note that you need pip > 10.x to use manylinux2010 wheels.
If you don't use the binary wheel and unicode is important to you, use
casacore 3.1.1. Note that we skipped 3.1.0 to match the casacore version
and hopefully avoid confusion.

Changes:

 - handle unicode even better! :) (#158)
 - iteritems() in casacore/tables/table.py incompatible with Python 3 (#165)
 - Make a big binary wheel including dependencies (#145)
 - Use ~ instead of - to negate the mask (#179)
 
 
# 3.0

 - Improve the setup procedure (#146)
 - prepare for 3.0.0 (#147)
 - More find_boost improvements  build system (#131)
 - gcc failure when attempting setup.py build_ext on Red Hat EL 7.4 (quantamath.cc) (#135)
 - python-casacore uses hardcoded casa:: calls (#136)
 - quanta example not working with python 2.7.6 bug (#17)
 - Fix build and namespace problem (#137)
 - Remove deprecated has_key (#132)
 - Correct header guard macro definition (#156)
 - Avoiding TypeError deep down in setuptool (#155)


# 2.2.0

 - Expose MeasurementSet functionality (#61)
 - Many improvements to documentation and test coverage
   Thanks to Shibasis Patel (@shibasisp) our Google summer of Code '17 student.
 
 A full list of changes can be found on the issue tracker:
 
 https://github.com/casacore/python-casacore/milestone/6?closed=1
 

# 2.1.0


 - Replaced references to pyrap -> casacore (issue #16)
 - Experimental support for Python3 (needs python3 branch build of casacore)
 - Link against correct Python on OSX when using homebrew (issue #15)


# 2.0.0

- Renamed project from pyrap to python-casacore
- Renamed modules from pyrap to casacore
- Added backswards compatible module which imports casacore
- Removed scons build dependency, just use setup.py 
- Depends on CASACORE 2.0
- Cleanup of project structure
- Moved development to github
