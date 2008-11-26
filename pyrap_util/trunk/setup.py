import glob
from setuptools import setup, find_packages

PKGNAME = "pyrap.util"

setup(name = PKGNAME,
      version = 'trunk',
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
      license = 'GPL',
      zip_safe = 0)
