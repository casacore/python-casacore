#!/usr/bin/env python
"""
Setup script for the CASACORE python wrapper.
"""
import os
import sys
import warnings
from setuptools import setup, Extension, find_packages
from distutils.sysconfig import get_config_vars
from distutils import ccompiler
from distutils.version import LooseVersion
import argparse
import ctypes

from casacore import __version__, __mincasacoreversion__

no_boost_error = """
Could not find a Python boost library! Please use your package manager to install boost.

Or install it manually:

http://boostorg.github.io/python/doc/html/index.html
"""

no_casacore_error = """Could not find Casacore!

Casacore is a critical requirement. Please install Casacore using a package manager or install it manually.
You can find installation instructions on:

 https://github.com/casacore/casacore

If you have Casacore installed in a non default location, you need to specify the location:

$ python setup.py build_ext -I/opt/casacore/include:/other/include/path -L/opt/casacore/lib

Don't give up!
"""


def find_library_file(libname):
    """
    Try to get the directory of the specified library.
    It adds to the search path the library paths given to distutil's build_ext.
    """
    # Use a dummy argument parser to get user specified library dirs
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--library-dirs", "-L", default='')
    args, unknown = parser.parse_known_args()
    user_lib_dirs = args.library_dirs.split(':')
    # Append default search path (not a complete list)
    lib_dirs = user_lib_dirs + [os.path.join(sys.prefix, 'lib'),
                              '/usr/local/lib',
                              '/usr/lib',
                              '/usr/lib/x86_64-linux-gnu']

    if 'LD_LIBRARY_PATH' in os.environ:
        lib_dirs += os.environ['LD_LIBRARY_PATH'].split(':')

    compiler = ccompiler.new_compiler()
    return compiler.find_library_file(lib_dirs, libname)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_boost():
    """Find the name of the boost-python library. Returns None if none is found."""
    short_version = "{}{}".format(sys.version_info[0], sys.version_info[1])
    boostlibnames = ['boost_python-py' + short_version,
                     'boost_python' + short_version,
                     'boost_python',
                     ]
    # The -mt (multithread) extension is used on macOS but not Linux.
    # Look for it first to avoid ending up with a single-threaded version.
    boostlibnames = [name + '-mt' for name in boostlibnames] + boostlibnames
    for libboostname in boostlibnames:
        if find_library_file(libboostname):
            return libboostname
    warnings.warn(no_boost_error)
    return boostlibnames[0]


def find_casacore():
    if sys.version_info[0] == 2:
        casa_python = 'casa_python'
    else:
        casa_python = 'casa_python3'

    # Find casacore libpath
    libcasacasa = find_library_file('casa_casa')

    if libcasacasa:
        # Get version number from casacore
        try:
            libcasa = ctypes.cdll.LoadLibrary(libcasacasa)
            getCasacoreVersion = libcasa.getVersion
            getCasacoreVersion.restype = ctypes.c_char_p
            casacoreversion = getCasacoreVersion()
        except:
            # getVersion was fixed in casacore 2.3.0
            warnings.warn("Your casacore version is older than 2.3.0! You need to upgrade your casacore.")
        else:
            if LooseVersion(casacoreversion.decode()) < LooseVersion(__mincasacoreversion__):
                warnings.warn("Your casacore version is too old. Minimum is " + __mincasacoreversion__)

    if not find_library_file(casa_python):
        warnings.warn(no_casacore_error)
    return casa_python


def get_extensions():

    boost_python = find_boost()
    casa_python = find_casacore()

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
             "src/pytablerow.cc", "src/tables.cc", "src/pyms.cc"],
            ["src/tables.h"],
            ['casa_derivedmscal', 'casa_meas', 'casa_ms', 'casa_tables', boost_python, casa_python],
        ),
        (
            "casacore._tConvert",
            ["tests/tConvert.cc"],
            [],
            [boost_python, casa_python],
        )
    )

    extensions = []
    for meta in extension_metas:
        name, sources, depends, libraries = meta

        # Add dependency on casacore libraries to trigger rebuild at casacore update
        for library in libraries:
            if library and 'casa' in library:
                found_lib = find_library_file(library)
                if found_lib:
                    depends = depends + [found_lib]

        extensions.append(Extension(name=name, sources=sources,
                                    depends=depends, libraries=libraries,
                                    # Since casacore 3.0.0 we have to be C++11
                                    extra_compile_args=['-std=c++11']))
    return extensions


# remove the strict-prototypes warning during compilation
(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
)


setup(name='python-casacore',
      version=__version__,
      description='A wrapper around CASACORE, the radio astronomy library',
      install_requires=['numpy', 'argparse', 'future', 'six'],
      author='Gijs Molenaar',
      author_email='gijs@pythonic.nl',
      url='https://github.com/casacore/python-casacore',
      keywords=['pyrap', 'casacore', 'utilities', 'astronomy'],
      long_description=read('README.rst'),
      long_description_content_type='text/x-rst',
      packages=find_packages(),
      ext_modules=get_extensions(),
      license='GPL')
