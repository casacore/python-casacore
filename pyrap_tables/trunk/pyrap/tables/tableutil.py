# tableutil.py: Utility table functions
# Copyright (C) 2006
# Associated Universities, Inc. Washington DC, USA.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Library General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
# License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Correspondence concerning AIPS++ should be addressed as follows:
#        Internet email: aips2-request@nrao.edu.
#        Postal address: AIPS++ Project Office
#                        National Radio Astronomy Observatory
#                        520 Edgemont Road
#                        Charlottesville, VA 22903-2475 USA
#
# $Id: tableutil.py,v 1.6 2006/11/08 00:12:55 gvandiep Exp $

from table import table
from table import _remove_prefix


# Construct a table from an ASCII file.
def tablefromascii (tablename, asciifile,
                    headerfile='',
                    autoheader=False, autoshape=[],
                    columnnames=[], datatypes=[],
                    sep=' ',
                    commentmarker='',
                    firstline=1, lastline=-1,
                    readonly=True,
                    lockoptions='default', ack=True):
    import os.path
    filename = os.path.expandvars(asciifile);
    filename = os.path.expanduser(filename);
    if not os.path.exists(filename):
        s = "File '%s' not found" % (filename)
        raise IOError(s)
    if headerfile != '':
        filename = os.path.expandvars(headerfile);
        filename = os.path.expanduser(filename);
        if not os.path.exists(filename):
            s = "File '%s' not found" % (filename)
            raise IOError(s)
    tab = table(asciifile, headerfile, tablename, autoheader, autoshape,
                sep, commentmarker, firstline, lastline,
                columnnames, datatypes, _oper=1);
    print 'Input format: [' + tab._getasciiformat() +']';
    # Close table and reopen it in correct way.
    tab = '';
    return table(tablename, readonly=readonly, lockoptions=lockoptions,
                 ack=ack);


def tabledelete (tablename, checksubtables=False, ack=True):
    tabname = _remove_prefix(tablename);
    t = table(tabname, ack=False);
    if t.ismultiused(checksubtables):
        print 'Table', tabname, 'cannot be deleted; it is still in use';
    else:
        t = 0;
        table(tabname, readonly=False, _delete=True, ack=False);
        if ack:
            print 'Table', tabname, 'has been deleted';


# Convert Python value type to a glish-like type string
# as expected by the table code.
def value_type_name (value):
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, int):
        return 'integer'
    if isinstance(value, long):
        return 'integer'
    if isinstance(value, float):
        return 'double'
    if isinstance(value, complex):
        return 'dcomplex'
    if isinstance(value, str):
        return 'string'
    if isinstance(value, dict):
        return 'record'
    return 'unknown'

# Create a description of a scalar column
def tablecreatescalarcoldesc (columnname, value,
                              datamanagertype='', 
                              datamanagergroup='',
                              options=0, maxlen=0, comment='',
                              valuetype=''):
    vtype = valuetype
    if vtype == '':
        vtype = value_type_name(value)
    rec2 = {'valueType' : vtype,
            'dataManagerType' : datamanagertype,
            'dataManagerGroup' : datamanagergroup,
            'option' : options,
            'maxlen' : maxlen,
            'comment' : comment}
    return {'name' : columnname,
            'desc' : rec2}

# Create a description of an array column
def tablecreatearraycoldesc (columnname, value, ndim=0,
                             shape=[], datamanagertype='',
                             datamanagergroup='', 
                             options=0, maxlen=0, comment='',
                             valuetype=''):
    vtype = valuetype
    if vtype == '':
        vtype = value_type_name(value)
    if len(shape) > 0:
        if ndim <= 0:
            ndim = len(shape);
    rec2 = {'valueType' : vtype,
            'dataManagerType' : datamanagertype,
            'dataManagerGroup' : datamanagergroup,
            'ndim' : ndim,
            'shape' : shape,
            '_c_order' : True,
            'option' : options,
            'maxlen' : maxlen,
            'comment' : comment}
    return {'name' : columnname,
            'desc' : rec2}

# Create a table description from a set of column descriptions
def tablecreatedesc (descs=[]):
    rec = {}
    for desc in descs:
        colname = desc['name']
        if rec.has_key(colname):
            raise ValueError('Column name ' + name + ' multiply used in table description')
        rec[colname] = desc['desc']
    return rec;


# Define a hypercolumn in the table description.
def tabledefinehypercolumn (tabdesc,
                            name, ndim, datacolumns,
                            coordcolumns=False,
                            idcolumns=False):
    rec = {'HCndim' : ndim,
           'HCdatanames' : datacolumns}
    if not isinstance(coordcolumns, bool):
        rec['HCcoordnames'] = coordcolumns
    if not isinstance(idcolumns, bool):
        rec['HCidnames'] = idcolumns
    if not tabdesc.has_key('_define_hypercolumn_'):
        tabdesc['_define_hypercolumn_'] = {}
    tabdesc['_define_hypercolumn_'][name] = rec


# Does a table exist?
def tableexists(tablename):
    result = True
    try:
        t = table(tablename, ack=False)
    except:
        result = False
    return result

# Is a table writable?
def tableiswritable(tablename):
    result = True
    try:
        t = table(tablename, readonly=False, ack=False)
        result = t.iswritable()
    except:
        result = False
    return result

# Copy a table.
def tablecopy(tablename, newtablename, deep=False):
    t = table(tablename, ack=False)
    return t.copy (newtablename, deep=deep)

# Rename a table.
def tablerename(tablename, newtablename):
    t = table(tablename, ack=False)
    t.rename (newtablename)

# Get the table info.
def tableinfo(tablename):
    t = table(tablename, ack=False)
    return t.info()

# Show the table summary.
def tablesummary(tablename):
    t = table(tablename, ack=False)
    t.summary()
