import os, sys, platform
from distutils.command import build_ext
 
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
        build_ext.build_ext.finalize_options(self)

	cclibdir = os.path.join(self.casacore, 'lib')
	prlibdir = os.path.join(self.pyrap, 'lib')
	boostlibdir = os.path.join(self.boost, 'lib')

	ccincdir = os.path.join(self.casacore, 'include', 'casacore')
	princdir = os.path.join(self.pyrap, 'include')
	boostincdir = os.path.join(self.boost, 'include')

	if cclibdir not in self.library_dirs:
	    self.library_dirs += [cclibdir]
	if prlibdir not in self.library_dirs:
	    self.library_dirs += [prlibdir]
	if boostlibdir not in self.library_dirs:
	    self.library_dirs += [boostlibdir]

	if ccincdir not in self.include_dirs:
	    self.include_dirs += [ccincdir]
	if princdir not in self.include_dirs:
	    self.include_dirs += [princdir]
	if boostincdir not in self.include_dirs:
	    self.include_dirs += [boostincdir]

	self.libraries += [self.boostlib]

        if self.enable_hdf5:
            hdf5libdir = os.path.join(self.hdf5, 'lib')
            hdf5incdir = os.path.join(self.hdf5, 'include')
            if hdf5libdir not in self.library_dirs:
                self.library_dirs += [hdf5libdir]
            self.libraries += [self.hdf5lib]


