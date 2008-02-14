import glob
from distutils.core import setup, Extension
from setupext import casacorebuild_ext

PKGNAME = "pyrap_quanta"
EXTNAME = "_quanta"
casalibs = [] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries = casalibs)
setup(name = PKGNAME,
      version = '0.2.0',
      description = 'Python bindings to casacore Quanta',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['quanta','casacore', 'unit conversion'],
      long_description = '''
This is a python module to do unit conversion using the casacore Quanta c++ library.
''',
      packages = [ PKGNAME ],
      license = 'GPL',
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext})

      
