import unittest2 as unittest
from pyrap.tables import *
import numpy

# Make some columns (5 scalars and an array)
c1 = makescacoldesc("coli", 0)
c2 = makescacoldesc("cold", 0.)
c3 = makescacoldesc("cols", "")
c4 = makescacoldesc("colb", True)
c5 = makescacoldesc("colc", 0. + 0j)
c6 = makearrcoldesc("colarr", 0.)


class TestTable(unittest.TestCase):

	#This decorator prepares the table to test with.
    def modifier(func):
        def modified(self):
            with table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5,
                       c6)), ack=False) as t:
                return func(self, t)
        return modified

    # Test table info
    @modifier
    def test_tableinfo(self, t):
        self.assertTrue(tableexists("ttable.py_tmp.tab1"))
        self.assertTrue(tableiswritable("ttable.py_tmp.tab1"))
        self.assertEqual(t.nrows(), 0)
        self.assertEqual(t.ncols(), 6)
        self.assertEqual(t.colnames(), ['cols', 'colc', 'coli', 'cold',
                                        'colb', 'colarr'])
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

    # ASCII table
    def test_tableascii(self):
        with table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5)),
                   ack=False) as t:
            tcol = t.colnames()
            t.addrows(5)
            t.toascii('asciitemp1', columnnames=tcol)
            tablefromascii(tablename='tablefromascii', asciifile='asciitemp1')
            ta = table("tablefromascii", readonly=False)
            tacol = ta.colnames()
            self.assertEqual(tcol, tacol)
        tabledelete('tablefromascii')
        tabledelete("ttable.py_tmp.tab1")

    # checking datatypes
    @modifier
    def test_check_datatypes(self, t):
        self.assertEqual(t.coldatatype("coli"), 'int')
        self.assertEqual(t.coldatatype("cold"), 'double')
        self.assertEqual(t.coldatatype("cols"), 'string')
        self.assertEqual(t.coldatatype("colb"), 'boolean')
        self.assertEqual(t.coldatatype("colc"), 'dcomplex')
        self.assertEqual(t.coldatatype("colarr"), 'double')

    # Add rows and put data
    @modifier
    def test_check_putdata(self, t):
        t.addrows(2)
        self.assertEqual(t.nrows(), 2)
        numpy.testing.assert_array_equal(t.getcol('coli'), numpy.array([0, 0]))
        t.putcol("coli", (1, 2))
        numpy.testing.assert_array_equal(t.getcol('coli'), numpy.array([1, 2]))
        numpy.testing.assert_array_equal(
            t.getcol('cold'), numpy.array([0., 0.]))
        t.putcol("cold", t.getcol('coli') + 3)
        numpy.testing.assert_array_equal(
            t.getcol('cold'), numpy.array([4., 5.]))
        t.removerows(1)
        self.assertEqual(t.nrows(), 1)

    # Add columns
    @modifier
    def test_addcolumns(self, t):
        t.addrows(2)
        cd1 = makecoldesc("col2", t.getcoldesc('coli'))
        t.addcols(cd1)
        self.assertEqual(t.ncols(), 7)
        self.assertIn('col2', t.colnames())
        t.renamecol("col2", "ncol2")
        self.assertNotIn('col2', t.colnames())
        self.assertIn('ncol2', t.colnames())

    # iter
    @modifier
    def test_iter(self, t):
        t.addrows(2)
        for iter_ in t.iter('coli', sort=False):
            print(iter_.getcol('coli'), iter_.rownumbers(t))

    # copy and rename
    @modifier
    def test_copyandrename(self, t):
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

    # Create a subset
    @modifier
    def test_subset(self, t):
        t1 = t.query('coli >0', sortlist='coli desc', columns='coli,cold')
        querycols = t1.colnames()
        t1 = taql('select coli,cold from $t where coli>0 order by coli desc')
        taqlcol = t1.colnames()
        self.assertEqual(querycols, taqlcol)
        t1.close()

    # Add some columns
    @modifier
    def test_adddmcolumns(self, t):
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
        t.putcell('colarrtsm', 0, numpy.array([[1, 2, 3], [4, 5, 6]]))
        t.putcell('colarrtsm', 1, t.getcell('colarrtsm', 0) + 10)
        self.assertEqual(t.getcell('colarrtsm', 0)[1, 2], 6)
        print(t.getvarcol('colarrtsm'))
        numpy.testing.assert_array_equal(t.getcellslice('colarrtsm', 0, [1, 1], [
                                         1, 2]), numpy.array([[5. + 0.j, 6. + 0.j]]))
        print(t.getvarcol('colarrtsm'))

    # Do keyword handling
    @modifier
    def test_keywords(self, t):
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
        #__getattr__
        tc = t.coli
        self.assertEqual(tc[0], 0)
        self.assertEqual(t.key1, 'keyval')
        self.assertRaises(AttributeError, lambda: t.key2)
        t.removekeyword('key1')
        self.assertNotIn('key1', t.getcolkeywords('coli'))

        # Print table row
        tr = t.row(['coli', 'cold'])
        self.assertEqual(tr[0]['coli'], 0)
        # Update a few fields in the row
        tr[0] = {'coli': 10, 'cold': 14}
        self.assertEqual(tr[0]['coli'], 10)

    # Some TaQL calculations
    @modifier
    def test_taqlcalc(self, t):
        t.addrows(2)
        numpy.testing.assert_array_almost_equal(
            t.calc("(1 km)cm"), numpy.array([100000.]))
        numpy.testing.assert_array_equal(t.calc("coli+1"), numpy.array([1, 1]))

    # Add some more data.
    @modifier
    def test_adddata(self, t):
        t.addrows(22)
        for i in range(2, 22):
            t.putcell('coli', i, i / 2)
        print(t[10])

    # Table column
    @modifier
    def test_tablecolumn(self, t):
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
            numpy.testing.assert_equal(tc.getvarcol()['r1'], 0)
            tc.putcell(2, 55)
            self.assertEqual(tc[2], 55)

    # Delete some columns.
    @modifier
    def test_deletecols(self, t):
        t.removecols(['colarr', 'cols', 'colb', 'colc'])
        self.assertNotIn(t.colnames())

    # table row
    @modifier
    def test_tablerow(self, t):
        t.addrows(20)
        with tablerow(t, 'colarr') as tr:
            self.assertEqual(len(tr), 20)
            print(tr[0])
            print(tr[:5])
            tr[1] = tr[0]
            tr[0] = {"key": "value"}
            self.assertTrue(tr.iswritable())

    # subtables
    @modifier
    def test_subtables(self, t):
        sub = table("sub", maketabdesc((c1, c2, c3)))
        t.putkeyword("subtablename", sub, makesubrecord=True)
        print(t.getsubtables())

    # Table index
    @modifier
    def test_tableindex(self, t):
        t.addrows(20)
        ti = t.index('coli')
        self.assertFalse(ti.isunique())
        self.assertIn('coli', ti.colnames())
        print(ti.rownrs(23))
        print(ti.rownrs(20))
        print(ti.rownrs(2))
        print(ti.rownrs(2, 7))                   # include borders
        print(ti.rownrs(2, 7, False, False))     # exclude borders

    def test_msutil(self):
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

        taql("SELECT FROM tabtemp where TIME in (SELECT DISTINCT TIME FROM tabtemp LIMIT 10) GIVING first10.MS AS PLAIN")
        taql("SELECT FROM tabtemp where TIME in (SELECT DISTINCT TIME FROM tabtemp LIMIT 10 OFFSET 10) GIVING second10.MS AS PLAIN")
        msconcat(["first10.MS", "second10.MS"], "combined.MS", concatTime=True)

        #TODO
        #msconcat with concatTime=False
        #msregularize
    def test_hypercolumn(self):
        scd1 = makescacoldesc("col2", "aa")
        scd2 = makescacoldesc("col1", 1, "IncrementalStMan")
        scd3 = makescacoldesc("colrec1", {})
        acd1 = makearrcoldesc("arr1", 1, 0, [2, 3, 4])
        acd2 = makearrcoldesc("arr2", 0. + 0j)
        td = maketabdesc([scd1, scd2, scd3, acd1, acd2])
        tabledefinehypercolumn(td, "TiledArray", 4, ["arr1"])
        tab = table("mytable", tabledesc=td, nrow=100)
        tab.done()

    def test_required_desc(self):
        #=============================================
        # TEST 1
        # Create a default Measurement Set
        #=============================================
        with default_ms("ttable.py_tmp.ms1") as ms1:
            pass

        #=============================================
        # TEST 2
        # Create a MS with a modified UVW column,
        # an additional MODEL_DATA column, as well as
        # specs for the column data managers
        #=============================================

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
                                         options=4, valuetype="complex",
                                         shape=[16, 4], ndim=2,
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

        #=============================================
        # TEST 3
        # Test subtable creation
        #=============================================
        subtables = ("ANTENNA", "DATA_DESCRIPTION", "DOPPLER",
                     "FEED", "FIELD", "FLAG_CMD", "FREQ_OFFSET",
                     "HISTORY", "OBSERVATION", "POINTING", "POLARIZATION",
                     "PROCESSOR", "SOURCE", "SPECTRAL_WINDOW", "STATE",
                     "SYSCAL", "WEATHER")

        for c in subtables:
            # Check that we can get the default description for this table
            def_subt_desc = required_ms_desc(c)

            # Don't use it though (too much to check).

            # Rather
            model_data_desc = makearrcoldesc("MODEL_DATA", 0.0,
                                             options=4,
                                             valuetype="complex", shape=[16, 4], ndim=2,
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
