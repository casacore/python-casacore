import sys
import os
import glob
import re
import platform
from  SCons.Variables import Variables
from SCons.Script import AddOption, GetOption

def get_libdir():
    if not platform.architecture()[0].startswith("64"):
        return "lib"
    dist = platform.dist()[0].lower()
    distdict = dict(suse='lib64', redhat='lib64')
    return distdict.get(dist, 'lib')

ARCHLIBDIR = get_libdir()

# try to autodetect numpy
def get_numpy_incdir():
    try:
        # try to find an egg
        from pkg_resources import require
        tmp = require("numpy")
        import numpy
        return numpy.__path__[0]+"/core/include"
    except Exception:
        # now try standard package
        try:
            import numpy
            return numpy.__path__[0]+"/core/include"
        except ImportError:
            pass
    return ""

def _to_list(xf):
    if xf.count(","):
        return xf.split(",")
    return xf.split()



class CLOptions(object):
    def __init__(self, env):
        self.opts = {}
        self.variables = []
        self.env = env

    def add_option(self, *args, **kw):
        AddOption(*args, **kw)
        key = kw.get('dest')
        value = GetOption(key)
        defvalue = kw.get('default')
        self.variables.append((key, '', defvalue))
        if value != defvalue:
            self.opts[key] = value

    def update(self, fname='options.cache'):
        if os.path.exists(fname) and not GetOption("silent") and\
                not GetOption("help"):
            print """Note: Restoring previous command-line options from '%s'.
      Please delete this file when trying to start from scratch."""% fname
        vars = Variables(fname, self.opts)
        vars.AddVariables(*self.variables)
        vars.Update(self.env)
        vars.Save(fname, self.env)

    def add_pkg_option(self, libid, root=None, lib=None, libdir=None, 
                  incdir=None, help=None):
        libname = lib or libid
        self.add_str_option(libid+"-lib", libname,
                       help="%s library name (default: %s)" % (libname, libname))
        self.add_str_option(libid+"-root", root,
                       help="%s package root" % libid)
        self.add_str_option(libid+"-incdir", incdir,
                       help="%s package 'include' directory (overwrites '-root')" % libid)
        self.add_str_option(libid+"-libdir", libdir,
                       help="%s package 'lib' directory (overwrites '-root')" \
                           % libid)

    def add_str_option(self, optname, default=None, help=None):
        envopt = optname.replace("-", "_")
        self.add_option("--%s" % optname, dest=envopt, type="string",
                        default=default, help=help)

    def add_comp_option(self, optname, default=None, help=None):
        self.add_option("--with-%s" % optname.lower(), dest=optname,
                        type="string", default=default, help=help)


