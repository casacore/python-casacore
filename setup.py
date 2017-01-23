#!/usr/bin/env python
"""
Setup script for the CASACORE python wrapper.
"""
import os
import sys
import platform
from setuptools import setup, Extension, find_packages
from distutils.sysconfig import get_config_vars
from distutils import ccompiler
import argparse
from ctypes.util import find_library

from casacore import __version__


def find_library_file(libname):
    ''' Try to get the directory of the specified library.
    It adds to the search path the library paths given to distutil's build_ext.
    This is not guaranteed to work, but should give the correct directory
    for most configurations. Should be used only for dependency tracking.
    '''
    # Use a dummy argument parser to get user specified library dirs
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--library-dirs", "-L", default='')
    args, unknown = parser.parse_known_args()
    user_libdirs = args.library_dirs.split(':')
    # Append default search path (not a complete list)
    libdirs = user_libdirs+['/usr/local/lib', '/usr/lib']
    compiler = ccompiler.new_compiler()
    return compiler.find_library_file(libdirs, libname)


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


def find_boost():
    # Find correct boost-python library.
    system = platform.system()
    if system == 'Linux':
        # Use version suffix if present
        boost_python = 'boost_python-py%s%s' % (sys.version_info[0], sys.version_info[1])
        if not find_library(boost_python):
            boost_python = "boost_python"
    elif system == 'Darwin':
        if sys.version_info[0] == 2:
            boost_python = "boost_python-mt"
        else:
            boost_python = "boost_python3-mt"
    return boost_python


boost_python = find_boost()
if not find_library(boost_python):
    raise Exception("can't find boost library")


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
    ),
    (
        "casacore.ms._ms",
        ["src/pytabledesc.cc", "src/pyms.cc", "src/ms.cc"],
        ["src/ms.h"],
        ["casa_ms", boost_python, casa_python],
    )

)

# Find casacore libpath
found_casacore_libraries=True;
if not find_library_file('casa_casa'):
    print("Warning: could not find casa library dir for dependency tracking.")
    print("Possibly not rebuilding. Specify --force to force a rebuild.")
    found_casacore_libraries=False

extensions = []
for meta in extension_metas:
    name, sources, depends, libraries = meta

    # Add dependency on casacore libraries to trigger rebuild at casacore update
    if found_casacore_libraries:
        for library in libraries:
            if 'casa' in library:
                found_lib=find_library_file(library)
                if found_lib:
                    depends=depends+[found_lib]

    extensions.append(Extension(name=name, sources=sources, depends=depends,
                                libraries=libraries))

setup(name='python-casacore',
      version=__version__,
      description='A wrapper around CASACORE, the radio astronomy library',
      install_requires=['numpy', 'argparse'],
      author='Gijs Molenaar',
      author_email='gijs@pythonic.nl',
      url='https://github.com/casacore/python-casacore',
      keywords=['pyrap', 'casacore', 'utilities', 'astronomy'],
      long_description=read('README.rst'),
      packages=find_packages(),
      ext_modules=extensions,
      license='GPL')
