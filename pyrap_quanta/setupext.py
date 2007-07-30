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
	    
def casacore_defines():
    """
    Get/autodetect platform specific defines.
    """
    pd = { "darwin": [("AIPS_DARWIN", None), ("AIPS_NO_LEA_MALLOC", None)],
	   "64bit": [("__x86_64__", None), ("AIPS_64B", None)],
	   "linux2": [("AIPS_LINUX", None)]
	   }
    # -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
    platfdefs = [("AIPS_STDLIB", None), ("AIPS_AUTO_STL", None)]
    sysplf = sys.platform
    sysarch = platform.architecture()[0]
    if sysarch == '64bit':
	platfdefs += pd["64bit"]
    else:
	platfdefs += pd[sysplf]
    if sys.byteorder == "little":
	platfdefs += [("AIPS_LITTLE_ENDIAN", None)]
    return platfdefs

