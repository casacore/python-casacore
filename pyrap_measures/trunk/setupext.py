import os, sys, platform
from distutils.command import build_ext
 
class casacorebuild_ext(build_ext.build_ext):
    """
    """
    user_options = build_ext.build_ext.user_options + \
            [('casacore=', None, 'Prefix for casacore installation location'),
	     ('pyrap=', None, 'Prefix for pyrap installation location'),
	     ('boost=', None, 'Prefix for boost_python installation location'),
	     ('boostlib=', None, 'Name of the boost_python library')
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
