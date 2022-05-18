# tableindex.py: Python tableindex functions
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
# $Id: tableindex.py,v 1.6 2006/11/08 00:12:55 gvandiep Exp $

# Make interface to class TableIndexProxy available.
from ._tables import TableIndex


class tableindex(TableIndex):
    """The Python interface to Casacore table index.

    A tableindex makes it possible to find rows in a :class:`table` based on
    the contents of one or more columns. When constructing the `tableindex` it
    has to be specified for which column or columns an index has to be built.
    Those columns will be loaded in memory and thereafter row numbers can be
    found in a fast way using a binary search.

    Using a table index is only useful if many searches will be done in the
    table. For a single or few searches it is better to query the table using
    method :func:`table.query`.

    Normally an index will be build on one or more scalar columns (e.g.
    on ANTENNA1 and ANTENNA2 in a measurementset table). However, it is also
    possible to buo.d an index for a column containing arrays (e.g. for a
    column where each cell can contain multiple names. In that case only a
    single column can be indexed.

    The index can be unique, but does not need to be.
    A unique index can be asked for the row number containing a given key.
    A non-unique index can only be asked for the row numbers containing a key.
    The returned sequence can thereafter be used in :func:`table.selectrows`
    to form that subset of the table.

    `tableindex` supports Python's index operator [] as explained in the
    methods :func:`rownr` and :func:`rownrs`.

    """

    def __init__(self, table, columnnames, sort=True):
        TableIndex.__init__(self, table, columnnames, not sort)

    """Create the index on one or more columns.

    By default the columns get sorted when forming in the index. By giving
    `sort=False` this can be omitted in case the table is already in the
    correct order.

    Method :func:`table.index` is a somewhat easier way to create a
    `tableindex` object.

    """

    # Turn a key into a dict if needed.
    def _makekey(self, key):
        d = key
        if not isinstance(d, dict):
            cols = self.colnames()
            if len(cols) != 1:
                raise RuntimeError("key has to be given as a dict for a multi-column index")
            d = {cols[0]: key}
        return d

    def rownr(self, key):
        """Get the unique row number containing the key.

        If the index is made from a single column, the keycan be given as a
        single value.
        Otherwise the key has to be given as a dict where the name of each
        field in the dict should correspond with the column name in the index.

        For example::

          t = table('3c343.MS/ANTENNA')
          tinx = t.index ('NAME')        # build index for antenna name
          rownr = tinx.rownr('RTE')      # find an antenna by name
          rownr = tinx['RTE']            # same as above
          t.getcell ('POSITION', rownr)  # get position of that antenna

        As shown in the example above the python index operator can also
        be used to find a row number if the index if made of a single column.

        An exception will be raised if the index is not unique. In that case
        method :func:`rownrs` should be used instead.

        """
        return self._rownr(self._makekey(key))

    def rownrs(self, key, upperkey={}, lowerincl=True, upperincl=True):
        """Get a sequence of row numbers containing the key(s).

        A single key can be given, but by giving argument `upperkey` as well
        a key range can be given (where upper key must be > lower).
        One can specify if the lower and upper key should be part of the range
        (`incl=True`) or not. By default both keys are part of the range.

        The key and optional upper key have to be given in the same way as
        for method :func:`rownr`.

        Similar to method :func:`rownr`. python's index operator [] can be used
        if the index consists of a single column. However, in this case only
        key ranges can be used (because the index operator with a single key
        returns a single row number, thus can only be used for unique indices).
        The lower key is inclusive, but the upper key is exclusive conform
        the standard python index semantics.

        For example::

          t = table('3c343.MS')
          tinx = t.index ('ANTENNA1')    # build index for antenna name
          rownr = tinx.rownr(0)          # find antenna1 = 0
          rownr = tinx[0:1]              # same as above

        """
        lkey = self._makekey(key)
        ukey = self._makekey(upperkey)
        if len(ukey) == 0:
            return self._rownrs(lkey)
        return self._rownrsrange(lkey, ukey, lowerincl, upperincl)

    def isunique(self):
        """Tell if all keys in the index are unique."""
        return self._isunique()

    def colnames(self):
        """Return the column names the index is made of."""
        return self._colnames()

    def setchanged(self, columnnames=[]):
        """Tell the index that data has changed.

        The index is smart enough to detect that the number of rows in the
        indexed table has changed. However, it cannot detect if a value in
        a column contained in this inex has changed. So it has to be told
        explicitly.

        `columnnames`
          The names of the columns in which data have changed.
          Giving no names means that all columns in the index have changed.
        """
        return self._setchanged(columnnames)

    def __getitem__(self, key):
        if not isinstance(key, slice):
            rnr = self.rownr(key)
            if rnr < 0:
                raise KeyError("key not found in tableindex")
            return rnr
        if key.step is not None:
            raise RuntimeError("tableindex slicing cannot have a step")
        lowerkey = 0
        if key.start is not None:
            lowerkey = key.start
        upperkey = 2147483647;  # highest int
        if key.stop is not None:
            upperkey = key.stop
            if (lowerkey >= upperkey):
                raise RuntimeError("tableindex slice stop must be > start")
        rnrs = self.rownrs(lowerkey, upperkey, True, False)
        if len(rnrs) == 0:
            raise KeyError("keys not found in tableindex")
        return rnrs
