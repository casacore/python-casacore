import glob
from distutils.core import setup, Extension
from setupext import casacorebuild_ext

PKGNAME = "pyrap_tables"
EXTNAME = "_tables"
casalibs = ['casa_tables'] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs)

setup(name = PKGNAME,
      version = '0.1.0',
      description = 'Python bindings to casacore Tables',
      author = 'Ger van Diepen',
      author_email = 'diepen@astron.nl',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['tables','casacore'],
      long_description = '''
This is a python module to access the casacore c++ tables package
''',
      packages = [ PKGNAME ],
      license = 'GPL',
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext})

      
