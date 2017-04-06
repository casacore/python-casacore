import unittest2 as unittest
from casacore import functionals


class TestFunctionals(unittest.TestCase):

    def test_something(self):
        # self.functional = functionals.functional(name='test')
        # functionals.chebyshev(self.functional)
        return

    def test_gaussian1d(self, dtype=None):
        if dtype != None:
            gauss1d = functionals.gaussian1d([1, 2, 3], dtype)
        else:
            gauss1d = functionals.gaussian1d([1, 2, 3])

        self.assertTrue(gauss1d.ndim() == 1)
        self.assertTrue(gauss1d.npar() == 3)
        self.assertTrue(gauss1d.__len__() == 3)

        self.assertTrue(gauss1d.get_parameters() == [1, 2, 3])
        gauss1d.set_parameters([3, 4, 5])
        self.assertTrue(gauss1d.get_parameters() == [3, 4, 5])
        gauss1d.set_parameter(0, 2)
        self.assertTrue(gauss1d.get_parameters()[0] == 2)

        self.assertTrue(gauss1d.get_masks() == [True, True, True])
        gauss1d.set_mask(0, False)
        self.assertTrue(gauss1d.get_masks() == [False, True, True])
        # gauss1d.set_masks([True, True, True])
        # self.assertTrue(gauss1d.get_masks() == [True, True, True]

        gauss1d.set_parameters([0, 0, 1])
        self.assertTrue(gauss1d.f(0) == [0])

    def test_gaussian1d_dtype(self):
        self.test_gaussian1d(1)

    def test_poly(self, dtype=None):
        if dtype != None:
            a = functionals.poly(3, dtype)
        else:
            a = functionals.poly(3)

        self.assertTrue(a.ndim() == 1)
        self.assertTrue(a.npar() == 4)
        self.assertTrue(a.__len__() == 4)

        a.set_parameters([4, 3, 2, 1])
        self.assertTrue(a.get_parameters() == [4.0, 3.0, 2.0, 1.0])
        a.set_parameter(0, 0)
        self.assertTrue(a.get_parameters()[0] == 0.0)

        self.assertTrue(a.get_masks() == [True, True, True, True])
        a.set_mask(0, False)
        self.assertTrue(a.get_masks() == [False, True, True, True])

        a.set_parameters([0, 0, 1,1])
        self.assertTrue(a.f(0) == [0])

    def test_poly_dtype(self):
        self.test_poly(1)