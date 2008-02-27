from _functionals import _functional

class functional(_functional):
    def __init__(self, name=None, order=-1, params=None, mode=None, dtype=0):
        self._dtype = dtype
        progtext = ""
        if not isinstance(name, str):
            raise TypeError("name was not of type string")
        
        if not isinstance(order, int) and not isinstance(order, str):
            raise TypeError("order was not of type integer or string")
        else:
            if isinstance(order, str):
                progtext = str(order)
                order=-1
        # our own functionals server
        d = { 'type': name, 'order': order, 'progtext': progtext}
        if isinstance(mode, dict):
            d['mode'] = mode
        _functional.__init__(self, d, dtype)
        if hasattr(params, "__len__"):
            if len(params) == 0:
                pass
            elif len(params) == self.npar():
                 self.setparameters(params)
            else:
                raise ValueError("Incorrect number of parameters " \
                                 "specified in functional")
    def __str__(self):
        return str(self.todict())

    def setparameters(self, params):
        if self._dtype == 0:
            return _functional.setparameters(self, params)
        else:
            return _functional.setparametersc(self, params)
    def setpar(self, idx, val):
        if self._dtype == 0:
            return _functional.setpar(self, idx, val)
        else:
            return _functional.setparc(self, idx, val)

    def setparameters(self, params):
        if self._dtype == 0:
            return _functional.setparameters(self, params)
        else:
            return _functional.setparametersc(self, params)
    def setpar(self, idx, val):
        if self._dtype == 0:
            return _functional.setpar(self, idx, val)
        else:
            return _functional.setparc(self, idx, val)

    def parameters(self):
        if self._dtype == 0:
            return _functional.parameters(self)
        else:
            return _functional.parametersc(self)

    def f(self, x=[]):
        if self._dtype == 0:
            return _functional.f(self, x)
        else:
            return _functional.fc(self, x)
        
    def fdf(self, x=[]):
        if self._dtype == 0:
            return _functional.fdf(self, x)
        else:
            return _functional.fdfc(self, x)
    
    def add(self, other):
        if not isinstance(other, functional):
            raise TypeError("'other' is not a functional")
        if self._dtype != other._dtype:
            raise TypeError("'other' is not of the same value type")
        
        if self._dtype == 0:
            _functional.add(self, other)
        else:
            _functional.addc(self, other)

class gaussian1d(functional):
    def __init__(self, name="gaussian1d", params=None, dtype=0):
        functional.__init__(self, name, params=params, dtype=dtype)

class gaussian2d(functional):
    def __init__(self, params=[1,0,0,1,1,0], dtype=0):
        functional.__init__(self, name="gaussian2d",
                            params= params,
                            dtype=dtype)
        
class poly(functional):
    def __init__(self, order=None, params=None, dtype=0):
        functional.__init__(self, name="poly",
                            order=order,
                            params= params,
                            dtype=dtype)
        if params is None:
            self.setparameters([v+1. for v in self.parameters()])

class oddpoly(functional):
    def __init__(self, order=None, params=None, dtype=0):
        functional.__init__(self, name="oddpoly",
                            order=order,
                            params= params,
                            dtype=dtype)
        if params is None:
            self.setparameters([v+1. for v in self.parameters()])

class evenpoly(functional):
    def __init__(self, order=None, params=None, dtype=0):
        functional.__init__(self, name="evenpoly",
                            order=order,
                            params= params,
                            dtype=dtype)
        if params is None:
            self.setparameters([v+1. for v in self.parameters()])

class chebyshev(functional):
    def __init__(self, order=None, params=None,
                 xmin=-1., xmax=1., ooimode='constant',
                 dtype=0):
        modes = "constant zeroth extrapolate cyclic edge".split()
        if not ooimode in modes:
            raise ValueError("Unrecognized ooimode")
        mode = {'interval': [float(xmin),float(xmax)], 'intervalMode': ooimode,
                'default': float(0.0) };        
        functional.__init__(self, name="chebyshev",
                            order=order,
                            params= params,
                            mode=mode,
                            dtype=dtype)
        if params is None:
            self.setparameters([v+1. for v in self.parameters()])

class compound(functional):
    def __init__(self, dtype=0):
        functional.__init__(self, name="compound", dtype=dtype)
                     
class combi(functional):
    def __init__(self, dtype=0):
        functional.__init__(self, name="combi", dtype=dtype )
                     
class compiled(functional):
    def __init__(self, code="", params=None, dtype=0):
        functional.__init__(self, name="compiled", order=code,
                            params=params, dtype=dtype)
