import unittest
from casacore import fitting


class TestFitting(unittest.TestCase):
    def setUp(self):
        self.fitserver = fitting.fitserver()

    def test_fitter(self):
        self.fitserver.fitter()