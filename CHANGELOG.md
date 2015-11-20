# 2.1.0

## General
 - Replaced references to pyrap -> casacore (issue #16)
 - Experimental support for Python3 (needs python3 branch build of casacore)
 - Link against correct Python on OSX when using homebrew (issue #15)


# 2.0.0

## General
- Renamed project from pyrap to python-casacore
- Renamed modules from pyrap to casacore
- Added backswards compatible module which imports casacore
- Removed scons build dependency, just use setup.py 
- Depends on CASACORE 2.0
- Cleanup of project structure
- Moved development to github
