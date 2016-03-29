# tablehelper.py: Helper table functions
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

from casacore.six import PY2


# A keywordset in a table can hold tables, but it is not possible to
# pass them around because a ValueHolder cannot deal with it.
# Therefore it is passed around as a string with a special prefix.
def _add_prefix (name):
    """Add the prefix 'Table: ' to a table name to get a specific keyword value."""
    return 'Table: ' + name;

def _do_remove_prefix (name):
    """Strip the possible prefix 'Table: ' from a table name."""
    res = name;
    if isinstance(res, str):
        if (res.find ('Table: ') == 0):
            res = res.replace ('Table: ', '', 1);
    return res;

def _remove_prefix (name):
    """Strip the possible prefix 'Table: ' from one or more table names."""
    if isinstance(name, str):
        return _do_remove_prefix (name)
    return [_do_remove_prefix(nm) for nm in name]

def _check_index (key, name):
    # The __index__ method converts e.g. np.int16 to a proper integer.
    # An exception is thrown if the type does not have __index__ which
    # means that the given key cannot be used as an index.
    try:
        return key.__index__()
    except:
        raise TypeError(name + " indices must be integer (or None in a slice)");
    
# Check a key or slice given to index a tablerow or tablecolumn object.
# A TypeError exception is raised if values or not integer or None.
# An IndexError is raised if incorrect values are given. 
# It returns a list of length 1 if a single index is given.
# Otherwise it returns [startrow, nrow, step].
def _check_key_slice (key, nrows, name):
    if not isinstance(key, slice):
        inx = _check_index (key, name)
        # A single index (possibly negative, thus from the end).
        if inx < 0:
            inx += nrows;
        if inx < 0  or  inx >= nrows:
            raise IndexError(name + " index out of range");
        return [inx];
    # Given as start:stop:step where each part is optional and can
    # be negative.
    incr = 1;
    if key.step != None:
        incr = _check_index (key.step, name);
        if incr == 0:
            raise RunTimeError(name + " slice step cannot be zero");
    strow  = 0;
    endrow = nrows;
    if incr < 0:
        strow  = nrows-1;
        endrow = -1;
    if key.start != None:
        strow = _check_index (key.start, name);
        if strow < 0:
            strow += nrows;
        strow = min(max(strow,0), nrows-1);
    if key.stop != None:
        endrow = _check_index (key.stop, name);
        if endrow < 0:
            endrow += nrows;
        endrow = min(max(endrow,-1), nrows);
    if incr > 0:
        nrow = int((endrow - strow + incr - 1) / incr);
    else:
        nrow = int((strow - endrow - incr - 1) / -incr);
    nrow = max(0, nrow);
    return [strow,nrow,incr];


# Convert Python value type to a glish-like type string
# as expected by the table code.
def _value_type_name (value):
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, int):
        return 'integer'
    if PY2 and isinstance(value, long):
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
