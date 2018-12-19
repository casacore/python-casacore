# coding=utf-8
import unittest
from casacore.tables import table, maketabdesc, makescacoldesc
from tempfile import mkdtemp
from shutil import rmtree
from os.path import join

unicode_string = u'«ταБЬℓσ»'


class TestUnicode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workdir = mkdtemp()

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.workdir)

    def test_table_unicode(self):
        t = table(join(self.workdir, unicode_string), maketabdesc(), ack=False)

    def test_getcol(self):
        c1 = makescacoldesc(unicode_string, 0)
        t = table(join(self.workdir, 'ascii'), maketabdesc([c1]), ack=False)
        t.getcol(unicode_string)