def generate(env):

    def DarwinDevSdk():
        import platform        
        devpath = { "4" : "/Developer/SDKs/MacOSX10.4u.sdk",
                    "5" : "/Developer/SDKs/MacOSX10.5.sdk",
                    "6" : "/Developer/SDKs/MacOSX10.6.sdk" }
        version = platform.mac_ver()[0].split(".")
        if version[0] != '10' or int(version[1]) < 4:
            print "Only Mac OS X >= 10.4 is supported"
            env.Exit(1)
        return devpath[version[1]]
    env.DarwinDevSdk = DarwinDevSdk

    env["ARCHLIBDIR"] = ARCHLIBDIR
    def SGlob(pattern, excludedirs=[], recursive=False):
	# always exclude .svn
	excludedirs.append(".svn")
        path = env.GetBuildPath('SConscript').replace('SConscript', '')	
	if recursive:
	    # remove '*' from pattern is accidentally specified
	    pattern=pattern.replace("*", "")
	    out = []
	    for d, ld, fls in os.walk(path):
		# remove directorys to be excluded 
		for exd in excludedirs:
		    if exd in ld:
			ld.remove(exd)
		for f in fls:		    
		    if f.endswith(pattern):
			drel=d.replace(path,"")
			out.append(os.path.join(drel,f))
	    return out
	else:
	    return [ i.replace(path, '') for i in  glob.glob(path + pattern) ]
    env.SGlob = SGlob

    def AddCustomPath(path=None):
        if path is None or not os.path.exists(path):
            env.Exit(1)
        env.PrependUnique(CPPPATH = [os.path.join(path, "include")])
        env.PrependUnique(LIBPATH = [os.path.join(path, ARCHLIBDIR)])
    env.AddCustomPath = AddCustomPath

    def AddCustomPackage(pkgname=None, incdirext=None):
        if pkgname is None:
	    return
        #print env.Dump()
        pkgroot = env.get("%s_root" % pkgname)
        pkgincd = env.get("%s_incdir" % pkgname)
        pkglibd = env.get("%s_libdir" % pkgname)
	incd = None
	libd = None
        if pkgroot == "/usr":
            if incdirext is not None:
                incd = os.path.join(pkgroot, "include", incdirext)
                env.PrependUnique(CPPPATH = [incd])
            return
	if pkgroot is not None:
	    incd = os.path.join(pkgroot, "include")
            if incdirext:
                incd = os.path.join(incd, incdirext)
	    libd = os.path.join(pkgroot, ARCHLIBDIR)
	else:	    
	    if pkgincd is not None:
		incd = pkgincd
            if incdirext:
                incd = os.path.join(incd, incdirext)
	    if pkglibd is not None:
		libd = pkglibd
	if incd is not None:
	    if not os.path.exists(incd):
		print "Custom %s include dir '%s' not found" % (pkgname, incd)
		env.Exit(1)
	    env.PrependUnique(CPPPATH = [incd])
	if libd is not None:
 	    if not os.path.exists(libd):
		print "Custom %s lib dir '%s' not found" % (pkgname, libd)
		env.Exit(1)
	    env.PrependUnique(LIBPATH = [libd])
    env.AddCustomPackage = AddCustomPackage

    def PlatformIdent():
	p = sys.platform
	# replace the trailing 2 in linux2
	p = re.sub(re.compile("2$"), "", p)
	return p + "_" + platform.machine()
    env.PlatformIdent = PlatformIdent

    def DefaultCasacoreRoot():
        hier = env.get("extra_root", None)
        if not env.get("casacore_root"):
            if hier:
                env["casacore_root"] = hier
            else:
                env["casacore_root"] = os.path.join("/usr", "local")
                            
    def AddFlags():
        # add extra Hierachy
        hier = env.get("extra_root", None)
        if hier is not None and hier != "/usr":
            hier = os.path.expandvars(os.path.expanduser(hier))
            incdir = os.path.join(hier, 'include')
            env.MergeFlags("-I"+incdir)
            libdir = os.path.join(hier, ARCHLIBDIR)
            ldname = sys.platform == "darwin" and "DYLD_LIBRARY_PATH" or \
                "LD_LIBRARY_PATH"
            env.PrependENVPath(ldname, [libdir])

            # maybe also lib64
            env.MergeFlags("-L"+libdir)
            bindir = os.path.join(hier, 'bin')
            env.PrependENVPath("PATH", [bindir])

        env.MergeFlags(env.get("extra_cppflags", None))
        env.MergeFlags(env.get("extra_cxxflags", None))
        env.MergeFlags(env.get("extra_cflags", None))
        env.MergeFlags(env.get("extra_includedir", None))
        env.MergeFlags(env.get("extra_librarydir", None))

        # need to add it to both
        linkf = env.ParseFlags(env.get("extra_linkflags", None))['LINKFLAGS']
        env.AppendUnique(LINKFLAGS=linkf)
        env.AppendUnique(SHLINKFLAGS=linkf)
        xf=env.get("extra_ldlibrarypath", None)
        if xf:
            ldname = sys.platform == "darwin" and "DYLD_LIBRARY_PATH" or \
                "LD_LIBRARY_PATH"
            env.PrependENVPath(ldname, _to_list(xf))
        xf=env.get("extra_path", None)
        if xf:
            env.PrependENVPath("PATH", _to_list(xf))
        if env["PLATFORM"] == 'darwin':
            uniarch = env.get("universal", False)
            flags = []
            if uniarch:
                for i in uniarch.split(','):            
                    flags += ['-arch', i]
                ppflags =  flags + ['-isysroot' , env.DarwinDevSdk() ]
                linkflags = flags + ['-Wl,-syslibroot,%s'\
                                         %  env.DarwinDevSdk()]
                env.Append(CPPFLAGS=ppflags)
                env.Append(SHLINKFLAGS=linkflags)
                env.Append(LINKFLAGS=linkflags)

    # set the extra flags where available

    env.CLOptions = CLOptions(env)

    def AddOptions():
        options = [("extra-cppflags", None, "Extra pre-processor flags"),
                   ("extra-cxxflags", None, "Extra c++ compiler falgs"),
                   ("extra-linkflags", None, "Extra linker flags"),
                   ("extra-includedir", None, "Extra 'include' dir(s)"),
                   ("extra-librarydir", None, "Extra 'lib' dir(s)"),
                   ("extra-ldlibrarypath", None, "Extra (DY)LD_LIBRARY_PATH"),
                   ("extra-libs", None, "Extra libraries for linker"),
                   ("extra-path", None, "Extra PATH (bin) to search"),
                   ("extra-root", None, "Extra hierachy root to search"),
                   ]
        if env["PLATFORM"] == "darwin":
            options.append(("framework-path", None, 
                            "Alternate FRAMEWORKPATH"))
            options.append(("universal", None, 
                            "Create universal build using any of: "
                            "ppc,i386,ppc64,x86_64"))

        for opt in options:
            env.CLOptions.add_str_option(*opt)
        options = [("CC", None, "The c compiler"),
                   ("CXX", None, "The c++ compiler"),]
