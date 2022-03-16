# tablecolumn.py: Python tablecolumn functions
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
# $Id: tablecolumn.py,v 1.9 2007/08/28 07:22:18 gvandiep Exp $

from .table import table
from .tablehelper import _check_key_slice, _do_remove_prefix, _format_cell

class tablecolumn:
    """The Python interface to a column in a Casacore table.

    The `tablecolumn` class is a convenience class to access data in a
    table column. All functionality provided in this class is available in
    :class:`table`, but `tablecolumn` is more convenient to use because the
    column name does not have to be given over and over again.

    For example::

      t = table('3C343.MS')
      tc = tablecolumn(t, 'DATA')
      # tc = t.col('DATA')           # another way to construct a tablecolumn
      tc.getcell(0)                  # get data from cell 0

    As can be seen in the example :func:`table.col` offers a slightly more
    convenient way to create a `tablecolumn` object.

    A `tablecolumn` can be indexed using Python's [] operator. Negative start,
    end, and stride is possible. For example::

      tc[0]               # get cell 0
      tc[:5]              # get cell 0,1,2,3,4
      tc[-5,-1,]          # get last 4 cells
      tc[-1,-5,-1]        # get last 4 cells in reversed order
      tc[1] = tr[0]       # put value of cell 0 into cell 1

    The `tablecolumn` class supports the context manager idiom (__enter__ and __exit__).
    When used in a `with` statement, the table changes will be flushed
    automatically, which is handy when writing to the table column.
    For example::

      with t.SPECTRAL_WINDOW_ID as tc:
        tc.putcell (0, 0)

    """

    def __init__(self, table, columnname):
        if columnname not in table.colnames():
            raise RuntimeError("Column " + columnname +
                               " does not exist in table " + table.name())
        self._table = table
        self._column = columnname

    def __enter__(self):
        """Function to enter a with block."""
        return self

    def __exit__(self, type, value, traceback):
        """Function to exit a with block which flushes the table object."""
        self._table.flush()

    def name(self):
        """Get the name of the column."""
        return self._column

    def table(self):
        """Get the table object this column belongs to."""
        return self._table

    def isscalar(self):
        """Tell if the column contains scalar values."""
        return self._table.isscalarcol(self._column)

    def isvar(self):
        """Tell if the column holds variable shaped arrays."""
        return self._table.isvarcol(self._column)

    def datatype(self):
        """Get the data type of the column.
        (see :func:`table.coldatatype`)"""
        return self._table.coldatatype(self._column)

    def arraytype(self):
        """Get the array type of a column holding arrays.
        (see :func:`table.colarraytype`)"""
        return self._table.colarraytype(self._column)

    def nrows(self):
        """Get number of cells in the column."""
        return self._table.nrows()

    def getshapestring(self, startrow=1, nrow=-1, rowincr=1):
        """Get the shapes of all cells in the column in string format.
        (see :func:`table.getcolshapestring`)"""
        return self._table.getcolshapestring(self._column,
                                             startrow, nrow, rowincr)

    def iscelldefined(self, rownr):
        """Tell if a column cell contains a value.
        (see :func:`table.iscelldefined`)"""
        return self._table.iscelldefined(self._column, rownr)

    def getcell(self, rownr):
        """Get data from a column cell.
        (see :func:`table.getcell`)"""
        return self._table.getcell(self._column, rownr)

    def getcellslice(self, rownr, blc, trc, inc=[]):
        """Get a slice from a column cell holding an array.
        (see :func:`table.getcellslice`)"""
        return self._table.getcellslice(self._column, rownr, blc, trc, inc)

    def getcol(self, startrow=0, nrow=-1, rowincr=1):
        """Get the contents of the column or part of it.
        (see :func:`table.getcol`)"""
        return self._table.getcol(self._column, startrow, nrow, rowincr)

    def getvarcol(self, startrow=0, nrow=-1, rowincr=1):
        """Get the contents of the column or part of it.
        (see :func:`table.getvarcol`)"""
        return self._table.getvarcol(self._column, startrow, nrow, rowincr)

    def getcolslice(self, blc, trc, inc=[], startrow=0, nrow=-1, rowincr=1):
        """Get a slice from a table column holding arrays.
        (see :func:`table.getcolslice`)"""
        return self._table.getcolslice(self._column, blc, trc, inc, startrow, nrow, rowincr)

    def putcell(self, rownr, value):
        """Put a value into one or more table cells.
        (see :func:`table.putcell`)"""
        return self._table.putcell(self._column, rownr, value)

    def putcellslice(self, rownr, value, blc, trc, inc=[]):
        """Put into a slice of a table cell holding an array.
        (see :func:`table.putcellslice`)"""
        return self._table.putcellslice(self._column, rownr, value, blc, trc, inc)

    def putcol(self, value, startrow=0, nrow=-1, rowincr=1):
        """Put an entire column or part of it.
        (see :func:`table.putcol`)"""
        return self._table.putcol(self._column, value, startrow, nrow, rowincr)

    def putvarcol(self, value, startrow=0, nrow=-1, rowincr=1):
        """Put an entire column or part of it.
        (see :func:`table.putvarcol`)"""
        return self._table.putvarcol(self._column, value, startrow, nrow, rowincr)

    def putcolslice(self, value, blc, trc, inc=[], startrow=0, nrow=-1, rowincr=1):
        """Put into a slice in a table column holding arrays.
        (see :func:`table.putcolslice`)"""
        return self._table.putcolslice(self._column, value, blc, trc, inc, startrow, nrow, rowincr)

    def keywordnames(self):
        """Get the names of all keywords of the column."""
        return self._table.colkeywordnames(self._column)

    def fieldnames(self, keyword=''):
        """Get the names of the fields in a column keyword value.
        (see :func:`table.colfieldnames`)"""
        return self._table.colfieldnames(self._column, keyword)

    def getkeyword(self, keyword):
        """Get the value of a column keyword.
        (see :func:`table.getcolkeyword`)"""
        return self._table.getcolkeyword(self._column, keyword)

    def getkeywords(self):
        """Get the value of all keywords of the column.
        (see :func:`table.getcolkeywords`)"""
        return self._table.getcolkeywords(self._column)

    def putkeyword(self, keyword, value, makesubrecord=False):
        """Put the value of a column keyword.
        (see :func:`table.putcolkeyword`)"""
        return self._table.putcolkeyword(self._column, keyword, value, makesubrecord)

    def putkeywords(self, value):
        """Put the value of multiple table keywords.
        (see :func:`table.putcolkeywords`)"""
        return self._table.putcolkeywords(self._column, value)

    def removekeyword(self, keyword):
        """Remove a column keyword.
        (see :func:`table.removecolkeyword`)"""
        return self._table.removecolkeyword(self._column, keyword)

    def getdesc(self):
        """Get the description of the column.
        (see :func:`table.getcoldesc`)"""
        return self._table.getcoldesc(self._column)

    def getdminfo(self):
        """Get data manager info of the column.
        (see :func:`table.getdminfo`)"""
        return self._table.getdminfo(self._column)

    def iter(self, order='', sort=True):
        """Return a :class:`tableiter` object on this column."""
        from casacore.tables import tableiter
        return tableiter(self._table, [self._column], order, sort)

    def index(self, sort=True):
        """Return a :class:`tableindex` object on this column."""
        from casacore.tables import tableindex
        return tableindex(self._table, [self._column], sort)

    def __len__(self):
        return self._table.nrows()

    def __getattr__(self, name):
        """Get the keyword value.

        | The value of a column keyword is returned if it names a keyword.
          If the keyword is a subtable, it opens the table and returns a
          table object.
        | The values of all column keywords is returned if name equals _ or keys.

        An AttributeError is raised if the name is not a keyword.

        For example::

          print tc.MEASINFO         # print the column's measure info
          print tc._                # print all column keywords

        """
        # Try if it is a keyword.
        try:
            val = self.getkeyword(name)
            # See if the keyword represents a subtable and try to open it.
            if val != _do_remove_prefix(val):
                try:
                    return table(val, ack=False)
                except:
                    pass
            return val
        except:
            pass
        # _ or keys means all keywords.
        if name in ('_', 'keys'):
            return self.getkeywords()
        # Unknown name.
        raise AttributeError("table has no attribute/keyword " + name)

    def __getitem__(self, key):
        """Get the values from one or more rows."""
        sei = _check_key_slice(key, self._table.nrows(), 'tablecolumn')
        if len(sei) == 1:
            # A single row.
            return self.getcell(sei[0])
        # Handle row by row and store values in a list.
        result = []
        rownr = sei[0]
        inx = 0
        while inx < sei[1]:
            result.append(self.getcell(rownr))
            rownr += sei[2]
            inx += 1
        return result

    def __setitem__(self, key, value):
        sei = _check_key_slice(key, self._table.nrows(), 'tablecolumn')
        if len(sei) == 1:
            # A single row.
            return self.putcell(sei[0], value)
        # Handle row by row.
        rownr = sei[0]
        inx = 0
        if not (isinstance(value, list) or isinstance(value, tuple)):
            # The same value is put in all rows.
            while inx < sei[1]:
                self.putcell(rownr, value)
                rownr += sei[2]
                inx += 1
        else:
            # Each row has its own value.
            if len(value) != sei[1]:
                raise RuntimeError(
                    "tablecolumn slice length differs from value length")
            for val in value:
                self.putcell(rownr, val)
                rownr += sei[2]
        return True

    def _repr_html_(self):
        """Give a nice representation of columns in notebooks."""
        out="<table class='taqltable'>\n"

        # Print column name (not if it is auto-generated)
        if not(self.name()[:4]=="Col_"):
            out+="<tr>"
            out+="<th><b>"+self.name()+"</b></th>"
            out+="</tr>"

        cropped=False
        rowcount=0
        colkeywords=self.getkeywords()
        for row in self:
            out +="\n<tr>"
            out += "<td>" + _format_cell(row, colkeywords) + "</td>\n"
            out += "</tr>\n"
            rowcount+=1
            out+="\n"
            if rowcount>=20:
                cropped=True
                break

        if out[-2:]=="\n\n":
            out=out[:-1]

        out+="</table>"

        if cropped:
            out+="<p style='text-align:center'>("+str(self.nrows()-20)+" more rows)</p>\n"

        return out

