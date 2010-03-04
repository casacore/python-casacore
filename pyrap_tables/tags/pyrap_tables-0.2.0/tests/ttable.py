#!/usr/bin/env python

from pyrap.tables import *
import numpy

# Make some columns (5 scalars and an array)
c1 = makescacoldesc ("coli", 0)
c2 = makescacoldesc ("cold", 0.)
c3 = makescacoldesc ("cols", "")
c4 = makescacoldesc ("colb", True)
c5 = makescacoldesc ("colc", 0.+0j)
c6 = makearrcoldesc ("colarr", 0.)
t = table ("ttable.py_tmp.tab1", maketabdesc((c1,c2,c3,c4,c5,c6)), ack=False)
# Print some info
print t.nrows()
print t.colnames()
print t.getkeywords()
print t.info()
t.addreadmeline ("test table run")
t.putinfo({'type':'test'})
print t.info()
# Add rows and put data
t.addrows (2)
print t.nrows()
t.putcol ("coli", (1,2))
t.putcol ("cold", t.getcol('coli')+3)
# Create a subset
t1 = t.query('coli == 3')
print len(t1)
t1 = taql('select coli,cold from $t where coli>0 order by coli desc')
print t1.colnames()
print t1.getcol('cold')
t1.close()

# Add some columns
# A scalar with the IncrementalStMan storage manager
t.addcols (maketabdesc(makescacoldesc("coli2",0)),
           dminfo={'TYPE':"IncrementalStMan", 'NAME':"ism1", 'SPEC':{}})
print t.colnames()
# An array with the StandardStMan
t.addcols (maketabdesc(makearrcoldesc("colarrssm","")))
# An array with the TiledShapeStMan
t.addcols (maketabdesc(makearrcoldesc("colarrtsm",0.+0j, ndim=2)),
           dminfo={'TYPE':"TiledShapeStMan", 'NAME':"tsm1", 'SPEC':{}})
print t.getdminfo()
coldmi = t.getdminfo('colarrtsm')
print t.getcoldesc('colarrtsm')
coldmi["NAME"] = 'tsm2'
t.addcols (maketabdesc(makearrcoldesc("colarrtsm2",0., ndim=2)), coldmi)
print t.getdminfo('colarrtsm2')
t.removecols('colarrtsm2')
# Write some data.
t.putcell('colarrtsm', 0, numpy.array([[1,2,3],[4,5,6]]))
t.putcell('colarrtsm', 1, t.getcell('colarrtsm',0)+10)
print t.getcol('colarrtsm')
print t.getcellslice('colarrtsm', 0, [1,1], [1,2])

# Do keyword handling
t.putkeyword ('key1', "keyval")
t.putkeyword ('keyrec', {'skey1':1, 'skey2': 3.})
print t.getkeywords()
print t.getkeyword('key1')
print t.keywordnames()
print t.fieldnames()
print t.fieldnames('keyrec')
print t.getcolkeywords('coli')

# Delete some columns.
t.removecols(['colarr','colarrssm','cols','colb','colc','coli2'])
print t.colnames()
# Print table row
tr = t.row(['coli','cold','colarrtsm'])
print tr[0]
# Update a few fields in the row
tr[0] = {'coli':10, 'cold':14}
# Rename a column
t.renamecol ('colarrtsm', 'colarr')
print t[0]

# Same TaQL calculations
print t.calc("(1 km)cm")
print t.calc("coli+1")

# Add some more data.
t.addrows(20);
for i in range(2,22):
    t.putcell ('coli', i, i/2)
# Table iteration
for iter in t.iter('coli'):
    print iter.getcol('coli'), iter.rownumbers(t)
# Table column
tc = tablecolumn(t,'coli');
tc[6] += 20
print tc[18:4:-2]
print tc[0:]
# Table index
ti = t.index('coli')
print ti.isunique(), ti.colnames()
print ti.rownrs(23)
print ti.rownrs(20)
print ti.rownrs(2)
print ti.rownrs(2,7)                   # include borders
print ti.rownrs(2,7,False,False)       # exclude borders
print ti[2:7]                          # exclude end