#                   ("LD", None, "The linker")]
        for opt in options:
            env.CLOptions.add_comp_option(*opt)


        env.CLOptions.add_option("--build-type", dest="build_type", 
                                 default="opt", action="store", type="string",
                                 help="Build optimized 'opt' (default) or "
                                      "debug 'dbg'")
        env.CLOptions.add_option("--enable-static", dest="enable_static",
                                 action="store_true", default=False,
                                 help="Enable building static library")
        env.CLOptions.add_option("--disable-shared", dest="disable_shared",
                                 action="store_true", default=False,
                                 help="Disable building shared library")
        env.CLOptions.add_option("--enable-hdf5", dest="enable_hdf5",
                                 action="store_true", default=False,
                                 help="Enable the HDF5 library")
        env.CLOptions.add_option("--numpy-incdir", dest="numpy_incdir", 
                                 default=get_numpy_incdir(),
                                 action="store", type="string",
                                 help="The directory of the numpy header files")
        env.CLOptions.add_option("--enable-rpath", dest="enable_rpath",
                                 action="store_true", default=False,
                                 help="OS X only. If an external library wants"
                                      " to set rpath to libpyrap.dylib "
                                      "-install_name needs to be set to an "
                                      "absolute path.")

        env.CLOptions.add_pkg_option("hdf5")
        env.CLOptions.add_pkg_option("dl")
        env.CLOptions.add_pkg_option("casacore", lib='casa_casa')
        env.CLOptions.add_pkg_option("boost", lib='boost_python')


        defdir = "/usr/local"
        PREFIX = 'prefix'
        LIBDIR = 'libdir'
        INCLUDEDIR = 'includedir'
        env.CLOptions.add_option("--"+PREFIX, dest=PREFIX,
                  type="string", default=defdir, 
                  help="The installation prefix (default: %s)" % defdir)
        env.CLOptions.add_option("--"+LIBDIR, dest=LIBDIR,
                                 type="string", default=None, 
                                 help="The installation lib directory "
                                      "(default: %s/%s)" % (defdir, 
                                                            ARCHLIBDIR))
        env.CLOptions.add_option("--"+INCLUDEDIR, dest=INCLUDEDIR,
                                 type="string", default=None, 
                                 help="The installation include directory "
                                      "(default: %s/include)" % defdir)

        env.CLOptions.update()
    AddOptions()
    AddFlags()
    DefaultCasacoreRoot()

def exists(env):
    return 1
