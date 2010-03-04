import glob
from setuptools import setup, find_packages
from setupext import casacorebuild_ext
from setupext import assay

PKGNAME = "pyrap.util"

setup(name = PKGNAME,
      version = '0.1.0',
      description = 'Utilities for the pyrap module',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'http://code.google.com/p/pyrap',
      keywords = ['pyrap','casacore', 'utilities'],
      long_description = '''
This is a python module for various utilities shared by the different pyrap modules.
''',
      packages = find_packages(),
      namespace_packages = ["pyrap"],
      cmdclass={'build_ext': casacorebuild_ext, 'test': assay},
      license = 'GPL',
      zip_safe = 0)
