#!/usr/bin/env python
"""
Setup script for the CASACORE python wrapper.
"""
import os
import glob
from setuptools import setup, find_packages, Extension
from casacore import __version__


extension_metas = (
    # name, extname, sources, depends, casalibs
    (
        "pyrap.fitting",
        "_fitting",
        ["src/fit.cc", "src/fitting.cc"],
        ["src/fitting.h"],
        ['casa_scimath', 'casa_scimath_f'],
    ),
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

for meta in extension_metas:
    name, extname, sources, depends, casalibs = meta
    extension = Extension(name="%s.%s" % (name, extname),
                          sources=sources,
                          depends=depends,
                          libraries=casalibs)

"""
PKGNAME = "pyrap.functionals"
EXTNAME = "_functionals"
casalibs = ['casa_scimath', 'casa_scimath_f'] # casa_casa is added by default

casaextension = Extension(name = "%s.%s" % (PKGNAME, EXTNAME),
                          sources = glob.glob('src/*.cc'),
                          depends = glob.glob('src/*.h'),
                          libraries = casalibs )


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


PKGNAME = "pyrap.measures"
EXTNAME = "_measures"
casalibs = ['casa_measures', 'casa_scimath', 'casa_scimath_f',
            'casa_tables',] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME),
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs)


PKGNAME = "pyrap.quanta"
EXTNAME = "_quanta"
casalibs = [] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME),
                          sources = glob.glob('src/*.cc'),
                          depends = glob.glob('src/*.h'),
                          libraries = casalibs)


PKGNAME = "pyrap.tables"
EXTNAME = "_tables"
casalibs = ['casa_tables'] # casa_casa is added by default

casaextension = Extension(name="%s.%s" % (PKGNAME, EXTNAME),
			sources = glob.glob('src/*.cc'),
			depends = glob.glob('src/*.h'),
			libraries= casalibs)

"""
setup(name='casacore',
      version=__version__,
      description='A wrapper around CASACORE, the radio astronomy library',
      author='Gijs Molenaar',
      author_email='gijs@pythonic.nl',
      url='https://github.com/gijzelaerr/casacore-python',
      keywords=['pyrap', 'casacore', 'utilities', 'astronomoy'],
      long_description=read('README.rst'),
      packages=find_packages(),
      ext_modules=[extension],
      license='GPL')
