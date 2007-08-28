# tablecolumn.py: Python tablecolumn functions
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
# $Id: tablecolumn.py,v 1.9 2007/08/28 07:22:18 gvandiep Exp $

class tablecolumn:
    """
        The Python interface to AIPS++ table columns
    """

    def __init__(self, table, columnname):
        if not columnname in table.colnames():
            raise RuntimeError("Column " + columnname + " does not exist in table " + table.name());
        self._table  = table;
        self._column = columnname;

    def name (self):
        return self._column;

    def table (self):
        return self._table;

    def isscalar (self):
        return self._table.isscalarcol (self._column);

    def isvar (self):
        return self._table.isvarcol (self._column);

    def datatype (self):
        return self._table.coldatatype (self._column);

    def arraytype (self):
        return self._table.colarraytype (self._column);

    def nrows (self):
        return self._table.nrows();

    def getshapestring (self, startrow=1, nrow=-1, rowincr=1):
        return self._table.getcolshapestring (self._column, startrow, nrow, rowincr);

    def iscelldefined (self, rownr):
        return self._table.iscelldefined (self._column, rownr);

    def getcell (self, rownr):
        return self._table.getcell (self._column, rownr);

    def getcellslice (self, rownr, blc, trc, inc=[]):
        return self._table.getcellslice (self._column, rownr, blc, trc, inc);

    def getcol (self, startrow=0, nrow=-1, rowincr=1):
        return self._table.getcol (self._column, startrow, nrow, rowincr);

    def getvarcol (self, startrow=0, nrow=-1, rowincr=1):
        return self._table.getvarcol (self._column, startrow, nrow, rowincr);

    def getcolslice (self, blc, trc, inc=[], startrow=0, nrow=-1, rowincr=1):
        return self._table.getcolslice (self._column, blc, trc, inc, startrow, nrow, rowincr);

    def putcell (self, rownr, value):
        return self._table.putcell (self._column, rownr, value);

    def putcellslice (self, rownr, value, blc, trc, inc=[]):
        return self._table.putcellslice (self._column, rownr, value, blc, trc, inc);

    def putcol (self, value, startrow=0, nrow=-1, rowincr=1):
        return self._table.putcol (self._column, value, startrow, nrow, rowincr);

    def putvarcol (self, value, startrow=0, nrow=-1, rowincr=1):
        return self._table.putvarcol (self._column, value, startrow, nrow, rowincr);

    def putcolslice (self, value, blc, trc, inc=[], startrow=0, nrow=-1, rowincr=1):
        return self._table.putcolslice (self._column, value, blc, trc, inc, startrow, nrow, rowincr);

    def keywordnames (self):
        return self._table.colkeywordnames (self._column);

    def fieldnames (self, keyword=''):
        return  self._table.colfieldnames (self._column, keyword);

    def getkeyword (self, keyword):
        return  self._table.getcolkeyword (self._column, keyword);

    def getkeywords (self):
        return self._table.getcolkeywords (self._column);

    def putkeyword (self, keyword, value, makesubrecord=False):
        return self._table.putcolkeyword (self._column, keyword, value, makesubrecord);

    def putkeywords (self, value):
        return self._table.putcolkeywords (self._column, value);

    def removekeyword (self, keyword):
        return self._table.removecolkeyword (self._column, keyword);

    def getdesc (self):
        return self._table.getcoldesc (self._column);

    def iter (self, order='', sort=True):
        from tables import tableiter;
        return tableiter (self._table, [self._column], order, sort);

    def index (self, sort=True):
        from tables import tableindex;
        return tableindex (self._table, [self._column], sort);

    def __len__ (self):
        return self._table.nrows();

    def __getitem__ (self, key):
        sei = self.checkkey (key, self._table.nrows());
        if len(sei) == 1:
            # A single row.
            return self.getcell (sei[0]);
        # Handle row by row and store values in a list.
        result = [];
        rownr  = sei[0];
        inx    = 0;
        while inx < sei[1]:
            result.append (self.getcell (rownr));
            rownr += sei[2];
            inx   += 1;
        return result;

    def __setitem__ (self, key, value):
        sei = self.checkkey (key, self._table.nrows());
        if len(sei) == 1:
            # A single row.
            return self.putcell (sei[0], value);
        # Handle row by row.
        rownr = sei[0];
        inx   = 0;
        if not (isinstance(value,list) or isinstance(value,tuple)):
            # The same value is put in all rows.
            while inx < sei[1]:
                self.putcell (rownr, value);
                rownr += sei[2];
                inx   += 1;
        else:
            # Each row has its own value.
            if len(value) != sei[1]:
                raise RuntimeError("tablecolumn slice length differs from value length")
            for val in value:
                self.putcell (rownr, val);
                rownr += sei[2];
        return True;
        
    def checkkey (self, key, nrows):
        if not isinstance(key, slice):
            # A single index (possibly negative, thus from the end).
            if key < 0:
                key += nrows;
            if key < 0  or  key >= nrows:
                raise IndexError("tablecolumn index out of range");
            return [key];
        # Given as start:stop:step where each part is optional and can
        # be negative.
        incr = 1;
        if key.step != None:
            incr = key.step;
            if incr == 0:
                raise RunTimeError("tablecolumn slice step cannot be zero");
        strow  = 0;
        endrow = nrows;
        if incr < 0:
            strow  = nrows;
            endrow = 0;
        if key.start != None:
            strow = key.start;
            if strow < 0:
                strow += nrows;
            strow = min(max(strow,0), nrows);
        if key.stop != None:
            endrow = key.stop;
            if endrow < 0:
                endrow += nrows;
            endrow = min(max(endrow,0), nrows);
        if incr > 0:
            nrow = int((endrow - strow + incr - 1) / incr);
        else:
            nrow = int((strow - endrow - incr - 1) / -incr);
        nrow = max(0, nrow);
        return [strow,nrow,incr];
