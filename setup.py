#!/usr/bin/env python
"""
Setup script for the CASACORE python wrapper.
"""
import os
import sys
from setuptools import setup, Extension, find_packages
from distutils.sysconfig import get_config_vars
from ctypes.util import find_library

from casacore import __version__


# remove the strict-prototypes warning during compilation
(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.version_info[0] == 2:
    casa_python = 'casa_python'
else:
    casa_python = 'casa_python3'

# Find correct boost-python library.
# Use version suffix if present
boost_pyversuffix = '-py%s%s' % (sys.version_info[0], sys.version_info[1])
if find_library("boost_python" + boost_pyversuffix) is None:
    boost_pyversuffix = ""

# If boost libraries with -mt suffix exist, use those
if find_library("boost_python-mt" + boost_pyversuffix) is None:
  boost_python = "boost_python"+boost_pyversuffix
else:
  boost_python = "boost_python-mt"+boost_pyversuffix

extension_metas = (
    # name, sources, depends, libraries
    (
        "casacore.fitting._fitting",
        ["src/fit.cc", "src/fitting.cc"],
        ["src/fitting.h"],
        ['casa_scimath', 'casa_scimath_f', boost_python, casa_python],
    ),
    (
        "casacore.functionals._functionals",
        ["src/functional.cc", "src/functionals.cc"],
        ["src/functionals.h"],
        ['casa_scimath', 'casa_scimath_f', boost_python, casa_python],
    ),
    (
        "casacore.images._images",
        ["src/images.cc", "src/pyimages.cc"],
        ["src/pyimages.h"],
        ['casa_images', 'casa_coordinates',
         'casa_fits', 'casa_lattices', 'casa_measures',
         'casa_scimath', 'casa_scimath_f', 'casa_tables', 'casa_mirlib',
         boost_python, casa_python]
    ),
    (
        "casacore.measures._measures",
        ["src/pymeas.cc", "src/pymeasures.cc"],
        ["src/pymeasures.h"],
        ['casa_measures', 'casa_scimath', 'casa_scimath_f', 'casa_tables',
         boost_python, casa_python]
    ),
    (
        "casacore.quanta._quanta",
        ["src/quanta.cc", "src/quantamath.cc", "src/quantity.cc",
            "src/quantvec.cc"],
        ["src/quanta.h"],
        ["casa_casa", boost_python, casa_python],
    ),
    (
        "casacore.tables._tables",
        ["src/pytable.cc", "src/pytableindex.cc", "src/pytableiter.cc",
         "src/pytablerow.cc", "src/tables.cc"],
        ["src/tables.h"],
        ['casa_tables', boost_python, casa_python],
    )
)


extensions = []
for meta in extension_metas:
    name, sources, depends, libraries = meta
    extensions.append(Extension(name=name, sources=sources, depends=depends,
                                libraries=libraries))


setup(name='python-casacore',
      version=__version__,
      description='A wrapper around CASACORE, the radio astronomy library',
      author='Gijs Molenaar',
      author_email='gijs@pythonic.nl',
      url='https://github.com/casacore/python-casacore',
      keywords=['pyrap', 'casacore', 'utilities', 'astronomy'],
      long_description=read('README.rst'),
      packages=find_packages(),
      ext_modules=extensions,
      license='GPL')
