import unittest
from pyrap.util import substitute


def f1(arg):
    a = 3
    s = substitute('subs as $a $arg', locals=locals())
    print(a, arg, s)


class TestUtil(unittest.TestCase):
    def test_util(self):
        a = 1
        b = 2
        p = "$((a+b)*(a+b))"
        s = substitute(p, locals=locals())
        print("a=%d, b=%d, %s => %s" % (a, b, p, s))
        f1(23)
        f1('xyz')

    def test_substitute(self):
        a = 2
        b = 3
        c = "xyz"
        d1 = True
        s1 = (1, 2, 3)
        s2 = ['ab', 'cde', 'f', 'ghij']

        self.assertTrue(substitute('$a $b $c $d1') == '2 3 "xyz" T')
        self.assertTrue(substitute('$(a) $(b) $(c) $(d1)') == '2 3 "xyz" T')
        self.assertTrue(substitute('$b $0 $a "$a" $b') == '3 $0 2 "$a" 3')
        self.assertTrue(substitute('$(a+b)') == '5')
        self.assertTrue(substitute('$((a+b)*(a+b))') == '25')
        self.assertTrue(substitute('$((a+b)*(a+c))') == '$((a+b)*(a+c))')
        self.assertTrue(substitute('"$(a+b)"') == '"$(a+b)"')
        self.assertTrue(substitute('\\$(a+b) \\\\$a \\$a') ==
                        '\\$(a+b) \\\\2 \\$a')

        self.assertTrue(substitute('$(a+b)+$a') == '5+2')
        self.assertTrue(substitute('$((a+b)+a)') == '7')
        self.assertTrue(substitute('$((a+b)*(a+b))') == '25')
        self.assertTrue(substitute('$(len("ab cd( de"))') == '9')
        self.assertTrue(substitute(
            ' $s1  $s2 ') == ' [1,2,3]  ["ab","cde","f","ghij"] ')
