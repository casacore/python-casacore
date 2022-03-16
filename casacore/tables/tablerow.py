# tablerow.py: Python tablerow functions
# Copyright (C) 2006
# Associated Universities, Inc. Washington DC, USA.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
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
# $Id: tablerow.py,v 1.6 2007/08/28 07:22:18 gvandiep Exp $

# Make interface to class TableRowProxy available.
from ._tables import TableRow

from .tablehelper import _check_key_slice


# A normal tablerow object keeps a reference to a table object to be able
# to know the actual number of rows.
# However, a mutual dependency is created when doing that for the tablerow
# object inside the table object.
# Therefore an intermediate _tablerow exists to be used in class table.

class _tablerow(TableRow):
    def __init__(self, table, columnnames, exclude=False):
        TableRow.__init__(self, table, columnnames, exclude)

    def iswritable(self):
        """Tell if all columns in the row object are writable."""
        return self._iswritable()

    def get(self, rownr):
        """Get the contents of the given row."""
        return self._get(rownr)

    def put(self, rownr, value, matchingfields=True):
        """Put the values into the given row.

        The value should be a dict (as returned by method :func:`get`.
        The names of the fields in the dict should match the names of the
        columns used in the `tablerow` object.

        `matchingfields=True` means that the value may contain more fields
        and only fields matching a column name will be used.

        """
        self._put(rownr, value, matchingfields)

    def _getitem(self, key, nrows):
        sei = _check_key_slice(key, nrows, 'tablerow')
        rownr = sei[0]
        if len(sei) == 1:
            return self.get(rownr)
        result = []
        inx = 0
        while inx < sei[1]:
            result.append(self.get(rownr))
            rownr += sei[2]
            inx += 1
        return result

    def _setitem(self, key, value, nrows):
        sei = _check_key_slice(key, nrows, 'tablerow')
        rownr = sei[0]
        if len(sei) == 1:
            return self.put(rownr, value)
        if isinstance(value, dict):
            # The same value is put in all rows.
            inx = 0
            while inx < sei[1]:
                self.put(rownr, value, True)
                rownr += sei[2]
                inx += 1
        else:
            # Each row has its own value.
            if len(value) != sei[1]:
                raise RuntimeError("tablerow slice length differs from value length")
            for val in value:
                self.put(rownr, val, True)
                rownr += sei[2]


class tablerow(_tablerow):
    """The Python interface to Casacore table rows.

    A table row is a record (dict) containing the values of a single row for
    one or more columns in a table. In constructing the `tablerow` object, one
    can specify which columns are to be included or excluded.
    By default all columns will be used, but if the table is writable,
    only writable columns will be used.

    A `tablerow` object can easily be constructed using :func:`table.row`.

    One or more rows can be read or written using the standard python indexing
    syntax where (negative) strides are possible.
    For example:

      t = table ('3c343.MS')
      tr = t.row (['ANTENNA1', 'ANTENNA2', 'ARRAY_ID'])
      tr[0]               # get row 0
      tr[:5]              # get row 0,1,2,3,4
      tr[-5,-1,]          # get last 4 rows
      tr[-1,-5,-1]        # get last 4 rows in reversed order
      tr[1] = tr[0]       # put values of row 0 into row 1

    Note that the last line will fail because the table is opened readonly.
    The argument `readonly=False` is needed in the table constructor to make
    it work.

    The `tablerow` class supports the context manager idiom (__enter__ and __exit__).
    When used in a `with` statement, the table changes will be flushed
    automatically, which is handy when writing to table rows.
    For example::

      with t.row() as tr:
        tr.put (1, tr.get(0))   # copy row 0 to row 1

    """

    def __init__(self, table, columnnames=[], exclude=False):
        _tablerow.__init__(self, table, columnnames, exclude)
        self._table = table

    def __enter__(self):
        """Function to enter a with block."""
        return self

    def __exit__(self, type, value, traceback):
        """Function to exit a with block which flushes the table object."""
        self._table.flush()

    def __len__(self):
        return self._table.nrows()

    def __getitem__(self, key):
        return self._getitem(key, self._table.nrows())

    def __setitem__(self, key, value):
        return self._setitem(key, value, self._table.nrows())
