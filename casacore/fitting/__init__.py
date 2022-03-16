# __init__.py: Top level .py file for python ftting interface
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
# $Id: __init__.py,v 1.1 2006/10/20 06:30:03 mmarquar Exp $

"""Python interface to the Casacore scimath fitting module.

Introduction
============

The fitting module provides least squares fitting. It can handle linear and
non-linear; real and complex (including cases where unknowns are each other's
conjugate); complete and singular-value-decomposition; with or without
external constraints; general or specific cases.

------------------
The fitting module
------------------

For most uses we will create a single fitting object to work with::

    from casacore.fitting import fitserver
    dfit = fitserver()


More fitting tools can be created by either the fitter constructor (which
creates and returns a separate fitting tool), or by the fitter method of
an existing fitting tool, which returns a fit identifier, which can be
used to indicate a specific sub-fitter in the fitter used by including a
parameter 'id=' in all calls to the fitting tool's functions. The latter is
especially useful in the case where many simultaneous solutions are necessary:
it is more resource efficient, and also allows you to have an array of fit
indices to loop over. In both cases the parameters of the tool can be given
in the constructor (fitter method), or in a separate init method (see next
example of the highest level use)::

    from casacore.fitting import fitserver
    myfit = fitserver()		# general fitting object created
    				# (needs initializing before it can be used)
    cpid = myfit.fitter(ftype='complex') # and another (sub-)fitter
                                         # with an id

The theory behind the fitting module's operation is described in detail in
(`Note 224 <../../casacore/doc/notes/224.html>`_).


Fitting requires a model describing the data obtained. The model is a described
as a functional with parameters to be solved for. Functionals can be
pre-programmed functionals like poly, gauss1d, or free form like compiled. In
the latter case an expression string describes the model.

The model can depend on zero, one or more arguments, called x. The number of
arguments determines the dimension of the model.

Fitting also needs a set of data, called y. If the model is not 0-dimensional,
each value x will have an observed value. E.g. for each hour of the day x you
can have a measured temperature. Or in the case of multi-dimensions e.g. each
pair of hour of the day at each height above the surface (x0, x1) you should
have a y value.

--------
Examples
--------

Simple linear example
---------------------

The example uses a set of x coordinates::

    from numpy import arange
    x = -1 + 0.1*arange(21)

The 'observed' values used are a simple 1-dim polynomial of order 2:

1 + 2(x+1) + 0.03(x+1)^2 == 3.03 +2.06x + 0.03x^2

We fill these values using the polynomial functional::

    y = functionals.poly(2, [3.03, 2.06, 0.03])(x)

To take the average of these points, we can do::

    dfit.linear(functionals.compiled('p'), [], y)

Note that an expression uses p (which is p0), p1 and x, x0, x1. Note also that
since no argument is used in the expression, no x-values have to be given.

We can get solutions and errors from these data (see for details the separate
routine descriptions)::

    >>> dfit.solution()
    3.041
    # Compare with the result:
    >>> print sum(y)/len(y)
    3.041
    >>> print dfit.sd()	# standard deviation per observation
    1.27824
    >>> print dfit.stddev()	# standard deviation per weight
    1.27824
    >>> print dfit.error()	# errors in solved parameters
    array( [0.278934])
    >>> print dfit.rank()	# rank of solution
    1
    >>> print dfit.covariance() # covariance matrix
    [[0.047619]]

We can also try to use a 0-order polynomial. Note that a polynomial, even a
zero-order one, is a 1-dim function, and we need an x defined::

    >>> dfit.linear(dfs.poly(0), [], y)
    RuntimeError: Linear fitter x and y lengths disagree
    >>> dfit.linear(dfs.poly(0),x,y)
    print >>> dfit.solution()
    3.041

We would like to check the results, so we will do an average in a separate
fitter::

    >>> id = dfit.fitter()	# get a new fitter
    >>> dfit.linear(dfs.compiled('p'), [], y, fid=id) # get average
    >>> dfit.solution() - dfit.solution(fid=id) # check difference
    -4.44089e-16
    # to really show we recalculate and check separately:
    >>> dfit.linear(dfs.compiled('p'), [], array(y)/2, fid=id) # calculate new average
    >>> print dfit.solution() - dfit.solution(fid=id)
    [1 .5205]

A 1-order polynomial is now easy::

    >>> dfit.linear(dfs.poly(1), x, y)
    >>> print dfit.solution()
    [3.041, 2.06]
    >>> print dfit.chi2()
    0.00201894
    >>> print dfit.error()
    [0.00224944, 0.00371484]
    >>> print dfit.sd()
    0.0103082

Note that each 'equation' can also be given a weight or standard deviation.

2-dimensional example
---------------------

A 2-dim model is done the same way. The x vector has now n pairs of values.
The Glish rbind can help in creating these pairs::

    >>> x1 = arange(1, 6)
    >>> x2 = 0.1*x1
    >>> x1 = ravel(array([x1,x2]).transpose()) # combine into pairs. Check:
    >>> print x1
    array([ 1. ,  0.1,  2. ,  0.2,  3. ,  0.3,  4. ,  0.4,  5. ,  0.5])
    >>> dfit.linear(dfs.compiled('p*x + p1*sin(x1)'), x1,
    dfs.compiled('3*x+7*sin(x[2])').f(x1))
    >>> print dfit.solution()
    [ 3. 7.]


Non-linear simple example
-------------------------

If the model is non-linear in the parameters to be solved, the functional
method should be used. The main difference is that a guess solution must be
inserted in the model parameters. In the following that is not necessary,
since the default zero values suffice if the function is linear::

    >>> dfit.functional(dfs.compiled('p*x + p1*sin(x1)'), x1,
        dfs.compiled('3*x+7*sin(x[2])').f(x1), id=id)
    >>> dfit.solution(fid=id)
    [ 3. 7.]
    >>> dfit.solution(fid=id)-dfit.solution()
    [  6.17284002e-13  -6.35846931e-12]
    # Try with an intial guess
    >>> dfit.functional(dfs.compiled('p*x + p1*sin(x1)', [3,7]), x1,
    dfs.compiled('3*x+7*sin(x[2])').f(x1), fid=id2)
    >>> dfit.solution(fid=id2)
    [ 3. 7.]
    >>> dfit.solution(fid=id2)-dfit.solution()
    [  6.17284002e-13  -6.35846931e-12]


Functional variety
------------------

Just to show the model can be anything, we redo the fit of an order 1
polynomial to the x, y data::

    >>> dfit.linear(dfs.poly(1), x,y)
    >>> dfit.solution()
    [ 3.041 2.06]

Now try the same by a sum of odd and even polynomials of default order
(note the order)::

    a = dfs.compound()
    a.add(dfs.functional('oddp'))
    a.add(dfs.functional('evenp'))
    dfit.linear(a,x,y,id=id2)
    dfit.solution(id=id2)
    [ 2.06 3.041]

And the combination of an odd (2x) and an even polynomial (3)::

    a = dfs.combi()
    a.add(dfs.functional('oddp', params=2))
    a.add(dfs.functional('evenp', params=3))
    dfit.linear(a, x, y)
    >>> dfit.solution()
    [ 1.03 1.01367]


Use constraints
---------------

We have measured a number of anlgles around a triangle. Each angle is measured
10 times (nominally 50, 60, 70 deg). Solving the angles will give::

    >>> import numpy
    >>> yz = numpy.array([numpy.zeros(10) + 50 + numpy.random.normal(0,1,10),
    numpy.zeros(10) + 60 + numpy.random.normal(0,1,10),
    numpy.zeros(10) + 70 + numpy.random.normal(0,1,10)]).flatten()
    # Create 3*10 equations
    >>> xz = array([1,0,0]*10 + [0,1,0]*10 + [0,0,1]*10)
    # The equation used and solve
    >>> f = dfs.compiled('p*x+p1*x1+p2*x2')
    >>> dfit.linear(f, xz, yz)
    >>> print dfit.solution(), 'sum=', sum(dfit.solution())
    [49.7079 60.2427 70.092]  sum= 180.043
    >>> dfit.error()
    [ 0.334828 0.334828 0.334828]
    # Add a constraint: sum of angles 180deg
    >>> dfit.addconstraint(x=[1,1,1],y=180)
    >>> dfit.linear(f,xz,yz)
    >>> print dfit.solution(), 'sum=', sum(dfit.solution())
    [ 49.6937 60.2285 70.0778]  sum= 180
    >>> print dfit.error()
    [ 0.273413 0.273413 0.273413]
    # Add another constraint, since we know second angle 60deg
    >>> dfit.addconstraint(x=[0,1,0], y=60)
    >>> dfit.linear(f,xz,yz)
    >>> print dfit.solution(), 'sum=', sum(dfit.solution())
    [ 49.8079 60 70.1921]  sum= 180
    >>> print dfit.error()
    [0.239827 0 0.239827]


Non-linear equation and constraints
-----------------------------------

In the following we have 2 Gaussian profiles and an offset. We add some noise,
and solve assuming we have a fair estimate of the position of the Gaussians.
Note that if the first estimate is beyond the real half-value point, the
fitting will be difficult, due to the derivatives changing sign::

    # The profile to generate and the parameters to use
    # (in essence 10 + 20 * exp (-((x-10)/4)^2) + 10 * exp(-((x-33)/4)^2) )
    f = dfs.compiled('p6+p0*exp(-((x-p1)/p2)^2) + p3*exp(-((x-p4)/p5)^2)',
    [20, 10, 4, 10, 33, 4, 10])
    xg = 0.5 * numpy.arange(1, 101) - 0.5
    yg = numpy.array(f(xg)) + numpy.random.normal(0,0.3,100)
    # Make an intial guess
    f.set_parameters([22, 11, 5, 10, 30, 5, 9])
    # Solve
    dfit.clearconstraints()
    dfit.functional(f,xg,yg)
    print dfit.solution()
    print dfit.solution() - numpy.array([20., 10, 4, 10, 33, 4, 10])
    print dfit.error()
    [0.211312 0.0334257 0.0527771 0.213666 0.0652003 0.102782 0.082641]
    # We know that the two lines have a peak ratio of 2: Amp1-2Amp2 = 0
    dfit.addconstraint([1, 0, 0, -2, 0, 0, 0])
    dfit.functional(f, xg, yg)
    print dfit.solution()
    print dfit.solution() - numpy.array([20., 10, 4, 10, 33, 4, 10])
    print dfit.solution()[0]/dfit.solution()[3]
    print dfit.error()
    # We know that the lines originated in same place: width1 == width2
    # Note that the default assumed value is 0.0
    dfit.addconstraint([0, 0, 1, 0, 0, -1, 0])
    dfit.functional(f, xg, yg)
    print dfit.solution()
    dfit.solution() - numpy.array([20, 10, 4, 10, 33, 4, 10])
    dfit.solution()[2]-dfit.solution()[5]
    dfit.error()
    # And see what happens if we assume that the widths are 4
    dfit.addconstraint([0, 0, 1, 0, 0, 0, 0], 4)
    dfit.functional(f, xg, yg)
    dfit.solution()
    dfit.solution() - [20, 10, 4, 10, 33, 4, 10]
    dfit.error()



Deficient solutions and SVD constraints
---------------------------------------

*DOES NOT WORK*

In some cases solutions of the least-squares equations is not completely
possible. An example is e.g. the solution of the closures equations in
synthesis calibrations, where a missing phase zero and slope and a missing
absolute gain cannot be solved for. The fitting described here will always
provide a solution, even in the case of a set of incomplete equations. After
the solution the deficiency can be checked. If there is a rank deficiency,
the set of 'constraints' that makes a solution possible (in a way similar to
SVD, i.e. providing a missing set of orthogonal equations) is available
through the constr function::

    # Provide a set of equations.
    x = array([1,1,1]*10)
    y = 180 + numpy.zeros(10) + numpy.random.normal(0, 3, 10)
    f = dfs.functional('hyper', 3)
    dfit.linear(f,x,y)
    dfit.deficiency()
    2
    dfit.solution()
    [60.0262 60.0262 60.0262]
    dfit.constraint()
    [-1 0 1 -1 1 0]
    # The SVD constraints can be used as constraints in subsequent solutions:
    dfit.addconstraint(x=dfit.constraint(1))
    T
    dfit.addconstraint(x=dfit.constraint(2))
    T
    dfit.linear(f,xz,yz)
    T
    dfit.solution()
    [60.0262 60.0262 60.0262]
    dfit.rank()
    3
    dfit.deficiency()
    0
    dfit.error()
    [0.202801 0.202801 0.202801]


Complex fitting
---------------

The fitter can handle functions of complex variables. In the following example
a second order polynomial is first fitted real with a first order linear
polynomial. The same is repeated complex (with real data); and then a complex
value is fitted. An example of a 2-dimensional non-linear function is also
given::

    # Define x and y data
    >>> x = -1 + numpy.arange(0,21)*0.1
    >>> y = dfs.poly(2, [3.03, 2.06, 0.03])(x)

    # fit a first order polynomial
    >>> dfit.linear(dfs.poly(1), x,y)
    >>> print 'linear', dfit.solution()
    linear [ 3.041 2.06]

    # Get a complex fitter and see the same fit
    >>> id1 = dfit.fitter()
    >>> dfit.set(ftype='complex', fid=id1)
    >>> dfit.linear(dfs.poly(1, dtype='complex'), x, y, fid=id1)
    >>> dfit.solution(fid=id1)
    [ 3.041+0j 2.06+0j]

    # Make a complex yi and redo
    >>> yi = dfs.poly(2, [3.03, 2.06, 0.03])(x)
    >>> yi = yi - 3j*array(dfs.poly(2, [3.03+0j, 2.06, 0.03])(x))
    >>> dfit.linear(dfs.poly(1, dtype='complex'), x, yi, fid=id1)
    >>> dfit.solution(fid=id1)
    [ 3.041-9.123j 2.06-6.18j]

    # A non-linear 2-dimensional function, real and complex
    >>> id2 = dfit.fitter()
    >>> dfit.functional(dfs.compiled('p*x + p1*sin(x1)', [3,7]), x1,
                    dfs.compiled('3*x+7*sin(x[2])')(x1), fid=id2)
    >>> x1 = arange(1,6)
    >>> x2 = 0.1*x1
    >>> x1 = array(zip(x1,x2)).flatten()
    >>> dfit.functional(dfs.compiled('p*x + p1*sin(x1)', [3,7]),x1,
                    dfs.compiled('3*x+7*sin(x[2])').f(x1), fid=id2)
    >>> dfit.solution(fid=id2)
    >>> dfit.set(type=dfit.complex(), fid=id2)
    >>> dfit.functional(dfs.compiled('p*x + p1*sin(x1)', [3,7]),x1,
                    dfs.compiled('3*x+7*sin(x[2])').f(x1), fid=id2)
    >>> dfit.solution(fid=id2)

"""
from .fitting import *
