import glob
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setupext import casacorebuild_ext

PKGNAME = "pyrap.tables"
EXTNAME = "_tables"
casalibs = ['casa_tables'] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs)

setup(name = PKGNAME,
      version = 'trunk',
      description = 'Python bindings to casacore Tables',
      author = 'Ger van Diepen',
      author_email = 'diepen@astron.nl',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['tables','casacore'],
      long_description = '''
This is a python module to access the casacore c++ tables package
''',
      packages = find_packages(),
      namespace_packages = ["pyrap"],
      license = 'GPL',
      zip_safe = 0,
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext})
      
