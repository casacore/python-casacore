import unittest
from casacore.quanta import *


class TestQuanta(unittest.TestCase):
    def test_quanta(self):
        q0 = quantity('1deg')
        self.assertTrue(is_quantity(q0))
        q1 = quantity(1.0, 'deg')
        self.assertTrue(is_quantity(q1))
        self.assertEqual(q1, q0)

        q2 = quantity([180.0, 0.0], 'deg')
        self.assertTrue(is_quantity(q2))
        self.assertNotEqual(q1, q2)
        self.assertEqual(str(q0+q1), '2 deg')
        self.assertEqual(str(q0-q1), '0 deg')
        self.assertEqual(str(q0*q1), '1 deg.deg')
        self.assertEqual(str(q0/q1), '1 deg/(deg)')
        self.assertEqual(str(q0+1), '2 deg')
        self.assertEqual(str(q2+[1, 1]), '[181, 1] deg')
        print(sin(q0))
        print(sin(q2))
        self.assertEqual(str(q0.get()), '0.017453 rad')
        self.assertEqual(str(q0.get('h')), '0.066667 h')
        self.assertEqual(str(q0.canonical()), '0.017453 rad')
        self.assertEqual(str(q0.get_value()), '1.0')
        self.assertEqual(str(q0.get_value('arcsec')), '3600.0')
        self.assertEqual(q0.get_unit(), 'deg')

        q3 = quantity('12h10m5s')
        print(q3.to_time())
        self.assertEqual(str(q3.to_unix_time()), '-3506672995.0')
        print(q3.to_angle())
        self.assertEqual(q3.formatted("ANGLE"), '+182.31.15')
        self.assertEqual(q3.to_string("%0.3f"), '182.521 deg')
        q4 = quantity({'unit': 'deg', 'value': 182.52083333333334})
        self.assertEqual(q3, q4)
        q5 = quantity(q4)
        self.assertEqual(q5, q4)

        self.assertIn('Jy', units)
        self.assertEqual(units['Jy'], ['jansky', quantity(1e-26, 'kg.s-2')])
        self.assertIn('a', prefixes)
        self.assertEqual(prefixes['a'], ['atto', 1e-18])

        boltzmann = constants['k']
        self.assertEqual(str(boltzmann), '1.3807e-23 J/K')
