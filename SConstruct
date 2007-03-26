import os
import sys
import distutils.sysconfig

# Put the package name here
PACKAGE="pyrap"

# general options
opts = Options( 'options.cfg', ARGUMENTS )
opts.Add(ListOption("build", "The build type", 
		    "opt", ["opt", "dbg"]))
opts.Add(ListOption("libtype", "The type of library to build", 
		    "shared", ["static", "shared"]))
opts.Add(BoolOption("tests", "Build the tests?", False))
opts.Add(("CC", "The c compiler", None))
opts.Add(("CXX", "The c++ compiler", None))
opts.Add(("CPPFLAGS", "Extra compiler flags ", None))
opts.Add(PathOption("casacoreroot", "The location of casacore",
		    "/usr/local"))
opts.Add(("numpyincdir", "The include dir for numpy", 
	  distutils.sysconfig.get_python_inc()))
opts.Add(("numarrayincdir", "The include dir for numarray", 
	  distutils.sysconfig.get_python_inc()))
opts.Add(("boostroot", "The root dir where boost is installed", None))
opts.Add(("boostlibdir", "The boost library location", None))
opts.Add(("boostincdir", "The boost header file location", None))


env = Environment(ENV = { 'PATH' : os.environ[ 'PATH' ],
			  'HOME' : os.environ[ 'HOME' ] 
			  },
		  options=opts
		  )
# keep a local sconsign database, rather than in very directory
env.SConsignFile()

env["PACKAGE"] = PACKAGE
env["casaincdir"] = [os.path.join(env["casacoreroot"],"include","casacore")]
env["casalibdir"] = [os.path.join(env["casacoreroot"],"lib")]
env["casashrdir"] = [os.path.join(env["casacoreroot"],"share","casacore")]

if not os.path.exists(os.path.join(env["casashrdir"][0], "casa.py")):
    print "Could not find casacore scons tools"
    Exit(1)

env.Tool('buildenv', env["casashrdir"])
env.Tool('utils', env["casashrdir"])
env.Tool('installer', env["casashrdir"])
env.Tool('casa', env["casashrdir"])
# add installer options, e.g. prefix
env.AddInstallerOptions( opts )
# add them into environment
opts.Update( env )
# cache them for the next run
opts.Save( 'options.cfg', env)
Help( opts.GenerateHelpText( env ) )


# Auto configure
if not env.GetOption('clean'):
    conf = Configure(env)
    conf.env.AppendUnique(LIBPATH=conf.env["casalibdir"])
    conf.env.AppendUnique(CPPPATH=conf.env["casaincdir"])
    if not conf.CheckLib('casa_casa', language='c++'):
	Exit(1)	
    conf.env.Append(CPPPATH=[distutils.sysconfig.get_python_inc()])
    if not conf.CheckHeader("Python.h", language='c'):
        Exit(1)
    pylib = 'python'+distutils.sysconfig.get_python_version()
    if env['PLATFORM'] == "darwin":
        print "Platform darwin - using python framework"
        conf.env.Append(FRAMEWORKS=["Python"])
    else:
	if not conf.CheckLib(library=pylib, language='c'): Exit(1)

    conf.env.AppendUnique(CPPPATH=env["numpyincdir"])
    hasnums = False
    if not conf.CheckHeader("numpy/config.h"):
	pass
    else:
	conf.env.Append(CPPDEFINES=["-DAIPS_USENUMPY=1"])
	hasnums = True
    conf.env.AppendUnique(CPPPATH=env["numarrayincdir"])
    if not conf.CheckHeader("numarray/numconfig.h"):
	pass
    else:
	conf.env.Append(CPPDEFINES=["-DAIPS_USENUMARRAY=1"])
	hasnums = True
    if not hasnums: 
	print "No numarray or numpy found."
	Exit(1)
    conf.env.AddCustomPackage('boost')
    if not conf.CheckLibWithHeader('boost_python', 
				   'boost/python.hpp', 'c++'): 
	Exit(1)

    env = conf.Finish()

# create the installer which handles installing the final build
installer = env.Installer()

# to find package based includes
env.Append(CPPPATH='#')

# add casa specific defines autodetected from platform
# currently works for darwin/linux(_x86_64), cray doesn't work
# because PGI compiler needs a lot of environment variables
# Probably need to write a PGI builder 
env.AddCasaPlatform()
# Replace some builder commands (lex,yacc) with custom versions
env.CustomCasaCom()

for bopt in env["build"]:
    # create an environment copy with teh dbg/opt compiler flags
    buildenv = env.BuildEnv(bopt)
    # buildir name
    buildenv["BUILDDIR"] = Dir("#/build_%s/%s" % (env.PlatformIdent(), bopt))
    env.SConscript(["%s/SConscript" % env["PACKAGE"]], 
		   build_dir= buildenv["BUILDDIR"],
		   duplicate=0, exports=["buildenv", "installer"]) 
