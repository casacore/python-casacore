#!/usr/bin/env python
from unittest import TestCase

import numpy as np
from casacore._tConvert import tConvert


class TestConvert(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = tConvert()

    def arrvh(self, arr):
        print('    testarrvh')
        print(self.t.testvh(arr))
        print(self.t.testvh(arr[0]))
        print(self.t.testvh([arr[0]]))
        print(self.t.testvh([arr[0], arr[1]]))

    def arrb(self, arr):
        self.arrvh(arr)
        print(self.t.testbool(arr[0]))

    def arri(self, arr):
        self.arrvh(arr)
        print(self.t.testint(arr[0]))
        print(self.t.testint64(arr[0]))
        print(self.t.testssize(arr[0]))
        print(self.t.testfloat(arr[0]))
        print(self.t.testcomplex(arr[0]))

    def arrf(self, arr):
        self.arrvh(arr)
        print(self.t.testfloat(arr[0]))
        print(self.t.testcomplex(arr[0]))

    def arrc(self, arr):
        self.arrvh(arr)
        print(self.t.testcomplex(arr[0]))

    def test_na(self):
        # Test byte and sbyte.
        b = np.array([-1, -2], np.int8)
        print(self.t.testvh(b))
        # UInt8 is Bool, therefore use Int16.
        b = np.array([211, 212], np.int16)
        print(self.t.testvh(b))
        print('>>>')
        res = self.t.testvh(np.array((0,)))
        print('<<<')
        print(res.shape)
        print(self.t.testvh({'shape': [2, 2], 'array': ['abcd', 'c', '12', 'x12']}))

    def test_np(self):
        # Test byte and sbyte.
        b = np.int8([-1, -2])
        print(self.t.testvh(b))
        b = np.uint8([211, 212])
        print(self.t.testvh(b))
        print('>>>')
        res = self.t.testvh(np.array([]))
        print('<<<')
        print(res.shape)
        print(self.t.testvh(np.array([["abcd", "c"], ["12", "x12"]])))

    def test_nps(self):
        self.arrb(np.array([True, False]))
        self.arri(np.array([-6, -7], dtype=np.int8))
        self.arri(np.array([5, 6], dtype=np.uint8))
        self.arri(np.array([-16, -17], dtype=np.int16))
        self.arri(np.array([15, 16], dtype=np.uint16))
        self.arri(np.array([-26, -27], dtype=np.int32))
        self.arri(np.array([25, 26], dtype=np.uint32))
        self.arri(np.array([-36, -37], dtype=np.int64))
        self.arri(np.array([35, 36], dtype=np.uint64))
        self.arrf(np.array([-46, -47], dtype=np.float32))
        self.arrf(np.array([45, 46], dtype=np.float64))
        self.arrc(np.array([-56 - 66j, -57 - 67j], dtype=np.complex64))
        self.arrc(np.array([-76 - 86j, -77 - 87j], dtype=np.complex128))

    def test_main(self):
        print('')
        print('begin dotest')
        print(self.t.testbool(True))
        print(self.t.testbool(False))
        print(self.t.testint(-1))
        print(self.t.testint(10))
        print(self.t.testint64(-123456789013))
        print(self.t.testint64(123456789014))
        print(self.t.testssize(-2))
        print(self.t.testssize(11))
        print(self.t.testfloat(3.14))
        print(self.t.testfloat(12))
        print(self.t.testdouble(3.14))
        print(self.t.testdouble(12))
        print(self.t.teststring("this is a string"))
        print(self.t.testunicode(u"this is a unicode"))

        arr = np.array([2, 3], np.int32)
        print(self.t.testint(arr[0]))
        print(self.t.testint64(arr[0]))
        print(self.t.testfloat(arr[0]))
        print(self.t.testdouble(arr[0]))
        arr = np.array([2.2, 3.2], np.float32)
        print(self.t.testint(arr[0]))
        print(self.t.testfloat(arr[0]))
        print(self.t.testdouble(arr[0]))
        arr = np.array([2.4, 3.4], np.float64)
        print(self.t.testint(arr[0]))
        print(self.t.testfloat(arr[0]))
        print(self.t.testdouble(arr[0]))

        print(self.t.testipos([2, 3, 4]))
        print(self.t.testipos(1))
        print(self.t.testipos(np.array([2])))
        print(self.t.testipos(np.array(3)))

        print(self.t.testvecint([1, 2, 3, 4]))
        print(self.t.testvecint([]))
        print(self.t.testvecint((-1, -2, -3, -4)))
        print(self.t.testvecint(-10))
        print(self.t.testvecint(np.array((10, 11, 12))))
        print(self.t.testvecint(np.array(1)))
        print(self.t.testveccomplex([1 + 2j, -1 - 3j, -1.5 + 2.5j]))
        print(self.t.testvecstr(["a1", "a2", "b1", "b2"]))
        print(self.t.testvecstr(()))
        print(self.t.testvecstr("sc1"))
        print(self.t.teststdvecuint([1, 2, 4]))
        print(self.t.teststdvecuint(()))
        print(self.t.teststdvecuint(10))
        print(self.t.teststdvecvecuint([[1, 2, 4]]))
        print(self.t.teststdvecvecuint((())))
        print(self.t.teststdvecvecuint(()))
        print(self.t.teststdvecvecuint([1, 2, 4]))
        print(self.t.teststdvecvecuint(20))

        print(self.t.testvh(True))
        print(self.t.testvh(2))
        print(self.t.testvh(1234567890123))
        print(self.t.testvh(1.3))
        print(self.t.testvh(10 - 11j))
        print(self.t.testvh("str"))
        print(self.t.testvh([True]) + 0)  # add 0 to convert nppy to integer)
        print(self.t.testvh([2, 4, 6, 8, 10]))
        print(self.t.testvh([1.3, 4, 5, 6]))
        print(self.t.testvh([10 - 11j, 1 + 2j]))
        #    print(self.t.testvh ([]))
        print(self.t.testvh(["str1", "str2"]))
        print(self.t.testvh({"shape": [2, 2], "array": ["str1", "str2", "str3", "str4"]}))
        a = self.t.testvh({"shape": [2, 2], "array": ["str1", "str2", "str3", "str4"]})
        print(a)
        print(self.t.testvh(a))

        print(self.t.testvh([u"str1", u"str2"]))
        print(self.t.testvh({"shape": [2, 2], "array": [u"str1", u"str2", u"str3", u"str4"]}))
        a1 = self.t.testvh({"shape": [2, 2], "array": [u"str1", u"str2", u"str3", u"str4"]})
        print(a1)
        print(self.t.testvh(a1))

        a = self.t.testvh([10 - 11j, 1 + 2j])
        print(a.shape)
        print(self.t.testvh(a))

        b = np.int32([[2, 3], [4, 5]])
        print(b)
        print(self.t.testvh(b))

        b = np.int32([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        print(b[2:9:2])
        print(self.t.testvh(b[2:9:2]))

        b = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10.])
        print(b[2:9:2])
        print(self.t.testvh(b[2:9:2]))
        a = b[2:9:2]
        print(self.t.testvh(a))

        print(self.t.testvh(np.array([20. + 10j])))
        print(self.t.testvh(np.array(21.)))

        print('>>>')
        res = self.t.testvh(np.array([]))
        print('<<<')
        print(res.shape)
        print('>>>')
        res = self.t.testvh(np.array([[]]))
        print('<<<')
        print(res.shape)

        # On 64-bit machines the output also contains 'dtype=int32'
        # So leave it out.
        a = self.t.testrecord({"int": 1, "int64": 123456789012, "str": "bc", 'vecint': [1, 2, 3]})
        print('>>>')
        print(a)
        print('<<<')
        print('end dotest')
        print('')
