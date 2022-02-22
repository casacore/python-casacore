# tablehelper.py: Helper table functions
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
# $Id: tableutil.py,v 1.6 2006/11/08 00:12:55 gvandiep Exp $

from six import string_types, integer_types
import numpy
import re
from ..quanta import quantity


# A keywordset in a table can hold tables, but it is not possible to
# pass them around because a ValueHolder cannot deal with it.
# Therefore it is passed around as a string with a special prefix.
def _add_prefix(name):
    """Add the prefix 'Table: ' to a table name to get a specific keyword value."""
    return 'Table: ' + name


def _do_remove_prefix(name):
    """Strip the possible prefix 'Table: ' from a table name."""
    res = name
    if isinstance(res, string_types):
        if res.find('Table: ') == 0:
            res = res.replace('Table: ', '', 1)
    return res


def _remove_prefix(name):
    """Strip the possible prefix 'Table: ' from one or more table names."""
    if isinstance(name, string_types):
        return _do_remove_prefix(name)
    return [_do_remove_prefix(nm) for nm in name]


def _check_index(key, name):
    # The __index__ method converts e.g. np.int16 to a proper integer.
    # An exception is thrown if the type does not have __index__ which
    # means that the given key cannot be used as an index.
    try:
        return key.__index__()
    except:
        raise TypeError(name + " indices must be integer (or None in a slice)")


# Check a key or slice given to index a tablerow or tablecolumn object.
# A TypeError exception is raised if values or not integer or None.
# An IndexError is raised if incorrect values are given.
# It returns a list of length 1 if a single index is given.
# Otherwise it returns [startrow, nrow, step].
def _check_key_slice(key, nrows, name):
    if not isinstance(key, slice):
        inx = _check_index(key, name)
        # A single index (possibly negative, thus from the end).
        if inx < 0:
            inx += nrows
        if inx < 0 or inx >= nrows:
            raise IndexError(name + " index out of range")
        return [inx]
    # Given as start:stop:step where each part is optional and can
    # be negative.
    incr = 1
    if key.step is not None:
        incr = _check_index(key.step, name)
        if incr == 0:
            raise RuntimeError(name + " slice step cannot be zero")
    strow = 0
    endrow = nrows
    if incr < 0:
        strow = nrows - 1
        endrow = -1
    if key.start is not None:
        strow = _check_index(key.start, name)
        if strow < 0:
            strow += nrows
        strow = min(max(strow, 0), nrows - 1)
    if key.stop is not None:
        endrow = _check_index(key.stop, name)
        if endrow < 0:
            endrow += nrows
        endrow = min(max(endrow, -1), nrows)
    if incr > 0:
        nrow = int((endrow - strow + incr - 1) / incr)
    else:
        nrow = int((strow - endrow - incr - 1) / -incr)
    nrow = max(0, nrow)
    return [strow, nrow, incr]


# Convert Python value type to a glish-like type string
# as expected by the table code.
def _value_type_name(value):
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, integer_types):
        return 'integer'
    if isinstance(value, float):
        return 'double'
    if isinstance(value, complex):
        return 'dcomplex'
    if isinstance(value, string_types):
        return 'string'
    if isinstance(value, dict):
        return 'record'
    return 'unknown'


def _format_date(val, unit):
    """
    Format dates.
    :param val: Value (just the value, not a quantity)
    :param unit: Unit. Should be 'rad' or 's'
    :return: A string representation of this date.

    >>> _format_date(4914741782.503475, 's')
    "14-Aug-2014/14:03:03"
    """
    if val == numpy.floor(val) and unit == 'd':
        # Do not show time part if 0
        return quantity(val, unit).formatted('YMD_ONLY')
    else:
        return quantity(val, unit).formatted('DMY')


def _format_quantum(val, unit):
    """
    Format a quantity with reasonable units.
    :param val: The value (just the value, not a quantity)
    :param unit: Unit (something that can be fed to quanta).
    :return: A string representation of this quantity.

    >>> _format_quantum(3, 'm')
    "3 m"
    >>> _format_quantum(4914741782.503475, 's')
    "4.91474e+09 s"
    """
    q = quantity(val, unit)
    if q.canonical().get_unit() in ['rad', 's']:
        return quantity(val, 'm').formatted()[:-1] + unit
    else:
        return q.formatted()


