import glob
from distutils.core import setup, Extension
from setupext import casacorebuild_ext

PKGNAME = "pyrap_fitting"
EXTNAME = "_fitting"
casalibs = ['casa_scimath', 'casa_scimath_f'] # casa_casa is added by default
deplibs = ['gfortran'] # change to g2c if build against it.

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs + deplibs)
setup(name = PKGNAME,
      version = 'trunk',
      description = 'Python bindings to casacore Fitting',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['fitting','casacore'],
      long_description = '''
This is a python module to access the casacore c++ scimath fitting.
''',
      packages = [ PKGNAME ],
      license = 'GPL',
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext})
