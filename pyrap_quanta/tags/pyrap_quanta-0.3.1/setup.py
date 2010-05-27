import glob
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setupext import casacorebuild_ext
from setupext import assay

PKGNAME = "pyrap.quanta"
EXTNAME = "_quanta"
casalibs = [] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
                          sources = glob.glob('src/*.cc'),
                          depends = glob.glob('src/*.h'),
                          libraries = casalibs)
setup(name = PKGNAME,
      version = '0.3.1',
      description = 'Python bindings to casacore Quanta',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['quanta','casacore', 'unit conversion'],
      long_description = '''
This is a python module to do unit conversion using the casacore Quanta c++ library.
''',
      packages = find_packages(),
      namespace_packages = ["pyrap"],
      license = 'GPL',
      zip_safe = 0,
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext, "test": assay})
