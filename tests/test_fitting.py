import unittest
from casacore import fitting, functionals
import numpy as np


class TestFitting(unittest.TestCase):
    """Test class for Fitting module."""

    def setUp(self):
        """Set up fitserver for all the tests."""
        self.fitserver = fitting.fitserver()

    def test_fitter(self):
        """Testing fitter."""
        self.fitserver.fitter()

    def test_fitserver(self):
        """Testing fitserver."""
        self.assertEqual(self.fitserver.getstate(),
                         {'colfac': 1e-08,
                          'lmfac': 0.001,
                          'n': 0,
                          'typ': 'real'})
        self.fitserver.set(n=1, colfac=1.0e-09, lmfac=1.0e-2, ftype=1)
        self.assertEqual(self.fitserver.getstate(),
                         {'colfac': 1e-09,
                          'lmfac': 0.01,
                          'n': 1,
                          'typ': 'complex'})

    def test_poly(self):
        """Test poly."""
        x = -1 + 0.1 * np.arange(21)
        y = functionals.poly(2, [3.03, 2.06, 0.03])(x)
        self.fitserver.linear(functionals.compiled('p'), [], y)
        np.testing.assert_equal(self.fitserver.solution(), sum(y)/len(y))
        np.testing.assert_equal(self.fitserver.sd(), self.fitserver.stddev())
        np.testing.assert_allclose(self.fitserver.error(),
                                   np.array([0.27893394]))
        self.assertAlmostEqual(self.fitserver.chi2(), 32.6777389399999)
        self.assertEqual(self.fitserver.rank(), 1)
        np.testing.assert_allclose(self.fitserver.covariance()[0],
                                   np.array([0.04761905]))

    def test_functional(self):
        """Test functional method."""
        f = functionals.compiled('p6+p0*exp(-((x-p1)/p2)^2)' +
                                 ' + p3*exp(-((x-p4)/p5)^2)',
                                 [20, 10, 4, 10, 33, 4, 10])
        xg = 0.5 * np.arange(1, 101) - 0.5
        yg = np.array(f(xg)) + np.random.normal(0, 0.3, 100)
        f.set_parameters([22, 11, 5, 10, 30, 5, 9])
        self.fitserver.clearconstraints()
        self.fitserver.functional(f, xg, yg)
        print(self.fitserver.solution())

    def test_complex_fitting(self):
        """Testing complex fitting."""
        x = -1 + np.arange(0, 21)*0.1
        y = functionals.poly(2, [3.03, 2.06, 0.03])(x)
        self.fitserver.linear(functionals.poly(1), x, y)
        print('linear', self.fitserver.solution())
        id1 = self.fitserver.fitter()
        self.fitserver.set(ftype='complex', fid=id1)
        self.fitserver.linear(functionals.poly(1, dtype='complex'), x, y,
                              fid=id1)
        np.testing.assert_allclose(self.fitserver.solution(fid=id1),
                                   np.array([3.041+0.j, 2.060+0.j]))

    def test_constraint(self):
        """Test constraint."""
        from casacore import functionals as dfs
        yz = np.array([np.zeros(10) + 50 + np.random.normal(0, 1, 10),
                       np.zeros(10) + 60 + np.random.normal(0, 1, 10),
                       np.zeros(10) + 70 + np.random.normal(0, 1, 10)]
                      ).flatten()
        xz = np.array([1, 0, 0]*10 + [0, 1, 0]*10 + [0, 0, 1]*10)
        f = dfs.compiled('p*x+p1*x1+p2*x2')
        self.fitserver.linear(f, xz, yz)
        self.fitserver.addconstraint(x=[1, 1, 1], y=180)
        self.fitserver.linear(f, xz, yz)
        self.assertAlmostEqual(sum(self.fitserver.solution()), 180.0)
        self.fitserver.clearconstraints()

    def test_fitspoly(self):
        """Test fitspoly."""
        x = np.arange(1, 11)
        y = 2. + 0.5*x - 0.1*x**2
        self.fitserver.fitspoly(3, x, y)
        np.testing.assert_allclose(self.fitserver.solution(),
                                   np.array([2.00000000e+00,
                                             5.00000000e-01,
                                             -1.00000000e-01,
                                             -4.70734562e-14]))

    def test_fitavg(self):
        """Test fitavg."""
        x = np.arange(1, 11)
        y = 2. + 0.5*x - 0.1*x**2
        self.fitserver.fitavg(y)
        np.testing.assert_allclose(self.fitserver.solution(),
                                   np.array([0.9]))

    def test_done(self):
        """Test done method."""
        fit = fitting.fitserver()
        x = np.arange(1, 11)
        y = 1. + 2*x - x**2
        fit.fitpoly(3, x, y)
        np.testing.assert_allclose(fit.solution()[0], 1)
        fit.done()
        with self.assertRaises(ValueError):
            fit.solution()
