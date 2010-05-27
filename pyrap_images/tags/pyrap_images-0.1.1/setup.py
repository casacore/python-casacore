import glob
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setupext import casacorebuild_ext
from setupext import assay

PKGNAME = "pyrap.images"
EXTNAME = "_images"
casalibs = ['casa_images', 'casa_components', 'casa_coordinates',
            'casa_fits', 'casa_lattices', 'casa_measures',
            'casa_scimath', 'casa_scimath_f', 'casa_tables', 'casa_mirlib'] 
# casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME), 
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs)

from setuptools import Command


setup(name = PKGNAME,
      version = '0.1.1',
      description = 'Python bindings to casacore Images',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['images','casacore'],
      long_description = '''
This is a python module to access the casacore c++ images package
''',
      packages = find_packages(),
      namespace_packages = ["pyrap"],
      license = 'GPL',
      zip_safe = 0,
      ext_modules =[ casaextension ],
      cmdclass={'build_ext': casacorebuild_ext, 'test': assay})
      
