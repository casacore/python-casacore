#!/usr/bin/env python
"""
Setup script for the CASACORE python wrapper.
"""
import os
import sys
import warnings
from setuptools import setup, Extension, find_packages
from distutils.sysconfig import get_config_vars
from distutils.command import build_ext as build_ext_module
from distutils import ccompiler
from distutils.version import LooseVersion
import argparse
import ctypes
from os.path import join, dirname

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
    lib_dirs = args.library_dirs.split(':')

    if 'LD_LIBRARY_PATH' in os.environ:
        lib_dirs += os.environ['LD_LIBRARY_PATH'].split(':')

    # Append default search path (not a complete list)
    lib_dirs += [join(sys.prefix, 'lib'),
                 '/usr/local/lib',
                 '/usr/lib64',
                 '/usr/lib',
                 '/usr/lib/x86_64-linux-gnu']

    compiler = ccompiler.new_compiler()
    return compiler.find_library_file(lib_dirs, libname)


def read(fname):
    return open(join(dirname(__file__), fname)).read()


def find_boost():
    """
    Find the name and path of boost-python

    Returns:
        library_name, e.g. 'boost_python-py36'        (a guess if boost is not found)
        library_dir,  e.g. '/opt/local/boost/lib'     ('' if boost is not found)
        include_dir,  e.g. '/opt/local/boost/include' ('' if boost is not found)
    """
    short_version = "{}{}".format(sys.version_info[0], sys.version_info[1])
    major_version = str(sys.version_info[0])

    # Prefer libraries with python version in their name over unversioned variants
    boostlibnames = ['boost_python-py' + short_version,
                     'boost_python' + short_version,
                     'boost_python' + major_version,
                     'boost_python',
                     ]
    # The -mt (multithread) extension is used on macOS but not Linux.
    # Look for it first to avoid ending up with a single-threaded version.
    boostlibnames = sum([[name + '-mt', name] for name in boostlibnames], [])

    for libboostname in boostlibnames:
        found_lib = find_library_file(libboostname)
        if found_lib:
            libdir = dirname(found_lib)
            includedir = join(dirname(libdir), "include")
            return libboostname, libdir, includedir

    warnings.warn(no_boost_error)
    return boostlibnames[0], '', ''


def find_casacore_version():
    """
    Find the version of casacore, or None if it's not found
    """
    if sys.version_info[0] == 2:
        casa_python = 'casa_python'
    else:
        casa_python = 'casa_python3'

    # Find casacore libpath
    libcasacasa = find_library_file('casa_casa')

    casacoreversion = None
    if libcasacasa:
        # Get version number from casacore
        try:
            libcasa = ctypes.cdll.LoadLibrary(libcasacasa)
            getCasacoreVersion = libcasa.getVersion
            getCasacoreVersion.restype = ctypes.c_char_p
            casacoreversion = getCasacoreVersion().decode('utf-8')
        except:
            # getVersion was fixed in casacore 2.3.0
            pass

    return casacoreversion


def find_casacore():
    """
    Find the name and path of casacore

    Returns:
        library_name, e.g. 'casa_python3'
        library_dir,  e.g. '/opt/local/casacore/lib'     ('' if casacore is not found)
        include_dir,  e.g. '/opt/local/casacore/include' ('' if casacore is not found)
    """
    if sys.version_info[0] == 2:
        casa_python = 'casa_python'
    else:
        casa_python = 'casa_python3'

    # Find casacore libpath
    libcasacasa = find_library_file('casa_casa')

    libdir = ''
    includedir = ''
    if libcasacasa:
        libdir = dirname(libcasacasa)
        includedir = join(dirname(libdir), "include")
    else:
        warnings.warn(no_casacore_error)

    return casa_python, libdir, includedir


def get_extensions():
    boost_python_libname, boost_python_libdir, boost_python_includedir = find_boost()
    casa_python_libname, casa_libdir, casa_includedir = find_casacore()

    extension_metas = (
        # name, sources, depends, libraries
        (
            "casacore.fitting._fitting",
            ["src/fit.cc", "src/fitting.cc"],
            ["src/fitting.h"],
            ['casa_scimath', 'casa_scimath_f', boost_python_libname, casa_python_libname],
        ),
        (
            "casacore.functionals._functionals",
            ["src/functional.cc", "src/functionals.cc"],
            ["src/functionals.h"],
            ['casa_scimath', 'casa_scimath_f', boost_python_libname, casa_python_libname],
        ),
        (
            "casacore.images._images",
            ["src/images.cc", "src/pyimages.cc"],
            ["src/pyimages.h"],
            ['casa_images', 'casa_coordinates',
             'casa_fits', 'casa_lattices', 'casa_measures',
             'casa_scimath', 'casa_scimath_f', 'casa_tables', 'casa_mirlib',
             boost_python_libname, casa_python_libname]
        ),
        (
            "casacore.measures._measures",
            ["src/pymeas.cc", "src/pymeasures.cc"],
            ["src/pymeasures.h"],
            ['casa_measures', 'casa_scimath', 'casa_scimath_f', 'casa_tables',
             boost_python_libname, casa_python_libname]
        ),
        (
            "casacore.quanta._quanta",
            ["src/quanta.cc", "src/quantamath.cc", "src/quantity.cc",
             "src/quantvec.cc"],
            ["src/quanta.h"],
            ["casa_casa", boost_python_libname, casa_python_libname],
        ),
        (
            "casacore.tables._tables",
            ["src/pytable.cc", "src/pytableindex.cc", "src/pytableiter.cc",
             "src/pytablerow.cc", "src/tables.cc", "src/pyms.cc"],
            ["src/tables.h"],
            ['casa_derivedmscal', 'casa_meas', 'casa_ms', 'casa_tables', boost_python_libname, casa_python_libname],
        ),
        (
            "casacore._tConvert",
            ["tests/tConvert.cc"],
            [],
            [boost_python_libname, casa_python_libname],
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

        library_dirs = [lib for lib in (boost_python_libdir, 
                                        casa_libdir) if lib]
        include_dirs = [inc for inc in (boost_python_includedir,
                                        casa_includedir) if inc]

        extensions.append(Extension(name=name, sources=sources,
                                    depends=depends, libraries=libraries,
                                    library_dirs=library_dirs,
                                    include_dirs=include_dirs,
                                    # Since casacore 3.0.0 we have to be C++11
                                    extra_compile_args=['-std=c++11']))
    return extensions


# remove the strict-prototypes warning during compilation
(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
)



class my_build_ext(build_ext_module.build_ext):
    def run(self):
        casacoreversion = find_casacore_version()
        if casacoreversion is not None and  LooseVersion(casacoreversion) < LooseVersion(__mincasacoreversion__):
            errorstr = "Your casacore version is too old. Minimum is " + __mincasacoreversion__ + \
                       ", you have " + casacoreversion
            if casacoreversion == "2.5.0":
                errorstr += " or 3.0.0 (which shipped in KERN5, incorrectly reporting itself as 2.5.0)"
            raise RuntimeError(errorstr)

        build_ext_module.build_ext.run(self)

setup(name='python-casacore',
      version=__version__,
      description='A wrapper around CASACORE, the radio astronomy library',
      install_requires=['numpy', 'six'],
      author='Gijs Molenaar',
      author_email='gijs@pythonic.nl',
      url='https://github.com/casacore/python-casacore',
      keywords=['pyrap', 'casacore', 'utilities', 'astronomy'],
      long_description=read('README.rst'),
      long_description_content_type='text/x-rst',
      packages=find_packages(),
      ext_modules=get_extensions(),
      cmdclass={'build_ext': my_build_ext},
      license='LGPL')
