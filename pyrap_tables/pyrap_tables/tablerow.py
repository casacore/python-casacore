# tablerow.py: Python tablerow functions
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
# $Id: tablerow.py,v 1.5 2006/11/08 00:12:55 gvandiep Exp $

# Make interface to class TableRowProxy available.
from _tables import TableRow

# A normal tablerow object keeps a reference to a table object to be able
# to know the actual number of rows.
# However, a mutual dependency is created when doing that for the tablerow
# object inside the table object.
# Therefore an intermediate _tablerow exists to be used in table.

class _tablerow(TableRow):
    def __init__(self, table, columnnames, exclude=False):
        TableRow.__init__ (self, table, columnnames, exclude);

    def _getitem (self, key, nrows):
        if not isinstance(key, slice):
            if key >= nrows:
                raise IndexError("tablerow key past end-of-table");
            return self.get (key);
        incr = 1;
        if key.step != None:
            incr = key.step;
        strow=0;
        if key.start != None:
            strow = key.start;
        endrow = nrows;
        if key.stop != None:
            endrow = min(endrow, key.stop);
        if incr <= 0  or  strow >= endrow:
            raise RuntimeError("tablerow slice start must be < stop and < nrows");
        result = [];
        while strow < endrow:
            result.append (self.get (strow));
            strow += incr;
        return result;
    
    def _setitem (self, key, value, nrows):
        if not isinstance(key, slice):
            if key >= nrows:
                raise IndexError("tablerow key past end-of-table");
            return self.put (key, value);
        incr = 1;
        if key.step != None:
            incr = key.step;
        strow=0;
        if key.start != None:
            strow = key.start;
        endrow = nrows;
        if key.stop != None:
            endrow = min(endrow, key.stop);
        if incr <= 0  or  strow >= endrow:
            raise RuntimeError("tablerow slice start must be < stop and < nrows");
        nrow = (endrow - strow + incr - 1) / incr;
        if isinstance(value, dict):
            # The same value is put in all rows.
            while strow < endrow:
                self.put (strow, value, True);
                strow += incr;
        else:
            # Each row has its own value.
            if len(value) != nrow:
                raise RuntimeError("tablerow slice length differs from value length")
            for val in value:
                self.put (strow, val, True);
                strow += incr;



class tablerow(_tablerow):
    """
        The Python interface to AIPS++ table rows
    """

    def __init__(self, table, columnnames, exclude=False):
        _tablerow.__init__ (self, table, columnnames, exclude);
        self._table = table;

    def __len__ (self):
        return self._table.nrows();

    def __getitem__ (self, key):
        return self._getitem (key, self._table.nrows());

    def __setitem__ (self, key, value):
        return self._setitem (key, value, self._table.nrows());
