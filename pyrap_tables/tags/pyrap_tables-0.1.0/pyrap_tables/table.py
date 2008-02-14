# table.py: Python table functions
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
# $Id: table.py,v 1.13 2006/11/10 01:18:53 gvandiep Exp $

# Make interface to class TableProxy available.
from _tables import Table

# A keywordset in a table can hold tables, but it is not possible to
# pass them around because a ValueHolder cannot deal with it.
# Therefore it is passed around as a string with a special prefix.
def _add_prefix (name):
    return 'Table: ' + name;

def _do_remove_prefix (name):
    res = name;
    if isinstance(res, str):
        if (res.find ('Table: ') == 0):
            res = res.replace ('Table: ', '', 1);
    return res;

def _remove_prefix (name):
    if isinstance(name, str):
        return _do_remove_prefix (name)
    return [_do_remove_prefix(nm) for nm in name]


# Execute a TaQL command on a table.
def tablecommand (command, style='Python', tables=[]):
    cmd = command;
    if style:
        cmd = 'using style ' + style + ' ' + command;
    tab = table(cmd, tables, _oper=2);
    result = tab._getcalcresult();
    # If result is empty, it was a normal TaQL command resulting in a table.
    # Otherwise it is a record containing calc values.
    if len(result) == 0:
        return tab;
    return result['values'];
def taql (command, style='Python', tables=[]):
    return tablecommand (command, style, tables);


