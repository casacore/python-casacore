#!/usr/bin/env python
from casacore._tConvert import tConvert
import numpy as np


def test_main(t):
    print('')
    print('begin dotest')
    print(t.testbool(True))
    print(t.testbool(False))
    print(t.testint(-1))
    print(t.testint(10))
    print(t.testint64(-123456789013))
    print(t.testint64(123456789014))
    print(t.testssize(-2))
    print(t.testssize(11))
    print(t.testfloat(3.14))
    print(t.testfloat(12))
    print(t.testdouble(3.14))
    print(t.testdouble(12))
    print(t.teststring("this is a string"))

    arr = np.array([2, 3], np.int32)
    print(t.testint(arr[0]))
    print(t.testint64(arr[0]))
    print(t.testfloat(arr[0]))
    print(t.testdouble(arr[0]))
    arr = np.array([2.2, 3.2], np.float32)
    print(t.testint(arr[0]))
    print(t.testfloat(arr[0]))
    print(t.testdouble(arr[0]))
    arr = np.array([2.4, 3.4], np.float64)
    print(t.testint(arr[0]))
    print(t.testfloat(arr[0]))
    print(t.testdouble(arr[0]))

    print(t.testipos([2, 3, 4]))
    print(t.testipos(1))
    print(t.testipos(np.array([2])))
    print(t.testipos(np.array(3)))

    print(t.testvecint([1, 2, 3, 4]))
    print(t.testvecint([]))
    print(t.testvecint((-1, -2, -3, -4)))
    print(t.testvecint(-10))
    print(t.testvecint(np.array((10, 11, 12))))
    print(t.testvecint(np.array(1)))
    print(t.testveccomplex([1 + 2j, -1 - 3j, -1.5 + 2.5j]))
    print(t.testvecstr(["a1", "a2", "b1", "b2"]))
    print(t.testvecstr(()))
    print(t.testvecstr("sc1"))
    print(t.teststdvecuint([1, 2, 4]))
    print(t.teststdvecuint(()))
    print(t.teststdvecuint(10))
    print(t.teststdvecvecuint([[1, 2, 4]]))
    print(t.teststdvecvecuint((())))
    print(t.teststdvecvecuint(()))
    print(t.teststdvecvecuint([1, 2, 4]))
    print(t.teststdvecvecuint(20))

    print(t.testvh(True))
    print(t.testvh(2))
    print(t.testvh(1234567890123))
    print(t.testvh(1.3))
    print(t.testvh(10 - 11j))
    print(t.testvh("str"))
    print(t.testvh([True]) + 0)  # add 0 to convert nppy to integer)
    print(t.testvh([2, 4, 6, 8, 10]))
    print(t.testvh([1.3, 4, 5, 6]))
    print(t.testvh([10 - 11j, 1 + 2j]))
    #    print(t.testvh ([]))
    print(t.testvh(["str1", "str2"]))
    print(t.testvh({"shape": [2, 2], "array": ["str1", "str2", "str3", "str4"]}))
    a = t.testvh({"shape": [2, 2], "array": ["str1", "str2", "str3", "str4"]})
    print(a)
    print(t.testvh(a))

    a = t.testvh([10 - 11j, 1 + 2j])
    print(a.shape)
    print(t.testvh(a))

    b = np.int32([[2, 3], [4, 5]])
    print(b)
    print(t.testvh(b))

    b = np.int32([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(b[2:9:2])
    print(t.testvh(b[2:9:2]))

    b = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10.])
    print(b[2:9:2])
    print(t.testvh(b[2:9:2]))
    a = b[2:9:2]
    print(t.testvh(a))

    print(t.testvh(np.array([20. + 10j])))
    print(t.testvh(np.array(21.)))

    print('>>>')
    res = t.testvh(np.array([]))
    print('<<<')
    print(res.shape)
    print('>>>')
    res = t.testvh(np.array([[]]))
    print('<<<')
    print(res.shape)

    # On 64-bit machines the output also contains 'dtype=int32'
    # So leave it out.
    a = t.testrecord({"int": 1, "int64": 123456789012, "str": "bc", 'vecint': [1, 2, 3]})
    print('>>>')
    print(a)
    print('<<<')
    print('end dotest')
    print('')


def testarrvh(arr):
    print('    testarrvh')
    print(t.testvh(arr))
    print(t.testvh(arr[0]))
    print(t.testvh([arr[0]]))
    print(t.testvh([arr[0], arr[1]]))


def testarrb(arr):
    testarrvh(arr)
    print(t.testbool(arr[0]))


def testarri(arr):
    testarrvh(arr)
    print(t.testint(arr[0]))
    print(t.testint64(arr[0]))
    print(t.testssize(arr[0]))
    print(t.testfloat(arr[0]))
    print(t.testcomplex(arr[0]))


def testarrf(arr):
    testarrvh(arr)
    print(t.testfloat(arr[0]))
    print(t.testcomplex(arr[0]))


def testarrc(arr):
    testarrvh(arr)
    print(t.testcomplex(arr[0]))


def testnps():
    testarrb(np.array([True, False]))
    testarri(np.array(object=[-6, -7]), dtype=np.int8)
    testarri(np.array(object=[5, 6]), dtype=np.uint8)
    testarri(np.array(object=[-16, -17]), dtype=np.int16)
    testarri(np.array(object=[15, 16]), dtype=np.uint16)
    testarri(np.array(object=[-26, -27]), dtype=np.int32)
    testarri(np.array(object=[25, 26]), dtype=np.uint32)
    testarri(np.array(object=[-36, -37]), dtype=np.int64)
    testarri(np.array(object=[35, 36]), dtype=np.uint64)
    testarrf(np.array(object=[-46, -47]), dtype=np.float32)
    testarrf(np.array(object=[45, 46]), dtype=np.float64)
    testarrc(np.array(object=[-56 - 66j, -57 - 67j]), dtype=np.complex64)
    testarrc(np.array(object=[-76 - 86j, -77 - 87j]), dtype=np.complex128)


def test_np():
    # Test byte and sbyte.
    b = np.int8([-1, -2])
    print(t.testvh(b))
    b = np.uint8([211, 212])
    print(t.testvh(b))
    print('>>>')
    res = t.testvh(np.array([]))
    print('<<<')
    print(res.shape)
    print(t.testvh(np.array([["abcd", "c"], ["12", "x12"]])))
    testnps()


def test_na():
    # Test byte and sbyte.
    b = np.array([-1, -2], np.int8)
    print(t.testvh(b))
    # UInt8 is Bool, therefore use Int16.
    b = np.array([211, 212], np.int16)
    print(t.testvh(b))
    print('>>>')
    res = t.testvh(np.array((0,)))
    print('<<<')
    print(res.shape)
    print(t.testvh({'shape': [2, 2], 'array': ['abcd', 'c', '12', 'x12']}))


if __name__ == '__main__':

    t = tConvert()
    test_na()
    test_main(t)
    testnps()
