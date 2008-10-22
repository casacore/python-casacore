#!/usr/bin/env python

import sys
import os
import re
import string
import optparse

usage = "usage: %prog [options] <packagename>"
parser = optparse.OptionParser(usage, description="This scripts builds libpyrap (the casacore to python conversion library) and all pyrap_* python bindings to casacore")

parser.add_option('--boostroot', dest='boost',
                  default="",
                  type="string",
                  help="Root directory of boost python (default is /usr)")

parser.add_option('--casacoreroot', dest='casacore',
                  default=None,
                  type="string",
                  help="Root directory of casacore (default is /usr/local)")

parser.add_option('--lapackroot', dest='lapack',
                  default=None,
                  type="string",
                  help="Root directory of lapack (default is /usr/local)")

parser.add_option('--enable-hdf5', dest='enable_hdf5',
                  default=False, action='store_true',
                  help="Enable the optional hdf5 support")

parser.add_option('--hdf5root', dest='hdf5',
                  default=None,
                  type="string",
                  help="Root directory of hdf5 (default is /usr/local)")

parser.add_option('--cfitsioroot', dest='cfitsio',
                  default=None,
                  type="string",
                  help="Root directory of cfitsio (default is /usr/local)")

parser.add_option('--wcsroot', dest='wcs',
                  default=None,
                  type="string",
                  help="Root directory of wcs (default is /usr/local)")

parser.add_option('--f2clib', dest='f2clib',
                  default=None,
                  type="string",
                  help="Fortran to c library (default is gfortran)")
parser.add_option('--f2c', dest='f2c',
                  default=None,
                  type="string",
                  help="Root directory of Fortran to c library (default is /usr)")

parser.add_option('--prefix', dest='prefix',
                  default=None,
                  type="string",
                  help="Install location for libpyrap (default is /usr/local)")

parser.add_option('--python-prefix', dest='pyprefix',
                  default=None,
                  type="string",
                  help="Install location for python modules (default is python site-packages)")

parser.add_option('--universal', dest='universal',
                  default=None,
                  type="string",
                  help="i386, ppc, x86_64 and ppc64")

parser.add_option('--numpyincdir', dest='numpyincdir',
                  default=None,
                  type="string",
                  help="Location of numpy include directory (default is to autodetect)")
parser.add_option('-r', '--release', dest='release', type="choice",
                  choices=["current", "trunk"], 
                  default="current",
                  help="Select RELEASE from: %s [default=%%default]" % \
                  string.join(["current", "trunk"], ", "))


# parse command line options
(opts, args) = parser.parse_args()

deps = {'pyrap_quanta' : None,
	'pyrap_tables': None,
	'pyrap_measures': ['pyrap_quanta'],
	'pyrap_functionals': None,
	'pyrap_fitting': ['pyrap_functionals'],
	'pyrap_images': None,
	}

def get_libs(pkg, version='trunk'):
    validver = ['current', 'trunk']
    if pkg not in deps.keys():
	return
    pkgs = [pkg]
    def getpkg(pkg, pgs):
	plist =  deps.get(pkg)
	if plist is None: return
	for p in plist:
	    pgs.insert(0, p)
	    getpkg(p, pgs)
    getpkg(pkg, pkgs)
    outpkgs = []
    # strip off duplicates
    for i in pkgs:
	if i not in outpkgs:
	    outpkgs.append(i)
    return outpkgs

def run_python(pkg, args):
    cwd = os.getcwd()
    os.chdir(os.path.join(pkg, args.release))
    setupscript = "setup.py"
    buildargs = ""
    installdir = ""
    if args.casacore:
        buildargs += " --casacore=%s" %  args.casacore
    if args.lapack:
        buildargs += " --lapack=%s" %  args.lapack
    if args.enable_hdf5:
        buildargs += " --enable-hdf5"
    if args.hdf5:
        buildargs += " --hdf5=%s" %  args.hdf5
    if args.cfitsio:
        buildargs += " --cfitsio=%s" %  args.cfitsio
    if args.wcs:
        buildargs += " --wcs=%s" %  args.wcs
    if args.boost:
        buildargs += " --boost=%s" %  args.boost
    if args.f2clib:
        buildargs += " --f2clib=%s" %  args.f2clib
    if args.f2c:
        buildargs += " --f2c=%s" %  args.f2c
    if args.prefix:
        buildargs += " --pyrap=%s" %  args.prefix
    if args.pyprefix:
        installdir = "--prefix=%s" % args.pyprefix

    print "******* python %s build_ext %s" % (setupscript, buildargs)
    try:
        err = os.system("python %s build_ext %s" % (setupscript, buildargs))
        if err:
            sys.exit(1)
        err = os.system("python %s install %s" % (setupscript, installdir))
        if err:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit()
    os.chdir(cwd)

def run_scons(target, args):
    cwd = os.getcwd()
    os.chdir(os.path.join(target, args.release))
    if os.path.exists("options.cfg"):
        os.remove("options.cfg")
    command = "scons "
    # copy the command line args into the new command
    pfx = None
    tests = False
    if args.casacore:
        command += " casacoreroot=%s" %  args.casacore
    if args.numpyincdir:
        command += " numpyincdir=%s" %  args.numpyincdir
    if args.boost:
        command += " boostroot=%s" %  args.boost
    if args.prefix:
        command += " prefix=%s" %  args.prefix
    if args.universal:
        command += " universal=%s" %  args.universal
    try:
        failed = os.system(command + " shared install")
    except KeyboardInterrupt:
        sys.exit()
    if failed:
        sys.exit(failed)
        sys.stdout.flush()
    os.chdir(cwd)

# build all by default
tobuild = ['pyrap_quanta', 'pyrap_tables', 'pyrap_measures',
           'pyrap_functionals', 'pyrap_fitting', 'pyrap_images']
for k in deps.keys():
    k = k.rstrip("/")
    if k in args:
	tobuild = get_libs(k)
	args.remove(k)

run_scons("libpyrap", opts)
for pkg in tobuild:
    run_python(pkg, opts)
