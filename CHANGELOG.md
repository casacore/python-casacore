# 3.0

 - Improve the setup procedure (#146)
 - prepare for 3.0.0 (#147)
 - More find_boost improvements  build system (#131)
 - gcc failure when attempting setup.py build_ext on Red Hat EL 7.4 (quantamath.cc) (#135)
 - python-casacore uses hardcoded casa:: calls (#136)
 - quanta example not working with python 2.7.6 bug (#17)
 - Fix build and namespace problem (#137)
 - Remove deprecated has_key (#132)


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
