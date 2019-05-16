from ._fitting import fitting
import numpy as NUM
import six
from casacore.functionals import *
from six import string_types


class fitserver(object):
    """Create a `fitserver instance.

    The object can be created without arguments (in which case it is assumed
    to be a real fitter), or with the arguments specifying the number of
    unknowns to be solved for (a number not relevant in practice); and the type
    of solution: real, complex, conjugate (complex with both the unknown and
    its conjugate in the condition equations), separable complex, asreal
    complex with the real and imaginary part seen as independent unknowns.
    All solutions need a model (specified as a :mod:`casacore.functionals`.
    All solutions are done using an SVD type method. A collinearity factor
    can be specified, which is in essence the sine squared of the minimum angle
    between two normal equation columns that are still to be considered
    independent. For automatic non-linear solutions, a Levenberg-Marquardt
    factor (see`Note 224 <../../casacore/doc/notes/224.html>`_) is used, which
    can be specified as well.

    In the case of non-linear solutions that have to be handled by the system,
    an initial estimate for the model parameters is necessary.

    :param n:      number of unknowns
    :param ftype:  type of solution
                   Allowed: real, complex, separable, asreal, conjugate
    :param colfac: collinearity factor
    :param lmfac:  Levenberg-Marquardt factor
    :param fid:    the id of a sub-fitter

    """

    def __init__(self, n=0, m=1, ftype=0, colfac=1.0e-8, lmfac=1.0e-3):
        self._fitids = []
        self._typeids = {"real": 0, "complex": 1, "separable": 3,
                         "asreal": 7, "conjugate": 11}
        self._fitproxy = fitting()
        fid = self.fitter(n=n, ftype=ftype, colfac=colfac, lmfac=lmfac)
        if fid != 0:
            raise RuntimeError("System problem creating fitter server")

    def fitter(self, n=0, ftype="real", colfac=1.0e-8, lmfac=1.0e-3):
        """Create a sub-fitter.

        The created sub-fitter can be used in the same way as a fitter
        default fitter. This function returns an identification, which has to
        be used in the `fid` argument of subsequent calls. The call can
        specify the standard constructor arguments (`n`, `type`, `colfac`,
        `lmfac`), or can specify them later in a :meth:`set` statement.

        :param n:      number of unknowns
        :param ftype:  type of solution
                       Allowed: real, complex, separable, asreal, conjugate
        :param colfac: collinearity factor
        :param lmfac:  Levenberg-Marquardt factor
        :param fid:    the id of a sub-fitter

        """
        fid = self._fitproxy.getid()
        ftype = self._gettype(ftype)
        n = len(self._fitids)
        if 0 <= fid < n:
            self._fitids[fid] = {}
        elif fid == n:
            self._fitids.append({})
        else:
            # shouldn't happen
            raise IndexError("fit id out of range")
        self.init(n=n, ftype=ftype, colfac=colfac, lmfac=lmfac, fid=fid)
        return fid

    def init(self, n=0, ftype="real", colfac=1.0e-8, lmfac=1.0e-3, fid=0):
        """Set selected properties of the fitserver instance.

        Like in the constructor, the number of unknowns to be solved for;
        the number of simultaneous solutions; the ftype and the collinearity
        and Levenberg-Marquardt factor can be specified. Individual values can
        be overwritten with the :meth:`set` function.

        :param n: number of unknowns
        :param ftype: type of solution
                      Allowed: real, complex, separable, asreal, conjugate
        :param colfac:	collinearity factor
        :param lmfac: Levenberg-Marquardt factor
        :param fid: the id of a sub-fitter
        """
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
        if isinstance(ftype, string_types):
            ftype = ftype.lower()
            if ftype not in self._typeids:
                raise TypeError("Illegal fitting type")
            else:
                return self._typeids[ftype]
        elif isinstance(ftype, six.integer_types):
            if ftype not in self._typeids.values():
                raise TypeError("Illegal fitting type")
        else:
            raise TypeError("Illegal fitting type")
        return ftype

    def _settype(self, ftype=0):
        for k, v in self._typeids.items():
            if ftype == v:
                return k
        return "real"

    def _checkid(self, fid=0):
        if not (0 <= fid < len(self._fitids)
                and isinstance(self._fitids[fid], dict)
                and "stat" in self._fitids[fid]
                and isinstance(self._fitids[fid]["stat"], dict)):
            raise ValueError("fit id out of range")

    def _reshape(self, fid=0):
        pass

    def _getstate(self, fid):
        d = self._fitproxy.getstate(fid)
        if "typ" in d:
            d["typ"] = self._settype(d["typ"])
        return d

    def set(self, n=None, ftype=None, colfac=None, lmfac=None, fid=0):
        """Set selected properties of the fitserver instance.

        All unset properties remain the same (in the :meth:`init` method all
        properties are (re-)initialized). Like in the constructor, the number
        of unknowns to be solved for; the number of simultaneous solutions;
        the ftype (as code); and the collinearity and Levenberg-Marquardt
        factor can be specified.

        :param n: number of unknowns
        :param ftype: type of solution
                    Allowed: real, complex, separable, asreal, conjugate
        :param colfac:	collinearity factor
        :param lmfac: Levenberg-Marquardt factor
        :param fid: the id of a sub-fitter
        """
        self._checkid(fid)
        if ftype is None:
            ftype = -1
        else:
            ftype = self._gettype(ftype)
        if n is None:
            n = -1
        elif n < 0:
            raise ValueError("Illegal set argument n")
        if colfac is None:
            colfac = -1
        elif colfac < 0:
            raise ValueError("Illegal set argument colfac")
        if lmfac is None:
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

    def done(self, fid=0):
        """Terminates the fitserver."""
        self._checkid(fid)
        self._fitids[fid] = {}
        self._fitproxy.done(fid)

    def reset(self, fid=0):
        """Reset the object's resources to its initialized state.

        :param fid: the id of a sub-fitter
        """
        self._checkid(fid)
        self._fitids[fid]["solved"] = False
        self._fitids[fid]["haserr"] = False
        if not self._fitids[fid]["looped"]:
            return self._fitproxy.reset(fid)
        else:
            self._fitids[fid]["looped"] = False
        return True

    def getstate(self, fid=0):
        """Obtain the state of the fitter object or a sub-fitter.

        :param fid: the id of a sub-fitter
        """
        self._checkid(fid)
        return self._fitids[fid]["stat"]

    def clearconstraints(self, fid=0):
        """Clear the constraints."""
        self._checkid(fid)
        self._fitids[fid]["constraint"] = {}

    def addconstraint(self, x, y=0, fnct=None, fid=0):
        """Add constraint."""
        self._checkid(fid)
        i = 0
        if "constraint" in self._fitids[fid]:
            i = len(self._fitids[fid]["constraint"])
        else:
            self._fitids[fid]["constraint"] = {}
        # dict key needs to be string
        i = str(i)
        self._fitids[fid]["constraint"][i] = {}
        if isinstance(fnct, functional):
            self._fitids[fid]["constraint"][i]["fnct"] = fnct.todict()
        else:
            self._fitids[fid]["constraint"][i]["fnct"] = \
                functional("hyper", len(x)).todict()
        self._fitids[fid]["constraint"][i]["x"] = [float(v) for v in x]
        self._fitids[fid]["constraint"][i]["y"] = float(y)
        six.print_(self._fitids[fid]["constraint"])

    def fitpoly(self, n, x, y, sd=None, wt=1.0, fid=0):
        if self.set(n=n + 1, fid=fid):
            return self.linear(poly(n), x, y, sd, wt, fid)

    def fitspoly(self, n, x, y, sd=None, wt=1.0, fid=0):
        """Create normal equations from the specified condition equations, and
        solve the resulting normal equations. It is in essence a combination.

        The method expects that the properties of the fitter to be used have
        been initialized or set (like the number of simultaneous solutions m
        the type; factors). The main reason is to limit the number of
        parameters on the one hand, and on the other hand not to depend
        on the actual array structure to get the variables and type. Before
        fitting the x-range is normalized to values less than 1 to cater for
        large difference in x raised to large powers. Later a shift to make x
        around zero will be added as well.

        :param n: the order of the polynomial to solve for
        :param x: the abscissa values
        :param y: the ordinate values
        :param sd: standard deviation of equations (one or more values used
                   cyclically)
        :param wt: an optional alternate for `sd`
        :param fid: the id of the sub-fitter (numerical)

        Example::

            fit = fitserver()
            x = N.arange(1,11) # we have values at 10 'x' values
            y = 2. + 0.5*x - 0.1*x**2 # which are 2 +0.5x -0.1x^2
            fit.fitspoly(3, x, y) # fit a 3-degree polynomial
            print fit.solution(), fit.error() #  show solution and their errors

        """
        a = max(abs(max(x)), abs(min(x)))
        if a == 0:
            a = 1
        a = 1.0 / a
        b = NUM.power(a, range(n + 1))
        if self.set(n=n + 1, fid=fid):
            self.linear(poly(n), x * a, y, sd, wt, fid)
            self._fitids[fid]["sol"] *= b
            self._fitids[fid]["error"] *= b
            return self.linear(poly(n), x, y, sd, wt, fid)

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
        fnct = kw["fnct"]
        kw["fnct"] = fnct.todict()
        self.reset(fid)
        x = self._as_array(kw["x"])
        if x.ndim > 1 and fnct.ndim() == x.ndim:
            x = x.flatten()
        y = self._as_array(kw["y"])
        if y.ndim > 1 and fnct.ndim() == y.ndim:
            x = y.flatten()
        wt = self._as_array(kw["wt"])
        if sd is not None:
            sd = self._as_array(sd)
            wt = sd.copy()
            wt[sd == 0] = 1
            wt = 1 / abs(wt * NUM.conjugate(wt))
            wt[NUM.logical_or(sd == -1, sd == 0)] = 0
        ftype = fitfunc
        dtype = 'float'
        if (
            self.getstate(fid)["typ"] != "real" or
            NUM.iscomplexobj(x) or
            NUM.iscomplexobj(y) or
            NUM.iscomplexobj(wt)
           ):
            ftype = "cx%s" % fitfunc
            dtype = 'complex'
        kw["x"] = self._as_array(x, dtype)
        kw["y"] = self._as_array(y, dtype)
        kw["wt"] = self._as_array(wt, dtype)
        if "constraint" not in self._fitids[fid]:
            self._fitids[fid]["constraint"] = {}
        kw["constraint"] = self._fitids[fid]["constraint"]
        func = getattr(self._fitproxy, ftype)
        result = func(**kw)
        self._fitids[fid].update(result)
        self._fitids[fid]["solved"] = True
        self._fitids[fid]["haserr"] = True
        self._fitids[fid]["looped"] = False

    def functional(self, fnct, x, y, sd=None, wt=1.0, mxit=50, fid=0):
        """Make a non-linear least squares solution.

        This will make a non-linear least squares solution for the points
        through the ordinates at the abscissa values, using the specified
        `fnct`. Details can be found in the :meth:`linear` description.

        :param fnct: the functional to fit
        :param x: the abscissa values
        :param y: the ordinate values
        :param sd: standard deviation of equations (one or more values used
                   cyclically)
        :param wt: an optional alternate for `sd`
        :param mxit: the maximum number of iterations
        :param fid: the id of the sub-fitter (numerical)

        """
        self._fit(fitfunc="functional", fnct=fnct, x=x, y=y, sd=sd, wt=wt,
                  mxit=mxit, fid=fid)

    nonlinear = functional

    def linear(self, fnct, x, y, sd=None, wt=1.0, fid=0):
        """Make a linear least squares solution.

        Makes a linear least squares solution for the points through the
        ordinates at the x values, using the specified fnct. The x can be of
        any dimension, depending on the number of arguments needed in the
        functional evaluation. The values should be given in the order:
        x0[1], x0[2], ..., x1[1], ..., xn[m] if there are n observations,
        and m arguments. x should be a vector of m*n length; y (the
        observations) a vector of length n.

        :param fnct: the functional to fit
        :param x: the abscissa values
        :param y: the ordinate values
        :param sd: standard deviation of equations (one or more values used
                   cyclically)
        :param wt: an optional alternate for `sd`
        :param fid: the id of the sub-fitter (numerical)

        """
        self._fit(fitfunc="linear", fnct=fnct, x=x, y=y, sd=sd, wt=wt, fid=fid)

    def _getval(self, valname, fid):
        self._checkid(fid)
        if not self._fitids[fid]["solved"]:
            raise RuntimeError("Not solved yet")
        return self._fitids[fid][valname]

    def solution(self, fid=0):
        """Return the solution for the fit.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("sol", fid)

    def rank(self, fid=0):
        """Obtain the rank(in SVD sense) of a fit.

         The :meth:`constraint` method will show the equations that are
         orthogonal to the existing ones, and which will make the solution
         possible.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("rank", fid)

    def deficiency(self, fid=0):
        """Obtain the missing rank (in SVD sense) of a fit.

        The :meth:`constraint` method will show the equations that are
        orthogonal to the existing ones, and which will make the solution
        possible.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("deficiency", fid)

    def chi2(self, fid=0):
        """Obtain the chi squared of a fit.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("chi2", fid)

    def sd(self, fid=0):
        """Obtain the standard deviation per unit of weight of a fit.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("sd", fid)

    def mu(self, fid=0):
        """Obtain the standard deviation per condition equation of a fit.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("mu", fid)

    stddev = mu

    def covariance(self, fid=0):
        """Obtain the covariance matrix of a fit.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("covar", fid)

    def error(self, fid=0):
        """Obtain the errors in the unknowns of a fit.

        :param fid: the id of the sub-fitter (numerical)

        """
        return self._getval("error", fid)

    def constraint(self, n=-1, fid=0):
        """Obtain the set of orthogonal equations that make the solution of
        the rank deficient normal equations possible.

        :param fid: the id of the sub-fitter (numerical)

        """
        c = self._getval("constr", fid)
        if n < 0 or n > self.deficiency(fid):
            return c
        else:
            raise RuntimeError("Not yet implemented")

    def fitted(self, fid=0):
        """Test if enough Levenberg-Marquardt loops have been done.

        It returns True if no improvement possible.

        :param fid: the id of the sub-fitter (numerical)
        """
        self._checkid(fid)
        return not (self._fitids[fid]["fit"] > 0
                    or self._fitids[fid]["fit"] < -0.001)

    def _as_array(self, v, dtype=None):
        if not hasattr(v, "__len__"):
            v = [v]
        return NUM.asarray(v, dtype)
