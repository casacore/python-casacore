import unittest
from casacore.functionals import *


class TestFunctionals(unittest.TestCase):

    def test_something(self):
        # self.functional = functionals.functional(name='test')
        # functionals.chebyshev(self.functional)
        return

    def test_gaussian1d(self, dtype=None):
        if dtype is not None:
            gauss1d = gaussian1d([1, 2, 3], dtype=dtype)
        else:
            gauss1d = gaussian1d([1, 2, 3])
        self.assertEqual(type(repr(gauss1d)), str)
        self.assertEqual(gauss1d.ndim(), 1)
        self.assertEqual(gauss1d.npar(), 3)
        self.assertEqual(gauss1d.npar(), len(gauss1d))

        self.assertEqual(gauss1d.get_parameters(), [1.0, 2.0, 3.0])
        gauss1d.set_parameters([4.0, 5.0, 6.0])
        self.assertEqual(gauss1d.get_parameters(), [4.0, 5.0, 6.0])
        gauss1d.set_parameter(0, 2)
        self.assertEqual(gauss1d.get_parameters()[0], 2)

        self.assertEqual(gauss1d.get_masks(), [True, True, True])
        gauss1d.set_mask(0, False)
        self.assertEqual(gauss1d.get_masks()[0], False)
        gauss1d.set_masks([True, True, True])
        self.assertEqual(gauss1d.get_masks()[0], True)

        numpy.testing.assert_array_equal(gauss1d(0), gauss1d.f(0))
        if dtype is None:
            numpy.testing.assert_array_equal(gauss1d(1, derivatives=True),
                                             gauss1d.fdf(1))

    def test_gaussian1d_dtype(self):
        self.test_gaussian1d(dtype='complex')

    def test_gaussian2d(self, dtype=None):
        if dtype is not None:
            gauss2d = gaussian2d(numpy.array([[1, 2, 3], [4, 5, 6]]), dtype=dtype)
        else:
            gauss2d = gaussian2d(numpy.array([[1, 2, 3], [4, 5, 6]]))

        self.assertEqual(type(repr(gauss2d)), str)
        self.assertEqual(gauss2d.ndim(), 2)
        self.assertEqual(gauss2d.npar(), 6)
        self.assertEqual(gauss2d.npar(), len(gauss2d))

        self.assertEqual(gauss2d.get_parameters(), [1.0, 2.0, 3.0,
                                                    4.0, 5.0, 6.0])
        gauss2d.set_parameters([4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        self.assertEqual(gauss2d.get_parameters(), [4.0, 5.0, 6.0,
                                                    7.0, 8.0, 9.0])
        gauss2d.set_parameter(0, 2)
        self.assertEqual(gauss2d.get_parameters()[0], 2)

        self.assertEqual(gauss2d.get_masks(), [True, True, True,
                                               True, True, True])
        gauss2d.set_mask(0, False)
        self.assertEqual(gauss2d.get_masks()[0], False)
        gauss2d.set_masks([True, True, True, True, True, True])
        self.assertEqual(gauss2d.get_masks()[0], True)

        numpy.testing.assert_array_equal(gauss2d([1, 2]), gauss2d.f([1, 2]))
        if dtype is None:
            numpy.testing.assert_array_equal(gauss2d([1, 2], derivatives=True),
                                             gauss2d.fdf([1, 2]))

    def test_gaussian2d_dtype(self):
        self.test_gaussian2d(dtype='complex')

    def test_poly(self, dtype=None):
        if dtype is not None:
            p = poly(3, dtype=dtype)
        else:
            p = poly(3)

        self.assertEqual(type(repr(p)), str)
        self.assertTrue(p.ndim(), 1)
        self.assertTrue(p.npar(), 4)
        self.assertEqual(p.npar(), len(p))

        self.assertTrue(p.get_parameters() == [1.0, 1.0, 1.0, 1.0])
        p.set_parameters([4, 3, 2, 1])
        self.assertTrue(p.get_parameters() == [4.0, 3.0, 2.0, 1.0])
        p.set_parameter(0, 0)
        self.assertEqual(p.get_parameters()[0], 0.0)

        self.assertEqual(p.get_masks(), [True, True, True, True])
        p.set_mask(0, False)
        self.assertEqual(p.get_masks()[0], False)
        p.set_masks([True, False, True, True])
        self.assertEqual(p.get_masks()[1], False)

        numpy.testing.assert_array_equal(p(0), p.f(0))
        numpy.testing.assert_array_equal(p(1), numpy.array([6.]))
        if dtype is None:
            numpy.testing.assert_array_equal(p(0, derivatives=True), p.fdf(0))
            numpy.testing.assert_array_equal(
                p.fdf(0), numpy.array([[0., 1., 0., 0., 0.]]))

    def test_poly_dtype(self):
        self.test_poly(dtype='complex')

    def test_oddpoly(self, dtype=None):
        if dtype is not None:
            op = oddpoly(3, dtype=dtype)
        else:
            op = oddpoly(3)

        self.assertEqual(type(repr(op)), str)
        self.assertTrue(op.ndim(), 1)
        self.assertTrue(op.npar(), 2)
        self.assertEqual(op.npar(), len(op))

        self.assertTrue(op.get_parameters() == [1.0, 1.0])
        op.set_parameters([2, 1])
        self.assertTrue(op.get_parameters() == [2.0, 1.0])
        op.set_parameter(0, 0)
        self.assertEqual(op.get_parameters()[0], 0.0)

        self.assertEqual(op.get_masks(), [True, True])
        op.set_mask(0, False)
        self.assertEqual(op.get_masks()[0], False)
        op.set_masks([True, False])
        self.assertEqual(op.get_masks()[1], False)

        numpy.testing.assert_array_equal(op(0), op.f(0))
        numpy.testing.assert_array_equal(op(1), numpy.array([1.]))
        if dtype is None:
            numpy.testing.assert_array_equal(op(0, derivatives=True), op.fdf(0))
            numpy.testing.assert_array_equal(
                op.fdf(1), numpy.array([[1., 1., 0.]]))

    def test_oddpoly_dtype(self):
        self.test_oddpoly(dtype='complex')

    def test_evenpoly(self, dtype=None):
        if dtype is not None:
            ep = evenpoly(3, dtype=dtype)
        else:
            ep = evenpoly(3)

        self.assertEqual(type(repr(ep)), str)
        self.assertTrue(ep.ndim(), 1)
        self.assertTrue(ep.npar(), 2)
        self.assertEqual(ep.npar(), len(ep))

        self.assertTrue(ep.get_parameters() == [1.0, 1.0])
        ep.set_parameters([2, 1])
        self.assertTrue(ep.get_parameters() == [2.0, 1.0])
        ep.set_parameter(0, 0)
        self.assertEqual(ep.get_parameters()[0], 0.0)

        self.assertEqual(ep.get_masks(), [True, True])
        ep.set_mask(0, False)
        self.assertEqual(ep.get_masks()[0], False)
        ep.set_masks([True, False])
        self.assertEqual(ep.get_masks()[1], False)

        numpy.testing.assert_array_equal(ep(0), ep.f(0))
        numpy.testing.assert_array_equal(ep(1), numpy.array([1.]))
        if dtype is None:
            numpy.testing.assert_array_equal(ep(0, derivatives=True), ep.fdf(0))
            numpy.testing.assert_array_equal(
                ep.fdf(1), numpy.array([[1., 1., 0.]]))

    def test_evenpoly_dtype(self):
        self.test_evenpoly(dtype='complex')

    def test_chebyshev(self, dtype=None):
        if dtype is not None:
            ch = chebyshev(3, dtype=dtype)
        else:
            ch = chebyshev(3)

        self.assertEqual(type(repr(ch)), str)
        self.assertTrue(ch.ndim(), 1)
        self.assertTrue(ch.npar(), 4)
        self.assertEqual(ch.npar(), len(ch))

        self.assertTrue(ch.get_parameters() == [1.0, 1.0, 1.0, 1.0])
        ch.set_parameters([4, 3, 2, 1])
        self.assertTrue(ch.get_parameters() == [4, 3, 2, 1])
        ch.set_parameter(0, 0)
        self.assertEqual(ch.get_parameters()[0], 0.0)

        self.assertEqual(ch.get_masks(), [True, True, True, True])
        ch.set_mask(0, False)
        self.assertEqual(ch.get_masks()[0], False)
        ch.set_masks([True, False, True, False])
        self.assertEqual(ch.get_masks()[1], False)

        numpy.testing.assert_array_equal(ch(0), ch.f(0))
        numpy.testing.assert_array_equal(ch(1), numpy.array([6.]))
        if dtype is None:
            numpy.testing.assert_array_equal(ch(0, derivatives=True), ch.fdf(0))
            numpy.testing.assert_array_equal(
                ch.fdf(1), numpy.array([[6., 1., 1., 1., 1.]]))

    # def test_chebyshev_dtype(self):
    #     self.test_chebyshev(dtype='complex')

    def test_compound(self, dtype=None):
        if dtype is not None:
            p = poly(3, dtype=dtype)
        else:
            p = poly(3)

        self.assertEqual(type(repr(p)), str)
        self.assertTrue(p.ndim(), 1)
        self.assertTrue(p.npar(), 4)
        self.assertEqual(p.npar(), len(p))

        self.assertTrue(p.get_parameters() == [1.0, 1.0, 1.0, 1.0])
        p.set_parameters([4, 3, 2, 1])
        self.assertTrue(p.get_parameters() == [4.0, 3.0, 2.0, 1.0])
        p.set_parameter(0, 0)
        self.assertEqual(p.get_parameters()[0], 0.0)

        self.assertEqual(p.get_masks(), [True, True, True, True])
        p.set_mask(0, False)
        self.assertEqual(p.get_masks()[0], False)
        p.set_masks([True, False, True, True])
        self.assertEqual(p.get_masks()[1], False)

        numpy.testing.assert_array_equal(p(0), p.f(0))
        numpy.testing.assert_array_equal(p(1), numpy.array([6.]))

        d = poly(2)
        gauss1d = gaussian1d([1, 0, 1])
        sum = compound()
        sum.add(d)
        sum.add(gauss1d)
        numpy.testing.assert_allclose(sum(2), numpy.array([7.000015]))

        if dtype is None:
            numpy.testing.assert_array_equal(p(0, derivatives=True), p.fdf(0))
            numpy.testing.assert_array_equal(
                p.fdf(0), numpy.array([[0., 1., 0., 0., 0.]]))

    def test_compound_dtype(self):
        self.test_compound(dtype='complex')

    def test_combi(self, dtype=None):
        const = poly(0)
        linear = poly(1)
        square = poly(2)
        c = combi()
        c.add(const)
        c.add(linear)
        c.add(square)
        print(c(0))
    def test_combi_dtype(self):
        self.test_combi(dtype='complex')

    def test_compiled(self, dtype=None):
        a = compiled('sin(pi(0.5) ) +pi')
        numpy.testing.assert_allclose(a(0), numpy.array([4.14159265]))
        b = compiled('p*exp(-(x/p[2])^2)')
        self.assertEqual(b.get_parameters(), [0.0, 0.0])
        b.set_parameters([10, 1])
        numpy.testing.assert_allclose(b([-1, -0.5, 0, .5, 1]),
                                      numpy.array([3.67879441,
                                                   7.78800783,
                                                  10.,
                                                   7.78800783,
                                                   3.67879441]))
        synca = compiled('((x==0) * 1)+((x!=0) * sin(x+(x==0)*1)/(x+(x==0)*1))')
        numpy.testing.assert_allclose(synca([-1, 0, 1]),
                                      numpy.array([0.84147098,
                                                   1.,
                                                   0.84147098]))

