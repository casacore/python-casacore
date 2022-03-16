# __init__.py: Top level .py file for python table interface
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
# $Id: __init__.py,v 1.6 2006/11/06 01:54:21 gvandiep Exp $

"""Python interface to the Casacore tables module.

A `casacore table <../../casacore/doc/html/group__Tables__module.html>`_
is similar to a relational data base table with the extension
that table cells can contain n-dimensional arrays.
It has a rich SQL-like query language
(`TaQL <../../doc/199.html>`_).

A table consists of numbered rows and named columns. A column can hold
scalar values or arrays of any dimensionality and shape. Furthermore the
table and each column can hold a set of keywords (e.g. to define the units).
It is nestable, thus the value of a keyword can be a keyword set in itself.

The `tables` module consists of a few classes:

:class:`table`
  main module to open, create, access, and query tables
:class:`tablecolumn`
  access the contents of a column in an easier way
:class:`tablerow`
  access the contents of table rows or parts of it
:class:`tableiter`
  iterate through a table based on the contents of one or more columns
:class:`tableindex`
  build and use an index on one or more table columns
submodule `tableutil <#table-utility-functions>`_
  table utility functions (e.g. to create a table description)
submodule `msutil <#measurementset-utility-functions>`_
  MeasuementSet utility functions (e.g. to concat MSs)

"""

from .msutil import *
from .table import table
from .table import default_ms
from .table import default_ms_subtable
from .table import tablecommand
from .table import taql
from .tablecolumn import tablecolumn
from .tableindex import tableindex
from .tableiter import tableiter
from .tablerow import tablerow
from .tableutil import *
