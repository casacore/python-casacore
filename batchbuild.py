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
                  help="true or false")

parser.add_option('--numpyincdir', dest='numpyincdir',
                  default=None,
                  type="string",
                  help="Location of numpy include directory (default is to autodetect)")
parser.add_option('-e', '--eggs', dest='useegg',
                  action="store_true", default=False,
                  help="Use easy_install to install python modules as eggs")

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
    print os.path.abspath(".")
    setupscript = "setup.py"
    buildargs = ""
    installdir = ""
    if args.casacore:
        buildargs += " --casacore=%s" %  args.casacore
    if args.boost:
        buildargs += " --boost=%s" %  args.boost
    if args.f2clib:
        buildargs += " --f2clib=%s" %  args.f2clib
    if args.f2c:
        buildargs += " --f2c=%s" %  args.f2c
    if args.prefix:
        buildargs += " --pyrap=%s" %  args.prefix
    if args.useegg:
        setupscript = "setupegg.py"
    if args.pyprefix:
        installdir = "--prefix=%s" % args.pyprefix
    os.system("python %s build_ext %s" % (setupscript, buildargs))
    os.system("python %s install %s" % (setupscript, installdir))
    os.chdir(cwd)

def run_scons(target, args):
    cwd = os.getcwd()
    os.chdir(os.path.join(target, args.release))
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
        failed = os.system(command + " install")
    except KeyboardInterrupt:
        sys.exit()
    if failed:
        sys.exit(failed)
        sys.stdout.flush()
    os.chdir(cwd)

# build all by default
tobuild = ['pyrap_quanta', 'pyrap_tables', 'pyrap_measures',
           'pyrap_functionals', 'pyrap_fitting']
for k in deps.keys():
    k = k.rstrip("/")
    if k in args:
	tobuild = get_libs(k)
	args.remove(k)

run_scons("libpyrap", opts)
for pkg in tobuild:
    run_python(pkg, opts)
