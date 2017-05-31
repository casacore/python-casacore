import unittest2 as unittest
from pyrap.tables import *
import numpy


class TestTable(unittest.TestCase):
    def test_table(self):
        # Make some columns (5 scalars and an array)
        c1 = makescacoldesc("coli", 0)
        c2 = makescacoldesc("cold", 0.)
        c3 = makescacoldesc("cols", "")
        c4 = makescacoldesc("colb", True)
        c5 = makescacoldesc("colc", 0.+0j)
        c6 = makearrcoldesc("colarr", 0.)
        t = table("ttable.py_tmp.tab1", maketabdesc((c1, c2, c3, c4, c5, c6)),
                  ack=False)

        # Print some info
        print(t.nrows())
        print(t.colnames())
        print(t.getkeywords())
        print(t.info())
        t.addreadmeline("test table run")
        t.putinfo({'type': 'test'})
        print(t.info())

        # Add rows and put data
        t.addrows(2)
        print(t.nrows())
        t.putcol("coli", (1, 2))
        t.putcol("cold", t.getcol('coli')+3)

        # Create a subset
        t1 = t.query('coli == 3')
        print(len(t1))
        t1 = taql('select coli,cold from $t where coli>0 order by coli desc')
        print(t1.colnames())
        print(t1.getcol('cold'))
        t1.close()

        # Add some columns
        # A scalar with the IncrementalStMan storage manager
        t.addcols(maketabdesc(makescacoldesc("coli2", 0)),
                  dminfo={'TYPE': "IncrementalStMan", 'NAME': "ism1",
                          'SPEC': {}})
        print(t.colnames())

        # An array with the StandardStMan
        t.addcols(maketabdesc(makearrcoldesc("colarrssm", "")))

        # An array with the TiledShapeStMan
        t.addcols(maketabdesc(makearrcoldesc("colarrtsm", 0.+0j, ndim=2)),
                  dminfo={'TYPE': "TiledShapeStMan", 'NAME': "tsm1",
                          'SPEC': {}})
        print(t.getdminfo())
        coldmi = t.getdminfo('colarrtsm')
        print(t.getcoldesc('colarrtsm'))
        coldmi["NAME"] = 'tsm2'
        t.addcols(maketabdesc(makearrcoldesc("colarrtsm2", 0., ndim=2)), coldmi)
        print(t.getdminfo('colarrtsm2'))
        t.removecols('colarrtsm2')

        # Write some data.
        t.putcell('colarrtsm', 0, numpy.array([[1, 2, 3], [4, 5, 6]]))
        t.putcell('colarrtsm', 1, t.getcell('colarrtsm', 0) + 10)
        print(t.getcol('colarrtsm'))
        print(t.getcellslice('colarrtsm', 0, [1, 1], [1, 2]))

        # Do keyword handling
        t.putkeyword('key1', "keyval")
        t.putkeyword('keyrec', {'skey1': 1, 'skey2': 3.})
        print(t.getkeywords())
        print(t.getkeyword('key1'))
        print(t.keywordnames())
        print(t.fieldnames())
        print(t.fieldnames('keyrec'))
        print(t.getcolkeywords('coli'))

        # Delete some columns.
        t.removecols(['colarr', 'colarrssm', 'cols', 'colb', 'colc', 'coli2'])
        print(t.colnames())
        # Print table row
        tr = t.row(['coli', 'cold', 'colarrtsm'])
        print(tr[0])
        # Update a few fields in the row
        tr[0] = {'coli': 10, 'cold': 14}
        # Rename a column
        t.renamecol('colarrtsm', 'colarr')
        print(t[0])

        # Same TaQL calculations
        print(t.calc("(1 km)cm"))
        print(t.calc("coli+1"))

        # Add some more data.
        t.addrows(20)
        for i in range(2, 22):
            t.putcell('coli', i, i/2)

        # Table iteration
        for iter_ in t.iter('coli'):
            print(iter_.getcol('coli'), iter_.rownumbers(t))

        # Table column
        tc = tablecolumn(t, 'coli')
        tc[6] += 20
        print(tc[18:4:-2])
        print(tc[0:])

        # Table index
        ti = t.index('coli')
        print(ti.isunique(), ti.colnames())
        print(ti.rownrs(23))
        print(ti.rownrs(20))
        print(ti.rownrs(2))
        print(ti.rownrs(2, 7))                   # include borders
        print(ti.rownrs(2, 7, False, False))     # exclude borders
        print(ti[2:7])                           # exclude end

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
        dmgroup_spec = { "UVW" : { "DEFAULTTILESHAPE" : [3,128*64]}}

        # Create an array column description
        # as well as a data manager group spec
        model_data_desc = makearrcoldesc("MODEL_DATA", 0.0,
            options=4, valuetype="complex",
            shape=[16,4], ndim=2,
            datamanagertype="TiledColumnStMan",
            datamanagergroup="DataGroup")
        dmgroup_spec.update({
            "DataGroup" : {"DEFAULTTILESHAPE" : [4,16,32]} })

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
            self.assertTrue(np.all(dminfo["SPEC"]["DEFAULTTILESHAPE"] == [3, 128*64]))
            self.assertTrue(np.all(dminfo["SPEC"]["HYPERCUBES"]["*1"]["TileShape"] == [3,128*64]))

            self.assertTrue("MODEL_DATA" in ms2.colnames())

            # Check that MODEL_DATA was correctly constructed
            desc = ms2.getcoldesc("MODEL_DATA")
            self.assertTrue(desc["dataManagerType"] == "TiledColumnStMan")
            self.assertTrue(desc["dataManagerGroup"] == "DataGroup")
            self.assertTrue(desc["valueType"] == "complex")
            self.assertTrue(desc["ndim"] == 2)
            self.assertTrue(np.all(desc["shape"] == [16,4]))

            dminfo = ms2.getdminfo("MODEL_DATA")
            self.assertTrue(dminfo["NAME"] == "DataGroup")
            self.assertTrue(dminfo["TYPE"] == "TiledColumnStMan")
            self.assertTrue(np.all(dminfo["SPEC"]["DEFAULTTILESHAPE"] == [4,16,32]))
            self.assertTrue(np.all(dminfo["SPEC"]["HYPERCUBES"]["*1"]["TileShape"] == [4,16,32]))


        #=============================================
        # TEST 3
        # Test subtable creation
        #=============================================
        subtables = ("ANTENNA", "DATA_DESCRIPTION", "DOPPLER",
            "FEED", "FIELD", "FLAG_CMD",  "FREQ_OFFSET",
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
                valuetype="complex", shape=[16,4], ndim=2,
                datamanagertype="TiledColumnStMan",
                datamanagergroup="DataGroup")
            dmgroup_spec = {"DataGroup" : {"DEFAULTTILESHAPE" : [4,16,32]} }

            tabdesc = maketabdesc(model_data_desc)
            dminfo = makedminfo(tabdesc, dmgroup_spec)
            subtname = "ttable.py_tmp_subt_%s.ms" % c

            with default_ms_subtable(c, subtname, tabdesc, dminfo) as subt:
                self.assertTrue('MODEL_DATA' in subt.colnames())
                dminfo = subt.getdminfo("MODEL_DATA")
                self.assertTrue(dminfo["NAME"] == "DataGroup")
                self.assertTrue(dminfo["TYPE"] == "TiledColumnStMan")
                self.assertTrue(np.all(dminfo["SPEC"]["DEFAULTTILESHAPE"] == [4,16,32]))
                self.assertTrue(np.all(dminfo["SPEC"]["HYPERCUBES"]["*1"]["TileShape"] == [4,16,32]))
