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
	     ('f2clib=', None, 'Name of the fortran to c library'),
	     ('cfitsio=', None, 'Prefix for cfitsio installation location'),
	     ('cfitsiolib=', None, 'Name of the cfitsio library'),
	     ('wcs=', None, 'Prefix for wcslib installation location'),
	     ('wcslib=', None, 'Name of the wcs library')
	     ]

    def initialize_options(self):
        """
	Overload to enable custom settings to be picked up
	"""
        build_ext.build_ext.initialize_options(self)
        
        # attribute corresponding to directory prefix
        # command line option
	self.libraries = ['casa_casa', 'pyrap']
	self.boostlib = 'boost_python'
	self.pyrap = '/usr/local'
	self.casacore = '/usr/local'
	self.boost = '/usr'
        self.f2clib = 'gfortran'
        self.cfitsio = '/usr'
        self.cfitsiolib = 'cfitsio'
	self.wcs = '/usr/local'
	self.wcslib = 'wcs'
	    
    def finalize_options(self):
        """
	Overloaded build_ext implementation to append custom library
        include file and library linking options
	"""
        build_ext.build_ext.finalize_options(self)

	cclibdir = os.path.join(self.casacore, 'lib')
	prlibdir = os.path.join(self.pyrap, 'lib')
	boostlibdir = os.path.join(self.boost, 'lib')
	cfitsiolibdir = os.path.join(self.cfitsio, 'lib')
	wcslibdir = os.path.join(self.wcs, 'lib')
	ccincdir = os.path.join(self.casacore, 'include', 'casacore')
	princdir = os.path.join(self.pyrap, 'include')
	boostincdir = os.path.join(self.boost, 'include')
	cfitsioincdir = os.path.join(self.cfitsio, 'include')
	cfitsioincdir2 = os.path.join(self.cfitsio, 'include', 'cfitsio')
        # cfitsio2 has different path
        if os.path.exists(cfitsioincdir2):
            cfitsoincdir = cfitsioincdir2
	wcsincdir = os.path.join(self.wcs, 'include', 'wcslib')


	if cclibdir not in self.library_dirs:
	    self.library_dirs += [cclibdir]
	if prlibdir not in self.library_dirs:
	    self.library_dirs += [prlibdir]
	if boostlibdir not in self.library_dirs:
	    self.library_dirs += [boostlibdir]

	if cfitsiolibdir not in self.library_dirs:
	    self.library_dirs += [cfitsiolibdir]
	if wcslibdir not in self.library_dirs:
	    self.library_dirs += [wcslibdir]

	if ccincdir not in self.include_dirs:
	    self.include_dirs += [ccincdir]
	if princdir not in self.include_dirs:
	    self.include_dirs += [princdir]
	if boostincdir not in self.include_dirs:
	    self.include_dirs += [boostincdir]
	if cfitsioincdir not in self.include_dirs:
	    self.include_dirs += [cfitsioincdir]
	if wcsincdir not in self.include_dirs:
	    self.include_dirs += [wcsincdir]

	self.libraries += [self.boostlib]
	self.libraries += [self.wcslib]
	self.libraries += [self.cfitsiolib]
