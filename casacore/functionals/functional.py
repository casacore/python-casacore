from six import string_types, integer_types
from ._functionals import _functional

import numpy


def copydoc(fromfunc, sep="\n"):
    """
    Decorator: Copy the docstring of `fromfunc`
    """
    def _decorator(func):
        sourcedoc = fromfunc.__doc__
        if func.__doc__ is None:
            func.__doc__ = sourcedoc
        else:
            func.__doc__ = sep.join([sourcedoc, func.__doc__])
        return func
    return _decorator


class functional(_functional):
    def __init__(self, name=None, order=-1, params=None, mode=None, dtype=0):
        if isinstance(dtype, string_types):
            dtypes = {'real': 0, 'complex': 1}
            dtype = dtypes.get(dtype.lower())
        if numpy.iscomplexobj(params):
            dtype = 1
        self._dtype = dtype
        progtext = ""
        if not isinstance(name, string_types):
            raise TypeError("'name' was not of type string")
        if not (isinstance(order, integer_types) or isinstance(order, string_types)):
            raise TypeError("'order' was not of type integer or string")
        else:
            if isinstance(order, string_types):
                progtext = order
                order = -1
        # our own functionals server
        d = {'type': name, 'order': order, 'progtext': progtext}
        if isinstance(mode, dict):
            d['mode'] = mode
        _functional.__init__(self, d, self._dtype)
        if hasattr(params, "__len__"):
            params = self._flatten(params)
            if len(params) == 0:
                pass
            elif len(params) == self.npar():
                self.set_parameters(params)
            else:
                raise ValueError("Incorrect number of parameters "
                                 "specified in functional")

    def __repr__(self):
        return str(self.todict())

    def _flatten(self, x):
        if (isinstance(x, numpy.ndarray) and x.ndim > 1
                and x.ndim == self.ndim()):
            return x.flatten()
        return x

    def ndim(self):
        return _functional.ndim(self)

    def npar(self):
        """
        Return the number of parameters of the functional


        :retval: int

        """
        return _functional.npar(self)

    def __len__(self):
        return self.npar()

    #    def __getitem__(self, i):
    #        return self.get_parameters()[i]

    #    def __setitem__(self, i, v):
    #        return self.set_parameter(i, v)

    def set_parameters(self, params):
        params = self._flatten(params)
        if self._dtype == 0:
            return _functional._setparameters(self, params)
        else:
            return _functional._setparametersc(self, params)

    def set_parameter(self, idx, val):
        if self._dtype == 0:
            return _functional._setpar(self, idx, val)
        else:
            return _functional._setparc(self, idx, val)

    def get_parameters(self):
        if self._dtype == 0:
            return _functional._parameters(self)
        else:
            return _functional._parametersc(self)

    def f(self, x):

        """Calculate the value of the functional for the specified arguments
        (taking any specified mask into account).


        :param x: the value(s) to evaluate at
        """
        x = self._flatten(x)
        if self._dtype == 0:
            return numpy.array(_functional._f(self, x))
        else:
            return numpy.array(_functional._fc(self, x))

    def __call__(self, x, derivatives=False):
        if derivatives:
            return numpy.array(self.fdf(x))
        else:
            return numpy.array(self.f(x))

    def fdf(self, x):
        """Calculate the value of the functional for the specified arguments,
        and the derivatives with respect to the parameters (taking any
        specified mask into account).


       :param x: the value(s) to evaluate at
       """
        x = self._flatten(x)
        n = 1
        if hasattr(x, "__len__"):
            n = len(x)
        if self._dtype == 0:
            retval = _functional._fdf(self, x)
        else:
            retval = _functional._fdfc(self, x)
        if len(retval) == n:
            return numpy.array(retval)
        return numpy.array(retval).reshape(self.npar() + 1,
                                           n // self.ndim()).transpose()

    def add(self, other):
        if not isinstance(other, functional):
            raise TypeError("'other' is not a functional")
        if self._dtype != other._dtype:
            raise TypeError("'other' is not of the same value type")

        if self._dtype == 0:
            _functional._add(self, other)
        else:
            _functional._addc(self, other)

    def set_mask(self, i, msk):
        _functional._setmask(self, i, msk)

    def set_masks(self, msk):
        _functional._setmasks(self, msk)

    def get_masks(self):
        return _functional._masks(self)

    def todict(self):
        return _functional.todict(self)


class gaussian1d(functional):
    """Create a 1-dimensional Gaussian with the specified height, width and
    center.
    :param params: the [height, center, width] as a list
    """

    def __init__(self, params=None, dtype=0):
        functional.__init__(self, name="gaussian1d", params=params,
                            dtype=dtype)

    @copydoc(functional.npar)
    def npar(self):
        """
        Equivalent::

            >>> g = gaussian1d([1, 2, 3])
            >>> print g.npar()
            3
            >>> print len(g)
            3
        """
        return functional.npar(self)

    @copydoc(functional.f)
    def f(self, x):
        """
        Example::

            >>> a = gaussian1d()
            >>> print(a.f(0.0))
            [ 1.]
            >>> print(a(0.0))      #equivalent
            [ 1.]

        """
        return functional.f(self, x)

    @copydoc(functional.fdf)
    def fdf(self, x):
        """
        Example::

            >>> g = gaussian1d()
            >>> print(g.fdf(0.0))
            [[ 1.,  1.,  0.,  0.]]
            >>> print(g(0.0, derivatives=True))        #equivalent
            [[ 1.,  1.,  0.,  0.]]

        """
        return functional.fdf(self, x)


class gaussian2d(functional):
    """
    Create a two-dimensional gaussian.

    :param params: list [amplitude, centers, major width, ratio, angle] of
                   Gaussian default is [1, 0, 0, 1, 1, 0]
    :param dtype:  The data type. One of 'real' or 0, or 'complex' or 1
    """

    def __init__(self, params=None, dtype=0):
        if params is None:
            params = [1, 0, 0, 1, 1, 0]
        functional.__init__(self, name="gaussian2d",
                            params=params,
                            dtype=dtype)

    @copydoc(functional.npar)
    def npar(self):
        """
        Equivalent::

            >>> g = gaussian2d([1, 2, 3][4, 5, 6])
            >>> print g.npar()
            6
            >>> print len(g)
            6
        """
        return functional.npar(self)

    @copydoc(functional.f)
    def f(self, x):
        """
        Example::

            >>> a = gaussian2d()
            >>> print(a.f(0.0))
            []
            >>> print(a(0.0))      #equivalent
            []

        """
        return functional.f(self, x)

    @copydoc(functional.fdf)
    def fdf(self, x):
        """
        Example::

            >>> a = gaussian2d()
            >>> print(a.fdf(0))
            []
            >>> print(g(0.0, derivatives=True))        #equivalent
            []

        """
        return functional.fdf(self, x)


class poly(functional):
    """
    Create a polynomial of specified degree. The default parameters are all 1.
    (Note that using the generic functional function the parameters are all
    set to 0).

    :param order: the order of the polynomial (number of parameters -1)
    :param params: the values of the parameters as a list.
    :param dtype: the optional data type. Default is float, but will be
                  auto-detected from `params`. Can be set to 'complex'.
    """

    def __init__(self, order, params=None, dtype=0):
        functional.__init__(self, name="poly",
                            order=order,
                            params=params,
                            dtype=dtype)
        if params is None:
            self.set_parameters([v + 1. for v in self.get_parameters()])

    @copydoc(functional.npar)
    def npar(self):
        """
        Equivalent::

            >>> p = poly(5)
            >>> print p.npar()
            6
            >>> print len(p)
            6
        """
        return functional.npar(self)

    @copydoc(functional.f)
    def f(self, x):
        """
        Example::

            >>> p = poly(5)
            >>> print(p.f(0.0))
            [ 1.]
            >>> print(p(0.0))      # equivalent
            [ 1.]

        """
        return functional.f(self, x)

    @copydoc(functional.fdf)
    def fdf(self, x):
        """
        Example::

            >>> p = poly(5)
            >>> print(p.fdf(0.0))
            [[ 1.,  1.,  0.,  0.,  0.,  0.,  0.]]
            >>>print(p(0.0, derivatives=True))     # equivalent
            [[ 1.,  1.,  0.,  0.,  0.,  0.,  0.]]
        """
        return functional.fdf(self, x)


class oddpoly(functional):
    """Create an odd polynomial of specified degree.

    :param order: the order of the polynomial
    :param params: the values of the parameters as a list.
    :param dtype: the optional data type. Default is float, but will be
                  auto-detected from `params`. Can be set to 'complex'.

    """

    def __init__(self, order, params=None, dtype=0):
        functional.__init__(self, name="oddpoly",
                            order=order,
                            params=params,
                            dtype=dtype)
        if params is None:
            self.set_parameters([v + 1. for v in self.get_parameters()])

    @copydoc(functional.npar)
    def npar(self):
        """
        Equivalent::

            >>> p = oddpoly(3)
            >>> print p.npar()
            2
            >>> print len(p)
            2
        """
        return functional.npar(self)

    @copydoc(functional.f)
    def f(self, x):
        """
        Example::

            >>> p = oddpoly(3)
            >>> print(p.f(0.0))
            [ 0.]
            >>> print(p(0.0))      # equivalent
            [ 0.]
        """
        return functional.f(self, x)

    @copydoc(functional.fdf)
    def fdf(self, x):
        """
        Example::

            >>> p = oddpoly(3)
            >>> print(p.fdf(0.0))
            [[ 0.,  0.,  0.]]
            >>> print(p(0.0, derivatives=True))     # equivalent
            [[ 0.,  0.,  0.]]
        """
        return functional.fdf(self, x)


class evenpoly(functional):
    """Create an even polynomial of specified degree.

    :param order: the order of the polynomial
    :param params: the values of the parameters as a list.
    :param dtype: the optional data type. Default is float, but will be
                  auto-detected from `params`. Can be set to 'complex'.

    """

    def __init__(self, order, params=None, dtype=0):
        functional.__init__(self, name="evenpoly",
                            order=order,
                            params=params,
                            dtype=dtype)
        if params is None:
            self.set_parameters([v + 1. for v in self.get_parameters()])

    @copydoc(functional.npar)
    def npar(self):
        """
        Equivalent::

            >>> p = evenpoly(2)
            >>> print p.npar()
            2
            >>> print len(p)
            2
        """
        return functional.npar(self)

    @copydoc(functional.f)
    def f(self, x):
        """
        Example::

            >>> p = evenpoly(2)
            >>> print(p.f(0.0))
            [ 1.]
            >>> print(p(0.0))      # equivalent
            [ 1.]

        """
        return functional.f(self, x)

    @copydoc(functional.fdf)
    def fdf(self, x):
        """
        Example::

            >>> p = oddpoly(3)
            >>> print(p.fdf(0.0))
            [[ 1.,  1.,  0.]]
            >>>print(p(0.0, derivatives=True))     # equivalent
            [[ 1.,  1.,  0.]]
        """
        return functional.fdf(self, x)


class chebyshev(functional):
    def __init__(self, order, params=None,
                 xmin=-1., xmax=1., ooimode='constant',
                 dtype=0):
        modes = "constant zeroth extrapolate cyclic edge".split()
        if ooimode not in modes:
            raise ValueError("Unrecognized ooimode")
        mode = {'interval': [float(xmin), float(xmax)], 'intervalMode': ooimode,
                'default': float(0.0)}
        functional.__init__(self, name="chebyshev",
                            order=order,
                            params=params,
                            mode=mode,
                            dtype=dtype)
        if params is None:
            self.set_parameters([v + 1. for v in self.get_parameters()])

    @copydoc(functional.npar)
    def npar(self):
        """
        Equivalent::

            >>> ch = chebyshev(2)
            >>> print ch.npar()
            4
            >>> print len(p)
            4
        """
        return functional.npar(self)

    @copydoc(functional.f)
    def f(self, x):
        """
        Example::

            >>> ch = chebyshev(2)
            >>> print(ch.f(0.0))
            [ 0.]
            >>> print(ch(0.0))      # equivalent
            [ 0.]

        """
        return functional.f(self, x)

    @copydoc(functional.fdf)
    def fdf(self, x):
        """
        Example::

            >>> ch = chebyshev(2)
            >>> print(ch.fdf(0.0))
            [[ 0.,  1.,  0., -1.]]
            >>>print(ch(0.0, derivatives=True))     # equivalent
            [[ 0.,  1.,  0., -1.]]
        """
        return functional.fdf(self, x)


class compound(functional):
    def __init__(self, dtype=0):
        """Create a compound function.

        This class takes a arbitary number of functions and
        generates a new single function object.

        Example::

            >>> d = poly(2)
            >>> gauss1d = gaussian1d([1, 0, 1])
            >>> sum = compound()
            >>> sum.add(d)
            >>> sum.add(gauss1d)
            >>> print(sum(2))
            [ 7.00001526]

        """
        functional.__init__(self, name="compound", dtype=dtype)


class combi(functional):
    def __init__(self, dtype=0):
        """Form a linear combinations of functions object.

        Example::

            >>> const = poly(0)
            >>> linear = poly(1)
            >>> square = poly(2)
            >>> c = combi()
            >>> c.add(const)
            >>> c.add(linear)
            >>> c.add(square)
            >>> print(c(0))
            [ 3.]

        """
        functional.__init__(self, name="combi", dtype=dtype)


class compiled(functional):
    """Create a function based on the programable string. The string should
    be a single expression, which can use the standard operators and
    functions and parentheses, having a single value as a result. The
    parameters of the function can be addressed with the *p* variable. This
    variable can be indexed in two ways. The first way is using the standard
    algebraic way, where the parameters are: ``p (or p0), p1, p2, ...`` . The
    second way is by indexing, where the parameters are addressed as: p[0],
    p[1], ... . The arguments are accessed in the same way, but using the
    variable name x. The compilation determines the number of dimensions and
    parameters of the produced function.

    Operators are the standard operators (including comparisons, which
    produce a zero or one result; and conditional expression).

    In addition to the standard expected functions, there is an atan with
    either one or two arguments (although atan2 exists as well), and pi and
    ee with no or one argument. The functional created behaves as all other
    functionals, and hence can be used in combinations.

    Examples::

        >>> from casacore.functionals import compiled
        >>> import math
        >>> a = compiled('sin(pi(0.5) ) +pi');  # an example
        >>> print a(0)
        array([ 4.1415926535897931])
        >>> b = compiled('p*exp(-(x/p[2])^2)')
        >>> print b.get_parameters()
        [0.0, 0.0]
        >>> b.set_parameters([10, 1]) # change to height 10 and  halfwidth 1
        >>> print b([-1,-0.5,0,.5,1])
        array([ 3.6787944117144233,
         7.788007830714049,
         10.0,
         7.788007830714049,
         3.6787944117144233])
        # the next one is sync(x), catering for x=0
        # using the fact that comparisons deliver values. Note
        # the extensive calculation to make sure no divison by 0
        >>> synca = compiled('( (x==0) * 1)+( (x!=0) * sin(x+(x==0)*1)/(x+(x==0)*1) )')
        >>> print synca([-1,0,1])
        [0.841471, 1., 0.841471]
        >>> print math.sin(1)/1
        0.841471
        # using conditional expressions:
        print compiled('x==0 ? 1 : sin(x)/x')([-1,0,1])
        [0.841471, 1.0, 0.841471]

    """

    def __init__(self, code="", params=None, dtype=0):
        functional.__init__(self, name="compiled", order=code,
                            params=params, dtype=dtype)
