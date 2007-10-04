import glob
from distutils.core import setup, Extension
from setupext import casacorebuild_ext, casacore_defines

PKGNAME = "pyrap_functionals"
EXTNAME = "_functionals"
casalibs = ['casa_scimath', 'casa_scimath_f'] # casa_casa is added by default
deplibs = ['gfortran'] # change to g2c if build against it.

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs + deplibs,
			define_macros = casacore_defines())
setup(name = PKGNAME,
      version = 'trunk',
      description = 'Python bindings to casacore Functionals',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['measures','casacore'],
      long_description = '''
This is a python module to access the casacore c++ scimath functionals.
''',
      packages = [ PKGNAME ],
      license = 'GPL',
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext})
