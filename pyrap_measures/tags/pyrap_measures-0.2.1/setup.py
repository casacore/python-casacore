import glob
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setupext import casacorebuild_ext
from setupext import assay

PKGNAME = "pyrap.measures"
EXTNAME = "_measures"
casalibs = ['casa_measures', 'casa_scimath', 'casa_scimath_f', 
            'casa_tables',] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs)
setup(name = PKGNAME,
      version = '0.2.1',
      description = 'Python bindings to casacore Measures',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['measures','casacore'],
      long_description = '''
This is a python module to access the casacore c++ measures package
''',
      packages = find_packages(),
      namespace_packages = ["pyrap"],
      zip_safe = 0,
      license = 'GPL',
      ext_modules =[ casaextension ],
      install_requires = ['pyrap.quanta'],
      cmdclass={'build_ext': casacorebuild_ext, 'test': assay})
