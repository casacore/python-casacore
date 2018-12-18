# coding=utf-8
import unittest
from casacore.tables import table, maketabdesc
from tempfile import mkdtemp
from shutil import rmtree

unicode_string = u'«ταБЬℓσ»'


class TestUnicode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workdir = mkdtemp()

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.workdir)

    def test_table_unicode(self):
        t = table(unicode_string)

    def test_getcol(self):
        t = table('ascii', maketabdesc(), ack=False)
        t.getcol(unicode_string)
