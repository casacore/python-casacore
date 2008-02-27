from _fitting import fitting
from pyrap.functionals import *
import numpy as NUM

class fitserver:
    def __init__(self, n=0, m=1, ftype=0, fnct=None,
                 colfac=1.0e-8, lmfac=1.0e-3):
        self._fitids = []
        self._typeids = {"real": 0, "complex": 1, "separable": 3,
                         "asreal": 7, "conjugate": 11}
        self._fitproxy = fitting()
        fid = self.fitter(n=n, ftype=ftype, colfac=colfac, lmfac=lmfac)
        if fid != 0:
            raise RuntimeError("System problem creating fitter server")

    def fitter(self, n=0, ftype="real", colfac=1.0e-8, lmfac=1.0e-3):
        fid = self._fitproxy.getid()
        n = len(self._fitids)
        if 0 <= fid < n:
            self._fitids[fid] = {}
        elif fid == n:
            self._fitids.append({})
        else:
            # shouldn't happen
            raise RangeError("fit id out of range")
        self.init(n=n, ftype=ftype, colfac=colfac, lmfac=lmfac, fid=fid)
        return fid

    def init(self,  n=0, ftype="real", colfac=1.0e-8, lmfac=1.0e-3, fid=0):
        ftype = self._gettype(ftype)
        self._fitids[fid]["stat"] = False
        self._fitids[fid]["solved"] = False
        self._fitids[fid]["haserr"] = False
        self._fitids[fid]["fit"] = False
        self._fitids[fid]["looped"] = False
        if self._fitproxy.init(fid, n, ftype, colfac, lmfac):
            self._fitids[fid]["stat"] = self._getstate(fid)
        else:
            return False

    def _gettype(self, ftype):
        if isinstance(ftype, str):
            ftype = ftype.lower()
            if not self._typeids.has_key(ftype):
                raise TypeError("Illegal fitting type")
            else:
                return self._typeids[ftype]
        elif isinstance(ftype, int):
            if not ftype in self._typeids.values():
                raise TypeError("Illegal fitting type")
        else:
            raise TypeError("Illegal fitting type")
        return ftype

    def _settype(self, ftype=0):
        for k, v in self._typeids.iteritems():
            if ftype == v:
                return k
        return "real"
        
    def _checkid(self, fid=0):
        if not ( 0 <= fid < len(self._fitids) \
		 and isinstance(self._fitids[fid], dict) \
		 and self._fitids[fid].has_key("stat") \
		 and isinstance(self._fitids[fid]["stat"], dict) ):
	    raise ValueError("fit id out of range")

    def _reshape(self, fid=0):
        pass

    def  _getstate(self, fid):
        d = self._fitproxy.getstate(fid)
        if d.has_key("typ"):
            d["typ"] = self._settype(d["typ"])
        return d

    def set(self, n=None, ftype=None, colfac=None, lmfac=None, fid=0):
        self._checkid(fid)
        if ftype is None:
            ftype = -1
        else:
            ftype = self._gettype()
        if  n is None:
            n = -1
        elif n < 0:
            raise ValueError("Illegal set argument n")
        if  colfac is None:
            colfac = -1
        elif colfac < 0:
            raise ValueError("Illegal set argument colfac")
        if  lmfac is None:
            lmfac = -1
        elif lmfac < 0:
            raise ValueError("Illegal set argument lmfac")
        
        self._fitids[fid]["stat"] = False
        self._fitids[fid]["solved"] = False
        self._fitids[fid]["haserr"] = False
        self._fitids[fid]["fit"] = True
        self._fitids[fid]["looped"] = False
        if n != -1 or ftype != -1 or colfac != -1 or lmfac != -1:
            if not self._fitproxy.set(fid, n, ftype, colfac, lmfac):
                return False
        self._fitids[fid]["stat"] = self._getstate(fid)
        return True

    def done(self, fid=None):
        self._checkid(fid)
        self._fitids[fid] = {}
        self._fitproxy.done(fid)

    def reset(self, fid=0):
        self._checkid(fid)
	self._fitids[fid]["solved"] = False
        self._fitids[fid]["haserr"] = False
        if not self._fitids[fid]["looped"]:
            return self._fitproxy.reset(fid)
        else:
            self._fitids[fid]["looped"] = False
        return True

    def getstate(self, fid=0):
        self._checkid(fid)
        return self._fitids[fid]["stat"]

    def clearconstraints(self, fid=0):
        self._checkid(fid)
        self._fitids[fid]["constraint"] = {}

    def addconstraint(self, fnct, x, y=0, fid=0):
        self._checkid(fid)
        i = 0
        if self._fitids[fid].has_key("constraint"):
            i = len(self._fitids[fid]["constraint"])
        else:
            self._fitids[fid]["constraint"] = {}
        self._fitids[fid]["constraint"][i] = {}
        if isinstance(fnct, functional):
            self._fitids[fid]["constraint"][i] = fnct
        else:
            self._fitids[fid]["constraint"][i] = functional("hyper", len(x))
        self._fitids[fid]["constraint"][i]["x"] = [float(d) for v in x]
        self._fitids[fid]["constraint"][i]["y"] = float(y)
    

    def fitpoly(self, n, x, y, sd=None, wt=1.0, fid=0):
        if self.set(n=n+1, fid=fid):
            return self.linear(poly(n), x, y, sd, wt, fid)

    def fitspoly(self, n, x, y, sd=None, wt=1.0, fid=0):
        a = max(abs(max(x)), abs(min(x)))
        if a == 0: a = 1
        a = 1.0/a
        b = NUM.power(a, range(n+1))
        if self.set(n=n+1, fid=fid):
            return self.linear(poly(n), x, y, sd, wt, fid)
        if self.set(n=n+1, fid=fid):
            self.linear(poly(n), x*a, y, sd, wt, fid)
            self._fitids[fid]["sol"] *= b
            self._fitids[fid]["error"] *= b

    def fitavg(self, y, sd=None, wt=1.0, fid=0):
        if self.set(n=1, fid=fid):
            return self.linear(compiled("p"), [], y, sd, wt, fid)
        
    def _fit(self, **kw):
	fitfunc = kw.pop("fitfunc")
	sd = kw.pop("sd")
        fid = kw.pop("fid")
        kw["id"] = fid
        if not isinstance(kw["fnct"], functional):
            raise TypeError("No or illegal functional")
        if not self.set(n=kw["fnct"].npar(), fid=fid):
            raise ValueError("Illegal fit id")
        kw["fnct"] = kw["fnct"].todict()
	self.reset(fid)
	x = self._as_array(kw["x"])
	y = self._as_array(kw["y"])
	wt = self._as_array(kw["wt"])
        if sd is not None:
	    sd = self._as_array(sd)
	    wt = sd.copy()
	    wt[sd == 0] = 1
	    wt = 1/abs(wt * NUM.conjugate(wt))
	    wt[NUM.logical_or(sd == -1, sd == 0)] = 0
	ftype = fitfunc
	dtype = 'float'
        if (self.getstate(fid)["typ"] != "real"
	    or NUM.iscomplexobj(x) \
	    or NUM.iscomplexobj(y) \
	    or NUM.iscomplexobj(wt) ):
	    ftype = "cx%s" % fitfunc
	    dtype = 'complex'
	kw["x"] = self._as_array(x, dtype)
	kw["y"] = self._as_array(y, dtype)
	kw["wt"] = self._as_array(wt, dtype)
	if not self._fitids[fid].has_key("constraint"):
	    self._fitids[fid]["constraint"] = {}
        kw["constraint"] =  self._fitids[fid]["constraint"]
	func = getattr(self._fitproxy, ftype)
	result = func(**kw)
	self._fitids[fid].update(result)
	self._fitids[fid]["solved"] = True 
	self._fitids[fid]["haserr"] = True 
	self._fitids[fid]["looped"] = False 

    def functional(self, fnct, x, y, sd=None, wt=1.0, mxit=50, fid=0):
	self._fit(fitfunc="functional", fnct=fnct, x=x, y=y, sd=sd, wt=wt,
		  mxit=mxit, fid=fid) 

    def linear(self, fnct, x, y, sd=None, wt=1.0, fid=0):
	self._fit(fitfunc="linear", fnct=fnct, x=x, y=y, sd=sd, wt=wt, fid=fid) 
        
    def _getval(self, valname, fid):
	self._checkid(fid)
	if not self._fitids[fid]["solved"]:
	    raise RuntimeError("Not solved yet")
	return self._fitids[fid][valname]

    def solution(self, fid=0):
	return self._getval("sol", fid)
    def deficiency(self, fid=0):
	return self._getval("deficiency", fid)
    def chi2(self, fid=0):
	return self._getval("chi2", fid)
    def sd(self, fid=0):
	return self._getval("sd", fid)
    def mu(self, fid=0):
	return self._getval("mu", fid)
    def stddev(self, fid=0):
	return self._getval("mu", fid)
    def covariance(self, fid=0):
	return self._getval("covar", fid)
    def error(self, fid=0):
	return self._getval("error", fid)

    def constraint(self, n=0, fid=0):
        c = self._getval("constr", fid)
        if n < 0 or n > self.deficiency(fid):
            return c
        else:
            raise RuntimeError("Not yet implemented")
        
    def fitted(self, fid=0):
	self._checkid(fid)
	return not (self._fitids[fid]["fit"] > 0 
		    or self._fitids[fid]["fit"] < -0.001)

    def _as_array(self, v, dtype=None):
        if not hasattr(v, "__len__"):
            v = [v]
        return NUM.asarray(v, dtype)
        

                