def _format_cell(val, colkeywords):
    """
    Format a cell of the table. Colkeywords can add units.
    :param val: A plain value (not a quantum)
    :param colkeywords:
    :return: A HTML representation of this cell.
    """
    out = ""

    # String arrays are returned as dict, undo that for printing
    if isinstance(val, dict):
        tmpdict = numpy.array(val['array'])
        tmpdict.reshape(val['shape'])
        # Leave out quotes around strings
        numpy.set_printoptions(formatter={'all': lambda x: str(x)})
        out += numpy.array2string(tmpdict, separator=', ')
        # Revert previous numpy print options
        numpy.set_printoptions(formatter=None)
    else:
        valtype = 'other'

        # Check if the column unit is like 'm' or ['m','m','m']
        singleUnit = ('QuantumUnits' in colkeywords and
                      (numpy.array(colkeywords['QuantumUnits']) == numpy.array(colkeywords['QuantumUnits'])[0]).all())
        if colkeywords.get('MEASINFO', {}).get('type') == 'epoch' and singleUnit:
            # Format a date/time. Use quanta for scalars, use numpy for array logic around it
            # (quanta does not support higher dimensional arrays)
            valtype = 'epoch'
            if isinstance(val, numpy.ndarray):
                numpy.set_printoptions(formatter={'all': lambda x: _format_date(x, colkeywords['QuantumUnits'][0])})
                out += numpy.array2string(val, separator=', ')
                numpy.set_printoptions(formatter=None)
            else:
                out += _format_date(val, colkeywords['QuantumUnits'][0])
        elif colkeywords.get('MEASINFO', {}).get('type') == 'direction' and singleUnit and val.shape == (1, 2):
            # Format one direction. TODO: extend to array of directions
            valtype = 'direction'
            out += "["
            part = quantity(val[0, 0], 'rad').formatted("TIME", precision=9)
            part = re.sub(r'(\d+):(\d+):(.*)', r'\1h\2m\3', part)
            out += part + ", "
            part = quantity(val[0, 1], 'rad').formatted("ANGLE", precision=9)
            part = re.sub(r'(\d+)\.(\d+)\.(.*)', r'\1d\2m\3', part)
            out += part + "]"
        elif isinstance(val, numpy.ndarray) and singleUnit:
            # Format any array with units
            valtype = 'quanta'
            numpy.set_printoptions(formatter={'all': lambda x: _format_quantum(x, colkeywords['QuantumUnits'][0])})
            out += numpy.array2string(val, separator=', ')
            numpy.set_printoptions(formatter=None)
        elif isinstance(val, numpy.ndarray):
            valtype = 'other'
            # Undo quotes around strings
            numpy.set_printoptions(formatter={'all': lambda x: str(x)})
            out += numpy.array2string(val, separator=', ')
            numpy.set_printoptions(formatter=None)
        elif singleUnit:
            valtype = 'onequantum'
            out += _format_quantum(val, colkeywords['QuantumUnits'][0])
        else:
            valtype = 'other'
            out += str(val)

    if 'QuantumUnits' in colkeywords and valtype == 'other':
        # Print units if they haven't been taken care of
        if not (numpy.array(colkeywords['QuantumUnits']) == numpy.array(colkeywords['QuantumUnits'])[0]).all():
            # Multiple different units for element in an array.
            # For now, just print the units and let the user figure out what it means
            out += " " + str(colkeywords['QuantumUnits'])
        else:
            out += " " + colkeywords['QuantumUnits'][0]

    # Numpy sometimes adds double newlines, don't do that
    out = out.replace('\n\n', '\n')
    return out


def _format_row(row, colnames, tab):
    """
    Helper function for _repr_html. Formats one row.
    :param row: row of this table
    :param colnames: vector of column names
    :param tab: table, used to get the column keywords
    :return: html-formatted row
    """
    out = ""

    out += "\n<tr>"
    for colname in colnames:
        out += "<td style='vertical-align:top; white-space:pre'>"
        out += _format_cell(row[colname], tab.getcolkeywords(colname))
        out += "</td>\n"
    out += "</tr>\n"
    return out
