# coding=utf-8
import unittest
from casacore.tables import makescacoldesc, table, maketabdesc

unicode_string = u'«ταБЬℓσ»'


class TestUnicode(unittest.TestCase):
    def test_basic_unicode(self):
        c1 = makescacoldesc(unicode_string, 0)
        # t = table(unicode_string, maketabdesc((c1,)), ack=False)
        t = table(unicode_string)