class table(Table):
    """
        The Python interface to AIPS++ tables
    """

    def __init__(self, tablename, tabledesc=False, nrow=0, readonly=True,
                 lockoptions='default', ack=True, dminfo={}, endian='aipsrc',
                 memorytable=False, columnnames=[], datatypes=[],
                 _oper=0, _delete=False, concatsubtables=[]):
        if _oper == 1:
            # This is the readascii constructor.
            tabname = _remove_prefix(tablename);
            Table.__init__ (self, tabname, tabledesc, nrow, readonly,
                            lockoptions, ack, dminfo, endian, memorytable,
                            columnnames, datatypes);
        elif _oper == 2:
            # This is the query constructor.
            Table.__init__ (self, tablename, tabledesc);
        elif _oper == 3:
            # This is the constructor taking a Table (used by copy).
            Table.__init__ (self, tablename);
        else:
            # This is the constructor for a normal table open.
            # It can be done in several forms:
            #  - open single existing table (PlainTable)
            #  - open multiple existing tables (ConcatTable)
            #  - create a new table (PlainTable or MemoryTable)
            #  - concatenate open tables (ConcatTable)
            tabname = _remove_prefix(tablename);
            lockopt = lockoptions;
            if isinstance(lockoptions, str):
                lockopt = {'option' : lockoptions};
            if isinstance(tabledesc, dict):
                # Create a new table.
                memtype = 'plain';
                if (memorytable):
                    memtype = 'memory';
                Table.__init__ (self, tabname, lockopt, endian,
                                    memtype, nrow, tabledesc, dminfo);
                if ack:
                    print 'Successful creation of', lockopt['option']+'-locked table', tabname+':', self.ncols(), 'columns,', self.nrows(), 'rows';
            else:
                # Deal with existing tables.
                if not tabname:
                    raise ValueError("No tables or names given")
                # Open an existing table
                opt=1
                typstr = 'readonly';
                if not readonly:
                    typstr = 'read/write';
                    opt = 5;
                    if _delete:
                        opt = 6;
                if isinstance(tabname,str):
                    Table.__init__ (self, tabname, lockopt, opt);
                    if ack:
                        print 'Successful', typstr, 'open of', lockopt['option']+'-locked table', tabname+':', self.ncols(), 'columns,', self.nrows(), 'rows';
                elif isinstance(tabname[0],str):
                    # Concatenate and open named tables.
                    Table.__init__ (self, tabname, concatsubtables, lockopt, opt)
                    if ack:
                        print 'Successful', typstr, 'open of', lockopt['option']+'-locked concatenated tables', tabname,':', self.ncols(), 'columns,', self.nrows(), 'rows';
                else:
                    # Concatenate already open tables.
                    Table.__init__ (self, tabname, concatsubtables, 0, 0, 0)
                    if ack:
                        print 'Successful virtual concatenation of', len(tabname), 'tables:', self.ncols(), 'columns,', self.nrows(), 'rows';
        # Create a row object for this table.
        from tablerow import _tablerow;
        self._row = _tablerow (self, self.colnames());

    def __str__ (self):
        return _add_prefix (self.name());
    
    def __len__ (self):
        return self.nrows();

    def __getitem__ (self, key):
        return self._row._getitem (key, self.nrows());

    def __setitem__ (self, key, value):
        self._row._setitem (key, value, self.nrows());

    def copy (self, newtablename, deep=False, valuecopy=False, dminfo={},
              endian='aipsrc', memorytable=False, copynorows=False):
        t = self._copy (newtablename, memorytable, deep, valuecopy,
                        endian, dminfo, copynorows);
        # copy returns a Table object, so turn that into table.
        return table(t, _oper=3);
    
    def selectrows (self, rownrs):
        t = self._selectrows (rownrs, name='');
        # selectrows returns a Table object, so turn that into table.
        return table(t, _oper=3);

    def col (self, columnname):
        from tables import tablecolumn;
        return tablecolumn (self, columnname);

    def row (self, columnnames, exclude=False):
        return tablerow (self, columnnames, exclude);

    def iter (self, columnnames, order='', sort=True):
        from tables import tableiter;
        return tableiter (self, columnnames, order, sort);

    def index (self, columnnames, sort=True):
        from tables import tableindex;
        return tableindex (self, columnnames, sort);

    def isvarcol (self, columnname):
        desc = self.getcoldesc(columnname);
        return desc.has_key('ndim') and not desc.has_key('shape');

    def putcell (self, columnname, rownr, value):
        return self._putcell (columnname, rownr, value);

    def getcellslice (self, columnname, rownr, blc, trc, inc=[]):
        return self._getcellslice (columnname, rownr,
                                   blc, trc, inc);

    def getcolslice (self, columnname, blc, trc, inc=[],
                     startrow=0, nrow=-1, rowincr=1):
        return self._getcolslice (columnname, blc, trc, inc,
                                  startrow, nrow, rowincr);

    def putcellslice (self, columnname, rownr, value, blc, trc, inc=[]):
        return self._putcellslice (columnname, rownr, value,
                                   blc, trc, inc);

    def putcolslice (self, columnname, value, blc, trc, inc=[],
                     startrow=0, nrow=-1, rowincr=1):
        return self._putcolslice (columnname, value, blc, trc, inc,
                                  startrow, nrow, rowincr);

    def putcol (self, columnname, value, startrow=0, nrow=-1, rowincr=1):
        return self._putcol (columnname, startrow, nrow, rowincr, value);

    def putvarcol (self, columnname, value, startrow=0, nrow=-1, rowincr=1):
        return self._putvarcol (columnname, startrow, nrow, rowincr, value);

    def getcolshapestring (self, columnname,
                           startrow=0, nrow=-1, rowincr=1):
        return self._getcolshapestring (columnname,
                                        startrow, nrow, rowincr,
                                        True);              #reverse axes

    def keywordnames (self):
        return self._getfieldnames ('', '', -1);

    def colkeywordnames (self, columnname):
        return self._getfieldnames (columnname, '', -1);

    def fieldnames (self, keyword=''):
        if isinstance(keyword, str):
            return self._getfieldnames ('', keyword, -1);
        else:
            return self._getfieldnames ('', '', keyword);

    def colfieldnames (self, columnname, keyword=''):
        if isinstance(keyword, str):
            return self._getfieldnames (columnname, keyword, -1);
        else:
            return self._getfieldnames (columnname, '', keyword);

    def getkeyword (self, keyword):
        if isinstance(keyword, str):
            return self._getkeyword ('', keyword, -1);
        else:
            return self._getkeyword ('', '', keyword);

    def getcolkeyword (self, columnname, keyword):
        if isinstance(keyword, str):
            return self._getkeyword (columnname, keyword, -1);
        else:
            return self._getkeyword (columnname, '', keyword);

    def getkeywords (self):
        return self._getkeywords ('');

    def getcolkeywords (self, columnname):
        return self._getkeywords (columnname);

    def putkeyword (self, keyword, value, makesubrecord=False):
        val = value;
        if isinstance(val, table):
            val = _add_prefix (val.name());
        if isinstance(keyword, str):
            return self._putkeyword ('', keyword, -1, val, makesubrecord);
        else:
            return self._putkeyword ('', '', keyword, val, makesubrecord);

    def putcolkeyword (self, columnname, keyword, value, makesubrecord=False):
        if isinstance(value, table):
            value = 'Table:' + value.name;
        if isinstance(keyword, str):
            return self._putkeyword (columnname, keyword, -1,
                                      value, makesubrecord);
        else:
            return self._putkeyword (columnname, '', keyword,
                                      value, makesubrecord);

    def putkeywords (self, value):
        return self._putkeywords ('', value);

    def putcolkeywords (self, columnname, value):
        return self._putkeywords (columnname, value);

    def removekeyword (self, keyword):
        if isinstance(keyword, str):
            self._removekeyword ('', keyword, -1);
        else:
            self._removekeyword ('', '', keyword);

    def removecolkeyword (self, columnname, keyword):
        if isinstance(keyword, str):
            self._removekeyword (columnname, keyword, -1);
        else:
            self._removekeyword (columnname, '', keyword);


    def summary (self, recurse=False):
        print 'Table summary:', self.name();
        print 'Shape:', self.ncols(), 'columns by', self.nrows(), 'rows';
        print 'Info:', self.info();
        tkeys = self.getkeywords();
        if (len(tkeys) > 0):
            print 'Table keywords:', tkeys;
        columns = self.colnames();
        if (len(columns) > 0):
            print 'Columns:', columns;
            for column in columns:
                ckeys = self.getcolkeywords(column);
                if (len(ckeys) > 0):
                    print column, 'keywords:', ckeys;
        if (recurse):
            for key in tkeys.keys():
                value = tkeys[key];
                tabname = _remove_prefix (value);
                print 'Summarizing subtable:', tabname;
                lt = table(tabname);
                if (not lt.summary(recurse)):
                    break;
        return True;

    def query (self, query='', name='', sortlist='', columns='',
               style='Python'):
        if not query and not sortlist and not columns:
            raise ValueError('No selection done (arguments query, sortlist, and columns are empty)');
        command = 'select ';
        if columns:
            command += columns;
        command += ' from $1';
        if query:
            command += ' where ' + query;
        if sortlist:
               command += ' orderby ' + sortlist;
        if name:
            command += ' giving ' + name;
        return tablecommand(command, style, [self]);

    def calc (self, expr, style='Python'):
        return tablecommand('calc from $1 calc ' + expr, style, [self]);
                            
    def browse (self):
        try:
            import wxPython
        except ImportError:
            print 'wx not available'
            return
        from wxPython.wx import wxPySimpleApp
        import sys
        app = wxPySimpleApp()
        from wxtablebrowser import CasaTestFrame
        frame = CasaTestFrame(None, sys.stdout, self)
        frame.Show(True)
        app.MainLoop()
