# coding=utf-8
import numpy as np
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

    def test_numpy_unicode(self):
        table_path = join(self.workdir, 'blah.ms')
        col1 = makescacoldesc('mycol1', 'test', valuetype='string')
        col2 = makescacoldesc('mycol2', 'test', valuetype='string')
        t = table(table_path, maketabdesc([col1, col2]), ack=False)
        t.addrows(2)
        t.putcol('mycol1', np.array([unicode_string, unicode_string]))
        t.putcol('mycol2', [unicode_string, unicode_string])
        t.close()

        t = table(table_path)
        self.assertEqual(t.getcol('mycol1'), t.getcol('mycol2'))
