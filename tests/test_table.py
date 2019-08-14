"""Tests for tables module."""
import unittest
from casacore.tables import (makescacoldesc, makearrcoldesc, table,
                             maketabdesc, tableexists, tableiswritable,
                             tableinfo, tablefromascii, tabledelete,
                             makecoldesc, msconcat, removeDerivedMSCal,
                             taql, tablerename, tablecopy, tablecolumn,
                             addDerivedMSCal, removeImagingColumns,
                             addImagingColumns, complete_ms_desc,
                             required_ms_desc, tabledefinehypercolumn,
                             default_ms, default_ms_subtable, makedminfo)
import numpy as np
import collections


subtables = ("ANTENNA", "DATA_DESCRIPTION", "DOPPLER",
             "FEED", "FIELD", "FLAG_CMD", "FREQ_OFFSET",
             "HISTORY", "OBSERVATION", "POINTING", "POLARIZATION",
             "PROCESSOR", "SOURCE", "SPECTRAL_WINDOW", "STATE",
             "SYSCAL", "WEATHER")


def compare(x, y):
    """Unordered list compare."""
    return collections.Counter(x) == collections.Counter(y)


class TestTable(unittest.TestCase):
    """Main TestTable class."""

    def test_tableinfo(self):
        """Test table info."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        self.assertTrue(tableexists("ttable.py_tmp.tab1"))
        self.assertTrue(tableiswritable("ttable.py_tmp.tab1"))
        self.assertEqual(t.nrows(), 0)
        self.assertEqual(t.ncols(), 6)
        self.assertTrue(compare(t.colnames(), ['cols', 'colc', 'coli',
                                               'cold', 'colb', 'colarr']))
        self.assertEqual(tableinfo("ttable.py_tmp.tab1"),
                         {'readme': '', 'subType': '', 'type': ''})
        t.addreadmeline("test table run")
        t.putinfo({'type': 'test', 'subType': 'test1'})

        self.assertEqual(t.info()['readme'], 'test table run\n')
        self.assertEqual(t.info()['subType'], 'test1')
        self.assertEqual(t.info()['type'], 'test')
        self.assertEqual(len(t), 0)
        print(str(t))
        self.assertEqual(t.endianformat(), 'little')
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_tableascii(self):
        """Testing ASCII table."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)

        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5)),
                  ack=False)
        tcol = t.colnames()
        t.addrows(5)
        t.toascii('asciitemp1', columnnames=tcol)
        tablefromascii(tablename='tablefromascii', asciifile='asciitemp1')
        ta = table("tablefromascii", readonly=False)
        tacol = ta.colnames()
        self.assertEqual(tcol, tacol)
        ta.close()
        t.close()
        tabledelete('tablefromascii')
        tabledelete("ttable.py_tmp.tab1")

    def test_check_datatypes(self):
        """Checking datatypes."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        self.assertEqual(t.coldatatype("coli"), 'int')
        self.assertEqual(t.coldatatype("cold"), 'double')
        self.assertEqual(t.coldatatype("cols"), 'string')
        self.assertEqual(t.coldatatype("colb"), 'boolean')
        self.assertEqual(t.coldatatype("colc"), 'dcomplex')
        self.assertEqual(t.coldatatype("colarr"), 'double')
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_check_putdata(self):
        """Add rows and put data."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                    c6)), ack=False)
        t.addrows(2)
        self.assertEqual(t.nrows(), 2)
        np.testing.assert_array_equal(t.getcol('coli'), np.array([0, 0]))
        t.putcol("coli", (1, 2))
        np.testing.assert_array_equal(t.getcol('coli'), np.array([1, 2]))
        np.testing.assert_array_equal(
            t.getcol('cold'), np.array([0., 0.]))
        t.putcol("cold", t.getcol('coli') + 3)
        np.testing.assert_array_equal(
            t.getcol('cold'), np.array([4., 5.]))
        t.removerows(1)
        self.assertEqual(t.nrows(), 1)
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_addcolumns(self):
        """Add columns."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t.addrows(2)
        cd1 = makecoldesc("col2", t.getcoldesc('coli'))
        t.addcols(cd1)
        self.assertEqual(t.ncols(), 7)
        self.assertIn('col2', t.colnames())
        t.renamecol("col2", "ncol2")
        self.assertNotIn('col2', t.colnames())
        self.assertIn('ncol2', t.colnames())
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_iter(self):
        """Testing tableiter."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t.addrows(2)
        for iter_ in t.iter('coli', sort=False):
            print(iter_.getcol('coli'), iter_.rownumbers(t))
        iter_.close()
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_copyandrename(self):
        """Copy and rename tables."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t_copy = tablecopy("ttable.py_tmp.tab1", "ttabel.tab1")
        self.assertEqual(t.name().split('/')[-1], 'ttable.py_tmp.tab1')
        self.assertEqual(t_copy.name().split('/')[-1], 'ttabel.tab1')
        numofrows = t.nrows()
        numofcols = t.ncols()
        self.assertEqual(t_copy.nrows(), numofrows)
        self.assertEqual(t_copy.ncols(), numofcols)
        tablerename("ttabel.tab1", "renamedttabel.tab1")
        self.assertEqual(t_copy.name().split('/')[-1], 'renamedttabel.tab1')
        t_copy.done()
        tabledelete("renamedttabel.tab1")
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_subset(self):
        """Create a subset."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t1 = t.query('coli >0', sortlist='coli desc', columns='coli,cold')
        querycols = t1.colnames()
        t1 = taql('select coli,cold from $t where coli>0 order by coli desc')
        taqlcol = t1.colnames()
        self.assertEqual(querycols, taqlcol)
        t1.close()
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_adddmcolumns(self):
        """Add some columns."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        # A scalar with the IncrementalStMan storage manager
        t.addcols(maketabdesc(makescacoldesc("coli2", 0)),
                  dminfo={'TYPE': "IncrementalStMan", 'NAME': "ism1",
                          'SPEC': {}})
        self.assertIn("coli2", t.colnames())

        # An array with the StandardStMan
        t.addcols(maketabdesc(makearrcoldesc("colarrssm", "")))
        self.assertIn("colarrssm", t.colnames())

        # An array with the TiledShapeStMan
        t.addcols(maketabdesc(makearrcoldesc("colarrtsm", 0. + 0j, ndim=2)),
                  dminfo={'TYPE': "TiledShapeStMan", 'NAME': "tsm1",
                          'SPEC': {}})
        self.assertIn("colarrtsm", t.colnames())
        print(t.getdminfo())
        coldmi = t.getdminfo('colarrtsm')
        print(t.getcoldesc('colarrtsm'))
        coldmi["NAME"] = 'tsm2'
        t.addcols(maketabdesc(makearrcoldesc(
            "colarrtsm2", 0., ndim=2)), coldmi)
        self.assertEqual(t.getdminfo('colarrtsm2')["NAME"], 'tsm2')
        t.removecols('colarrtsm2')

        # Write some data.
        t.addrows(22)
        t.putcell('colarrtsm', 0, np.array([[1, 2, 3], [4, 5, 6]]))
        t.putcell('colarrtsm', 1, t.getcell('colarrtsm', 0) + 10)
        self.assertEqual(t.getcell('colarrtsm', 0)[1, 2], 6)
        print(t.getvarcol('colarrtsm'))
        np.testing.assert_array_equal(t.getcellslice('colarrtsm', 0, [1, 1],
                                         [1, 2]),
                                         np.array([[5. + 0.j, 6. + 0.j]]))
        print(t.getvarcol('colarrtsm'))
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_keywords(self):
        """Do keyword handling."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t.addrows(2)
        t.putkeyword('key1', "keyval")
        t.putkeyword('keyrec', {'skey1': 1, 'skey2': 3.})
        self.assertTrue(t._["keyrec"]['skey1'], 1)
        self.assertEqual(t.getkeyword('key1'), 'keyval')
        self.assertIn('key1', t.keywordnames())
        self.assertIn('keyrec', t.keywordnames())
        key1 = t.keywordnames()
        key2 = t.fieldnames()
        self.assertEqual(key1, key2)
        self.assertIn('skey1', t.fieldnames('keyrec'))
        self.assertIn('skey2', t.fieldnames('keyrec'))
        t.putcolkeyword('coli', 'keycoli', {'colskey': 1, 'colskey2': 3.})
        self.assertEqual(t.getcolkeywords('coli')['keycoli']['colskey2'], 3)
        # getattr
        tc = t.coli
        self.assertEqual(tc[0], 0)
        self.assertEqual(t.key1, 'keyval')
        self.assertRaises(AttributeError, lambda: t.key2)
        t.removekeyword('key1')
        self.assertNotIn('key1', t.getcolkeywords('coli'))

        # Print table row
        # tr = t.row(['coli', 'cold')
        # self.assertEqual(tr[0]['coli'], 0)
        # # Update a few fields in the row
        # tr[0] = {'coli': 10, 'cold': 14}
        # self.assertEqual(tr[0]['coli'], 10)
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_taqlcalc(self):
        """Some TaQL calculations."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t.addrows(2)
        np.testing.assert_array_almost_equal(
            t.calc("(1 km)cm"), np.array([100000.]))
        np.testing.assert_array_equal(t.calc("coli+1"), np.array([1, 1]))
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_adddata(self):
        """Add some more data."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t.addrows(22)
        for i in range(2, 22):
            t.putcell('coli', i, i / 2)
        print(t[10])
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_tablecolumn(self):
        """Table column."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        t.addrows(20)
        with tablecolumn(t, 'coli') as tc:
            tc[6] += 20
            self.assertEqual(tc[6], 20)
            self.assertIn(20, tc[18:4:-2])
            self.assertEqual(tc[0:][6], 20)
            self.assertEqual(tc.datatype(), 'int')
            self.assertEqual(tc.name(), 'coli')
            print(tc.table())
            self.assertTrue(tc.isscalar())
            self.assertFalse(tc.isvar())
            self.assertEqual(tc.nrows(), 20)
            self.assertTrue(tc.iscelldefined(2))
            self.assertEqual(tc.getcell(3), 0)
            print(tc._)
            self.assertEqual(tc.getcol(2, 15)[4], 20)
            tc.putkeyword('key1', "keyval")
            self.assertIn('key1', tc.keywordnames())
            self.assertIn('key1', tc.fieldnames())
            self.assertEqual(tc.getdesc()['dataManagerType'], 'StandardStMan')
            self.assertEqual(tc.getdminfo()['TYPE'], 'StandardStMan')

            for iter_ in tc.iter(sort=False):
                print(iter_[0]['coli'])
            self.assertEqual(len(tc), 20)
            self.assertEqual(tc.getkeywords()['key1'], 'keyval')
            np.testing.assert_equal(tc.getvarcol()['r1'], 0)
            tc.putcell(2, 55)
            self.assertEqual(tc[2], 55)
            iter_.close()
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    def test_deletecols(self):
        """Delete some columns."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                     c6)), ack=False)
        a = ['colarr', 'cols', 'colb', 'colc']
        t.removecols(a)
        self.assertNotIn(a, t.colnames())
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    # def test_tablerow(self):
    #     """Testing table row."""
    #     c1 = makescacoldesc("coli", 0)
    #     c2 = makescacoldesc("cold", 0.)
    #     c3 = makescacoldesc("cols", "")
    #     c4 = makescacoldesc("colb", True)
    #     c5 = makescacoldesc("colc", 0. + 0j)
    #     c6 = makearrcoldesc("colarr", 0.)
    #     t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
    #                                                  c6)), ack=False)
    #     t.addrows(20)
    #     with tablerow(t, 'colarr') as tr:
    #         self.assertEqual(len(tr), 20)
    #         print(tr[0])
    #         print(tr[:5])
    #         tr[1] = tr[0]
    #         tr[0] = {"key": "value"}
    #         self.assertTrue(tr.iswritable())
    #     t.close()
    #     tabledelete("ttable.py_tmp.tab1")

    def test_subtables(self):
        """Testing subtables."""
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0. + 0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                                                    c6)), ack=False)
        sub = table("sub", maketabdesc((c1, c2, c3)))
        t.putkeyword("subtablename", sub, makesubrecord=True)
        print(t.getsubtables())
        t.close()
        tabledelete("ttable.py_tmp.tab1")

    # def test_tableindex(self):
    #     """Testing table index."""
    #     c1 = makescacoldesc("coli", 0)
    #     c2 = makescacoldesc("cold", 0.)
    #     c3 = makescacoldesc("cols", "")
    #     c4 = makescacoldesc("colb", True)
    #     c5 = makescacoldesc("colc", 0. + 0j)
    #     c6 = makearrcoldesc("colarr", 0.)
    #     t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
    #                                                  c6)), ack=False)
    #     t.addrows(20)
    #     ti = t.index('coli')
    #     self.assertFalse(ti.isunique())
    #     self.assertIn('coli', ti.colnames())
    #     print(ti.rownrs(23))
    #     print(ti.rownrs(20))
    #     print(ti.rownrs(2))
    #     print(ti.rownrs(2, 7))                   # include borders
    #     print(ti.rownrs(2, 7, False, False))     # exclude borders
    #     t.close()
    #     tabledelete("ttable.py_tmp.tab1")

    def test_msutil(self):
        """Testing msutil."""
        datacoldesc = makearrcoldesc("DATA", 0., ndim=2, shape=[20, 4])
        ms = default_ms("tabtemp", maketabdesc((datacoldesc)))
        ms.close()

        spw = table("tabtemp/SPECTRAL_WINDOW", readonly=False)
        spw.addrows()
        spw.putcell('NUM_CHAN', 0, 20)
        t = table("tabtemp", readonly=False)
        print(t.colnames())
        addImagingColumns("tabtemp")

        self.assertIn('MODEL_DATA', t.colnames())
        self.assertIn('CORRECTED_DATA', t.colnames())
        self.assertIn('IMAGING_WEIGHT', t.colnames())

        removeImagingColumns("tabtemp")

        self.assertNotIn('MODEL_DATA', t.colnames())
        self.assertNotIn('CORRECTED_DATA', t.colnames())
        self.assertNotIn('IMAGING_WEIGHT', t.colnames())

        addDerivedMSCal("tabtemp")

        self.assertIn('PA1', t.colnames())
        self.assertIn('PA2', t.colnames())
        self.assertIn('LAST', t.colnames())
        self.assertIn('AZEL2', t.colnames())
        self.assertIn('AZEL1', t.colnames())
        self.assertIn('UVW_J2000', t.colnames())
        self.assertIn('LAST1', t.colnames())
        self.assertIn('LAST2', t.colnames())
        self.assertIn('HA1', t.colnames())
        self.assertIn('HA2', t.colnames())
        self.assertIn('HA', t.colnames())

        removeDerivedMSCal("tabtemp")

        self.assertNotIn('PA1', t.colnames())
        self.assertNotIn('PA2', t.colnames())
        self.assertNotIn('LAST', t.colnames())
        self.assertNotIn('AZEL2', t.colnames())
        self.assertNotIn('AZEL1', t.colnames())
        self.assertNotIn('UVW_J2000', t.colnames())
        self.assertNotIn('LAST1', t.colnames())
        self.assertNotIn('LAST2', t.colnames())
        self.assertNotIn('HA1', t.colnames())
        self.assertNotIn('HA2', t.colnames())
        self.assertNotIn('HA', t.colnames())
        self.assertNotIn('HA', t.colnames())
        self.assertNotIn('HA', t.colnames())

        taql("SELECT FROM tabtemp where TIME in (SELECT DISTINCT TIME" +
             " FROM tabtemp LIMIT 10) GIVING first10.MS AS PLAIN")
        taql("SELECT FROM tabtemp where TIME in (SELECT DISTINCT TIME" +
             " FROM tabtemp LIMIT 10 OFFSET 10) GIVING second10.MS AS PLAIN")
        msconcat(["first10.MS", "second10.MS"], "combined.MS", concatTime=True)
        spw.close()
        t.close()
        tabledelete("tabtemp")

        # TODO
        # msconcat with concatTime=False
        # msregularize
    def test_hypercolumn(self):
        """Test hypercolumns."""
        scd1 = makescacoldesc("col2", "aa")
        scd2 = makescacoldesc("col1", 1, "IncrementalStMan")
        scd3 = makescacoldesc("colrec1", {})
        acd1 = makearrcoldesc("arr1", 1, 0, [2, 3, 4])
        acd2 = makearrcoldesc("arr2", 0. + 0j)
        td = maketabdesc([scd1, scd2, scd3, acd1, acd2])
        tabledefinehypercolumn(td, "TiledArray", 4, ["arr1"])
        tab = table("mytable", tabledesc=td, nrow=100)
        tab.done()
        tabledelete("mytable")

    def test_complete_desc(self):
        """ Test complete table descriptions """
        for i, name in enumerate(("MAIN",) + subtables):
            desc = complete_ms_desc(name)
            assert isinstance(desc, dict)
            assert len(desc) > 0

            with table("complete_desc_table_%s-%d.table" % (name, i),
                       desc, ack=False, readonly=False) as T:
                T.addrows(10)

    def test_required_desc(self):
        """Testing required_desc."""
        # =============================================
        # TEST 1
        # Create a default Measurement Set
        # =============================================
        with default_ms("ttable.py_tmp.ms1") as ms1:
            pass

        # =============================================
        # TEST 2
        # Create a MS with a modified UVW column,
        # an additional MODEL_DATA column, as well as
        # specs for the column data managers
        # =============================================

        # Get the required description for an MS
        ms2_desc = required_ms_desc("MAIN")

        # Modify UVW to use a Tiled Column Storage Manager
        ms2_desc["UVW"].update(options=0,
                               shape=[3], ndim=1,
                               dataManagerGroup="UVW",
                               dataManagerType='TiledColumnStMan')
        dmgroup_spec = {"UVW": {"DEFAULTTILESHAPE": [3, 128 * 64]}}

        # Create an array column description
        # as well as a data manager group spec
        model_data_desc = makearrcoldesc("MODEL_DATA", 0.0,
                                         options=4,
                                         valuetype="complex",
                                         shape=[16, 4],
                                         ndim=2,
                                         datamanagertype="TiledColumnStMan",
                                         datamanagergroup="DataGroup")
        dmgroup_spec.update({
            "DataGroup": {"DEFAULTTILESHAPE": [4, 16, 32]}})

        # Incorporate column into table description
        ms2_desc.update(maketabdesc(model_data_desc))

        # Construct a data manager info from the table description
        # and the data manager group spec
        ms2_dminfo = makedminfo(ms2_desc, dmgroup_spec)

        # Create measurement set with table description
        # and data manager info
        with default_ms("ttable.py_tmp.ms2", ms2_desc, ms2_dminfo) as ms2:

            # Check that UVW was correctly constructed
            desc = ms2.getcoldesc("UVW")
            self.assertTrue(desc["dataManagerType"] == "TiledColumnStMan")
            self.assertTrue(desc["dataManagerGroup"] == "UVW")
            self.assertTrue(desc["valueType"] == "double")
            self.assertTrue(desc["ndim"] == 1)
            self.assertTrue(np.all(desc["shape"] == [3]))

            dminfo = ms2.getdminfo("UVW")
            self.assertTrue(dminfo["NAME"] == "UVW")
            self.assertTrue(dminfo["TYPE"] == "TiledColumnStMan")
            self.assertTrue(
                np.all(dminfo["SPEC"]["DEFAULTTILESHAPE"] == [3, 128 * 64]))
            self.assertTrue(np.all(dminfo["SPEC"]["HYPERCUBES"][
                            "*1"]["TileShape"] == [3, 128 * 64]))

            self.assertTrue("MODEL_DATA" in ms2.colnames())

            # Check that MODEL_DATA was correctly constructed
            desc = ms2.getcoldesc("MODEL_DATA")
            self.assertTrue(desc["dataManagerType"] == "TiledColumnStMan")
            self.assertTrue(desc["dataManagerGroup"] == "DataGroup")
            self.assertTrue(desc["valueType"] == "complex")
            self.assertTrue(desc["ndim"] == 2)
            self.assertTrue(np.all(desc["shape"] == [16, 4]))

            dminfo = ms2.getdminfo("MODEL_DATA")
            self.assertTrue(dminfo["NAME"] == "DataGroup")
            self.assertTrue(dminfo["TYPE"] == "TiledColumnStMan")
            self.assertTrue(
                np.all(dminfo["SPEC"]["DEFAULTTILESHAPE"] == [4, 16, 32]))
            self.assertTrue(np.all(dminfo["SPEC"]["HYPERCUBES"][
                            "*1"]["TileShape"] == [4, 16, 32]))

        # =============================================
        # TEST 3
        # Test subtable creation
        # =============================================

        for c in subtables:
            # Check that we can get the default description for this table
            def_subt_desc = required_ms_desc(c)

            # Don't use it though (too much to check).

            # Rather
            model_data_desc = makearrcoldesc(
                                    "MODEL_DATA", 0.0,
                                    options=4,
                                    valuetype="complex",
                                    shape=[16, 4],
                                    ndim=2,
                                    datamanagertype="TiledColumnStMan",
                                    datamanagergroup="DataGroup")
            dmgroup_spec = {"DataGroup": {"DEFAULTTILESHAPE": [4, 16, 32]}}

            tabdesc = maketabdesc(model_data_desc)
            dminfo = makedminfo(tabdesc, dmgroup_spec)
            subtname = "ttable.py_tmp_subt_%s.ms" % c

            with default_ms_subtable(c, subtname, tabdesc, dminfo) as subt:
                self.assertTrue('MODEL_DATA' in subt.colnames())
                dminfo = subt.getdminfo("MODEL_DATA")
                self.assertTrue(dminfo["NAME"] == "DataGroup")
                self.assertTrue(dminfo["TYPE"] == "TiledColumnStMan")
                self.assertTrue(
                    np.all(dminfo["SPEC"]["DEFAULTTILESHAPE"] == [4, 16, 32]))
                self.assertTrue(np.all(dminfo["SPEC"]["HYPERCUBES"][
                                "*1"]["TileShape"] == [4, 16, 32]))
