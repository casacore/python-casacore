# tableindex.py: Python tableindex functions
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
# $Id: tableindex.py,v 1.6 2006/11/08 00:12:55 gvandiep Exp $

# Make interface to class TableIndexProxy available.
from _tables import TableIndex

class tableindex(TableIndex):
    """
        The Python interface to AIPS++ table index
    """

    def __init__(self, table, columnnames, sort=True):
        TableIndex.__init__ (self, table, columnnames, sort);

    def _makekey (self, key):
        d = key;
        if not isinstance(d, dict):
            cols = self.colnames();
            if len(cols) != 1:
                raise RunTimeError("key has to be given as a dict for a multi-column index");
            d = {cols[0] : key};
        return d;

    def rownr (self, key):
        return self._rownr (self._makekey(key));

    def rownrs (self, key, upperkey={}, lowerincl=True, upperincl=True):
        lkey = self._makekey(key);
        ukey = self._makekey(upperkey);
        if len(ukey) == 0:
            return self._rownrs (lkey);
        return self._rownrsrange (lkey, ukey, lowerincl, upperincl);

    def __getitem__ (self, key):
        if not isinstance(key, slice):
            rnr = self.rownr (key);
            if rnr < 0:
                raise KeyError("key not found in tableindex");
            return rnr;
        if key.step != None:
            raise RuntimeError("tableindex slicing cannot have a step");
        lowerkey = 0;
        if key.start != None:
            lowerkey = key.start;
        upperkey = 2147483647;        # highest int
        if key.stop != None:
            upperkey = key.stop;
            if (lowerkey >= upperkey):
                raise RuntimeError("tableindex slice stop must be > start");
        rnrs = self.rownrs (lowerkey, upperkey, True, False);
        if len(rnrs) == 0:
            raise KeyError("keys not found in tableindex");
        return rnrs;
