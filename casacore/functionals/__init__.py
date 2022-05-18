# __init__.py: Top level .py file for python functionals interface
# Copyright (C) 2006,2007
# Associated Universities, Inc. Washington DC, USA.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Correspondence concerning AIPS++ should be addressed as follows:
#        Internet email: aips2-request@nrao.edu.
#        Postal address: AIPS++ Project Office
#                        National Radio Astronomy Observatory
#                        520 Edgemont Road
#                        Charlottesville, VA 22903-2475 USA
#
# $Id: __init__.py,v 1.1 2006/09/29 06:42:55 mmarquar Exp $
"""
Introduction
============

A functional is a function with parameters, defined as *f(p;x)*, where *p* are
the parameters, and *x* the arguments. Methods are available to calculate the
value of a function for a series of argument values for the given set of
parameters, and for the automatic calculation of the derivatives with respect
to the parameters.

The created functionals can be used for fitiing as provided by
:mod:`casacore.fitting`.

A functional has a mask associated with it, to indicate if certain parameters
have to be solved for. See masks for details.

To access the functionals module ``import casacore.functionals``.

Functionals are created in a variety of ways, in general by specifying the
name of the functional, together with some necessary information like e.g.
the order of a polynomial, or the code needed to compile your privately
defined function. Parameters can be set at creation time or later::

    >>> from casacore.functionals import functional, gaussian1d
    >>> a = gaussian1d()	         # creates a 1D Gaussian, default arguments
    >>> b = functional('gaussian1d') # creates the same one
    >>> print a.f(1)                 # the value at x=1
    [0.062500000000000028]
    >>> print a(1)
    [0.062500000000000028]
    >>> print a.fdf([0,0.5]);        # value and derivatives
    >>> print a([0, 0.5], derivatives=True)

In some cases an order can be specified as well (e.g. for polynomials)::

    >>> from casacore.functionals import functional, poly
    >>> a = poly(3)                  # creates a 3rd order polynomial
    >>> print a
    {'ndim': 1, 'masks': array([ True,  True,  True,  True], dtype=bool),
     'params': array([ 1.,  1.,  1.,  1.]), 'npar': 4, 'type': 5, 'order': 3}

An extremely valuable aspect of the Functionals module is the ability to
create a functional from a compiled string specifying an arbitrary function.
For example, let us make our own polynomial ``1 + 2*x + 3*x2`` and evaluate it
at a few abcissa locations::

    >>> from casacore.functionals import compiled
    >>> a = compiled('p0 + p1*x + p2*x*x', [1,2,3])   # Define
    >>> a([0,10,20])                                  # Evaluate at x=[0,10,20]
    [1.0, 321.0, 1241.0]

The functions created can also be used to specify the function to be fitted
in a least squares fit.

"""
from .functional import *
