# tableiter.py: Python tableiter functions
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
# $Id: tableiter.py,v 1.6 2006/12/11 02:46:08 gvandiep Exp $

# Make interface to class TableIterProxy available.
from ._tables import TableIter

from .table import table


class tableiter(TableIter):
    """The Python interface to Casacore table iterators

    A `tableiter` allows iteration through a table based on the contents
    of one or more columns. Each step in the iteration process forms
    a subset of the table for which the specified columns have the same value.

    It can easily be constructed using the :func:`table.iter` method as done
    in the example below::

      t = table('3c343.MS')
      for ts in t.iter('ANTENNA1'):
        print ts.nrows()

    In this example `ts` will be a so-called reference table which can be
    operated on like any other table object.

    Multiple column names should be given in a sequence (tuple or list).

    """

    def __init__(self, table, columnnames, order='', sort=True):
        st = sort
        if isinstance(sort, bool):
            st = 'heapsort'
            if not sort:
                st = 'nosort'
        TableIter.__init__(self, table, columnnames, order, st)

    def __iter__(self):
        # __iter__ is needed
        return self

    def next(self):
        # next returns a Table object, so turn that into table.
        return table(self._next(), _oper=3)

    def reset(self):
        """Reset the iterator to the beginning."""
        self._reset()

    __next__ = next
