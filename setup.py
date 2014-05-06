#!/usr/bin/env python
"""
Setup script for the CASACORE python wrapper.
"""
import os
from setuptools import setup, find_packages, Extension
from distutils.sysconfig import get_config_vars
from casacore import __version__

# this looks hacky but it removes the strict-prototypes warning
# durng compilation
(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
)

# below is the binary python module stuff
extension_metas = (
    # name, extname, sources, depends, casalibs
    (
        "pyrap.fitting",
        "_fitting",
        ["src/fit.cc", "src/fitting.cc"],
        ["src/fitting.h"],
        ['casa_scimath', 'casa_scimath_f'],
    ),
    (
        "pyrap.functionals",
        "_functionals",
        ["src/functional.cc", "src/functionals.cc"],
        ["src/functionals.h"],
        ['casa_scimath', 'casa_scimath_f'],
    ),
    (
        "pyrap.images",
        "_images",
        ["src/images.cc", "src/pyimages.cc"],
        ["src/pyimages.h"],
        ['casa_images', 'casa_components', 'casa_coordinates',
            'casa_fits', 'casa_lattices', 'casa_measures',
            'casa_scimath', 'casa_scimath_f', 'casa_tables', 'casa_mirlib']
    ),
    (
        "pyrap.measures",
        "_measures",
        ["src/pymeas.cc", "src/pymeasures.cc"],
        ["src/pymeasures.h"],
        ['casa_measures', 'casa_scimath', 'casa_scimath_f', 'casa_tables']
    ),
    (
        "pyrap.quanta",
        "_quanta",
        ["src/quanta.cc", "src/quantamath.cc", "src/quantity.cc",
            "src/quantvec.cc"],
        ["src/quanta.h"],
        [],
    ),
    (
        "pyrap.tables",
        "_tables",
        ["src/pytable.cc", "src/pytableindex.cc", "src/pytableiter.cc",
         "src/pytablerow.cc", "src/tables.cc"],
        ["src/tables.h"],
        ['casa_tables'],
    )
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

extensions = []
for meta in extension_metas:
    name, extname, sources, depends, casalibs = meta
    extensions.append(Extension(name="%s.%s" % (name, extname),
                                sources=sources,
                                depends=depends,
                                libraries=casalibs))


setup(name='casacore',
      version=__version__,
      description='A wrapper around CASACORE, the radio astronomy library',
      author='Gijs Molenaar',
      author_email='gijs@pythonic.nl',
      url='https://github.com/gijzelaerr/casacore-python',
      keywords=['pyrap', 'casacore', 'utilities', 'astronomoy'],
      long_description=read('README.rst'),
      packages=find_packages(),
      ext_modules=extensions,
      license='GPL')
