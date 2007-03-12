import os
import sys
import distutils.sysconfig

# Put the package name here, e.g. casa, tables
PACKAGE="pyrap"

# general options
opts = Options( 'options.cfg', ARGUMENTS )
opts.Add(ListOption("build", "The build type", 
		    "opt", ["opt", "dbg"]))
opts.Add(ListOption("libtype", "The type of library to build", 
		    "shared", ["static", "shared"]))
opts.Add(BoolOption("tests", "Build the tests?", False))
opts.Add(PathOption("casacoredir", "The location of casacore/casa",
		    "/usr"))
opts.Add(("CC", "The c compiler", None))
opts.Add(("CXX", "The c++ compiler", None))
opts.Add(("numpy", "The include dir for numpy", 
	  distutils.sysconfig.get_python_inc()))

env = Environment(ENV = { 'PATH' : os.environ[ 'PATH' ],
			  'HOME' : os.environ[ 'HOME' ] 
			  },
		  options=opts
		  )
# keep a local sconsign database, rather than in very directory
env.SConsignFile()

env["PACKAGE"] = PACKAGE
env["casaincdir"] = [os.path.join(env["casacoredir"],"include","casacore")]
env["casalibdir"] = [os.path.join(env["casacoredir"],"lib")]
env["casashrdir"] = [os.path.join(env["casacoredir"],"share","casacore")]

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
    if env['PLATFORM'] == "darwin":
        print "Platform darwin - using python framework"
        conf.env.Append(FRAMEWORKS=["Python"])
    else:
	if not conf.CheckLib(library=pylib, language='c'): Exit(1)

    conf.env.AppendUnique(CPPPATH=env["numpy"])
    if not conf.CheckHeader("numpy/config.h"):
	Exit(1)
    else:
	conf.env.Append(CPPDEFINES="-DAIPS_USENUMPY=1")
    if not conf.CheckLibWithHeader('boost_python', 
				   'boost/python.hpp', 'c++'): 
	Exit(1)

    env = conf.Finish()

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
 

