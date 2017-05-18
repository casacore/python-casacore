import unittest2 as unittest
from pyrap.util import substitute


def f1(arg):
    a = 3
    s = substitute('subs as $a $arg', locals=locals())
    print(a, arg, s)


def f2():
    a=2
    b=3
    c="xyz"
    d1=True
    s1=(1,2,3)
    s2=['ab','cde','f','ghij']

    assert substitute ('$a $b $c $d1') == '2 3 "xyz" T'
    assert substitute ('$(a) $(b) $(c) $(d1)') == '2 3 "xyz" T'
    assert substitute ('$b $0 $a "$a" $b') == '3 $0 2 "$a" 3'
    assert substitute ('$(a+b)') == '5'
    assert substitute ('$((a+b)*(a+b))') == '25'
    assert substitute ('$((a+b)*(a+c))') == '$((a+b)*(a+c))'
    assert substitute ('"$(a+b)"') == '"$(a+b)"'
    assert substitute ('\\$(a+b) \\\\$a \\$a') == '\\$(a+b) \\\\2 \\$a'

    assert substitute('$(a+b)+$a') == '5+2'
    assert substitute('$((a+b)+a)') == '7'
    assert substitute('$((a+b)*(a+b))') == '25'
    assert substitute('$(len("ab cd( de"))') == '9'
    assert substitute(' $s1  $s2 ') == ' [1,2,3]  ["ab","cde","f","ghij"] '


class TestUtil(unittest.TestCase):
    def test_util(self):
        a = 1
        b = 2
        p = "$((a+b)*(a+b))"
        s = substitute(p, locals=locals())
        print("a=%d, b=%d, %s => %s" % (a, b, p, s))
        f1(23)
        f1('xyz')
        f2()
