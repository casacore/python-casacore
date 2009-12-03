import os, sys, platform
from distutils.command import build_ext
from setuptools import Command

def get_libdir():
    if not platform.architecture()[0].startswith("64"):
        return "lib"
    dist = platform.dist()[0].lower()
    distdict = dict(suse='lib64', redhat='lib64')   
    return distdict.get(dist, 'lib')

ARCHLIBDIR = get_libdir()

class casacorebuild_ext(build_ext.build_ext):
    """
    """
    user_options = build_ext.build_ext.user_options + \
            [('casacore=', None, 'Prefix for casacore installation location'),
	     ('pyrap=', None, 'Prefix for pyrap installation location'),
	     ('boost=', None, 'Prefix for boost_python installation location'),
	     ('boostlib=', None, 'Name of the boost_python library'),
             # can't do autoconf so have to enable explictly
             ('enable-hdf5=', None, 'Enable hdf5'),
	     ('hdf5=', None, 'Prefix for hdf5 installation location'),
	     ('hdf5lib=', None, 'Name of the hdf5 library'),

             # catch the rest to suppress errors
	     ('f2c=', None, 'Prefix for f2clib installation location'),
	     ('f2clib=', None, 'Name of the fortran to c library'),
	     ('cfitsio=', None, 'Prefix for cfitsio installation location'),
	     ('cfitsiolib=', None, 'Name of the cfitsio library'),
	     ('wcs=', None, 'Prefix for wcslib installation location'),
	     ('wcslib=', None, 'Name of the wcs library'),
	     ('lapack=', None, 'Prefix for lapack installation location'),
	     ('lapacklib=', None, 'Name of the lapack library'),
	     ]

    def initialize_options(self):
        """
	Overload to enable custom settings to be picked up
	"""
        build_ext.build_ext.initialize_options(self)
        # attribute corresponding to directory prefix
        # command line option
	self.libraries = ['pyrap', 'casa_casa']
	self.boostlib = 'boost_python'
	self.pyrap = '/usr/local'
	self.casacore = '/usr/local'
	self.boost = '/usr'
        self.enable_hdf5 = False
        self.hdf5 = '/usr'
        self.hdf5lib = 'hdf5'
        # not used here - disable
        self.f2c = None
        self.f2clib = None
        self.lapack = None
        self.lapacklib = None
        self.cfitsio = None
        self.cfitsiolib = None
        self.wcs = None
        self.wcslib = None
	    
    def finalize_options(self):
        """
	Overloaded build_ext implementation to append custom library
        include file and library linking options
	"""
        pass

class assay(Command):
    """Command to run casacore_assay"""

    ## The description string of this Command class    
    description = "run an assay test on the target"

    ## List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [('casacore=', 'c', "Path to casacoreroot")]

    ## Initialise all the option member variables
    def initialize_options (self):
        self.casacore = "/usr/local"
    
    ## Finalize the option member variables after they have been configured
    # by command line arguments or the configuration file. Needs to ensure that
    # they are valid for processing.
    def finalize_options (self):
        pass

    def run(self):
        import subprocess
        import glob
        tdir = "tests"
        if not os.path.exists(tdir):
            print "No tests found"
            return
        os.chdir(tdir)
        pth = os.path.join(self.casacore, "bin")
        comm = os.path.join(pth, "casacore_assay")
        os.environ["PATH"] = os.path.pathsep.join([pth, os.environ["PATH"]])
        if not os.path.exists(comm):
            print "casacore_assay not found"
            return

        tfiles = glob.glob("t*.py")
        for f in tfiles:
            err = subprocess.call(comm+" ./"+f, shell=True)
