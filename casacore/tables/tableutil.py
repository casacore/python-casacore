# tableutil.py: Utility table functions
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


from collections import defaultdict

import six
from .table import table
from .tablehelper import _remove_prefix, _value_type_name


def tablefromascii(tablename, asciifile,
                   headerfile='',
                   autoheader=False, autoshape=[],
                   columnnames=[], datatypes=[],
                   sep=' ',
                   commentmarker='',
                   firstline=1, lastline=-1,
                   readonly=True,
                   lockoptions='default', ack=True):
    """Create a table from an ASCII file.

    Create a table from a file in ASCII format. Columnar data as well as
    table and column keywords may be specified.
    Once the table is created from the ASCII data, it is opened in the
    specified mode and a table object is returned.

    The table columns are filled from a file containing the data values
    separated by a separator (one line per table row). The default
    separator is a blank. Blanks before and after the separator are ignored.
    If a non-blank separator is used, values can be empty. Such values
    default to 0, empty string, or F depending on the data type. E.g.
    1,,2, has 4 values of which the 2nd and 4th are empty and default to 0.
    Similarly if fewer values are given than needed, the missing values
    get the default value.

    Either the data format can be explicitly specified or it can be found
    automatically. The former gives more control in ambiguous situations.
    Both scalar and array columns can be generated from the ASCII input.
    The format string determines the type and optional shape.

    It is possible to give the column names and their data types in
    various ways:

    - Using 2 header lines (as described below) as the first two lines
      in the data file or in a separate header file. This is the default way.
    - Derive them automatically from the data (`autoheader=True`).
    - Using the arguments `columnnames` and
      `datatypes` (as non-empty vectors of strings).
      It implies (`autoheader=False`). The data types should be
      given in the same way as done in headers.

    In automatic mode (`autoheader=True`) the first line
    of the ASCII data is analyzed
    to deduce the data types. Only the types I, D, and A can be
    recognized. A number without decimal point or exponent is I (integer),
    otherwise it is D (double). Any other string is A (string).
    Note that a number may contain a leading sign (+ or -).
    The `autoshape` argument can be used to specify if the input
    should be stored as multiple scalars (the default) or as a single
    array. In the latter case one axis in the shape can be defined as
    variable length by giving it the value 0. It means that the actual
    array shape in a row is determined by the number of values in the
    corresponding input line.
    Columns get the names `Column1`, `Column2`, etc..
    For example:

    1. `autoshape=[]` (which is the default) means that all values
       are to be stored as scalar columns.
    2. `autoshape=0` means that all values in a row are to be stored as
       a variable length vector.
    3. `autoshape=10` defines a fixed length vector. If an input
       line contains less than 10 values, the vector is filled with default
       values. If more than 10 values, the latter values are ignored.
    4. `autoshape=[5,0]` defines a 2-dim array of which the 2nd axis is
       variable. Note that if an input line does not contain a multiple of 5
       values, the array is filled with default values.

    If the format of the table is explicitly specified, it has to be done
    either in the first two lines of the data file (named by the
    argument filename), or in a separate header file (named by the
    argument headerfile). In both forms, table keywords may also be
    specified before the column definitions.
    The column names and types can be described by two lines:

    1. The first line contains the names of the columns.
       These names may be enclosed in quotes (either single or double).
    2. The second line contains the data type and optionally the shape
       of each column. Valid types are:

       - S for Short data
       - I for Integer data
       - R for Real data
       - D for Double Precision data
       - X for Complex data (Real followed by Imaginary)
       - Z for Complex data (Amplitude then Phase)
       - DX for Double Precision Complex data (Real followed by Imaginary)
       - DZ for Double Precision Complex data (Amplitude then Phase)
       - A for ASCII data (a value must be enclosed in single or double quotes
         if it contains whitespace)
       - B for Boolean data (False are empty string, 0, or any string
         starting with F, f, N, or n).

    If a column is an array, the shape has to be given after the data type
    without any whitespace. E.g. `I10` defines an integer vector
    of length 10. `A2,5` defines a 2-dim string array with shape
    [2,5]. Note that `I` is not the same as `I1` as the
    first one defines a scalar and the other one a vector with length 1.
    The last column can have one variable length axis denoted by the value 0.
    It "consumes" the remainder of the input line.

    If the argument headerfile is set then the header information is
    read from that file instead of the first lines of the data file.

    To give a simple example of the form where the header information
    is located at the top of the data file::

      COLI   COLF   COLD       COLX        COLZ       COLS
        I      R      D          X           Z          A
        1      1.1    1.11       1.12 1.13   1.14 1.15  Str1
        10     11     12         13   14     15   16    ""

    Note that a complex number consists of 2 numbers.
    Also note that an empty string can be given.

    Let us now give an example of a separate header file that one might use to
    get interferometer data into casacore::

      U     V      W         TIME        ANT1       ANT2      DATA
      R     R      R          D           I          I        X1,0

    The data file would then look like::

      124.011 54560.0  3477.1  43456789.0990    1      2        4.327 -0.1132
      34561.0 45629.3  3900.5  43456789.0990    1      3        5.398 0.4521

    Note that the DATA column is defined as a 2-dim array of 1
    correlation and a variable number of channels, so the actual number of
    channels is determined by the input. In this example both rows will
    have 1 channel (note that a complex value contains 2 values).

    Tables may have keywords in addition to the columns. The keywords
    are useful for holding information that is global to the entire
    table (such as author, revision, history, etc.).
    The keywords in the header definitions must preceed the column descriptions.
    They must be enclosed between a line that starts with ".key..." and
    a line that starts with ".endkey..." (where ... can be anything).
    A table keywordset and column keywordsets can be specified.
    The latter can be specified by specifying the column name after
    the .keywords string.
    Between these two lines each line should contain the following:

    - The keyword name, e.g., ANYKEY
    - The datatype and optional  shape of the keyword
      (cf. list of valid types above)
    - The value or values for the keyword (the keyword may contain
      a scalar or an array of values). e.g., 3.14159 21.78945

    Thus to continue the example above, one might wish to add keywords
    as follows::

      .keywords
      DATE        A  "97/1/16"
      REVISION    D 2.01
      AUTHOR      A "Tim Cornwell"
      INSTRUMENT  A "VLA"
      .endkeywords
      .keywords TIME
      UNIT A "s"
      .endkeywords
      U     V      W         TIME        ANT1       ANT2      DATA
      R     R      R          D           I          I        X1,0

    Similarly to the column format string, the keyword formats can also
    contain shape information. The only difference is that if no shape is
    given, a keyword can have multiple values (making it a vector).

    It is possible to ignore comment lines in the header and data file
    by giving the `commentmarker`. It indicates that lines
    starting with the given marker are ignored. Note that the marker can
    be a regular expression (e.g. `' *//'` tells that lines starting
    with // and optionally preceeded by blanks have to be ignored).

    With the arguments `firstline` and `lastline` one can
    specify which lines have to be taken from the input file. A negative value
    means 1 for `firstline` or end-of-file for `lastline`.
    Note that if the headers and data are combined in one file,
    these line arguments apply to the whole file. If headers and data are in
    separate files, these line arguments apply to the data file only.

    Also note that ignored comment lines are counted, thus are used to
    determine which lines are in the line range.

    The number of rows is determined by the number of lines read from the data
    file.

    """
    import os.path
    filename = os.path.expandvars(asciifile)
    filename = os.path.expanduser(filename)
    if not os.path.exists(filename):
        s = "File '%s' not found" % (filename)
        raise IOError(s)
    if headerfile != '':
        filename = os.path.expandvars(headerfile)
        filename = os.path.expanduser(filename)
        if not os.path.exists(filename):
            s = "File '%s' not found" % (filename)
            raise IOError(s)
    tab = table(asciifile, headerfile, tablename, autoheader, autoshape,
                sep, commentmarker, firstline, lastline,
                _columnnames=columnnames, _datatypes=datatypes, _oper=1)
    six.print_('Input format: [' + tab._getasciiformat() + ']')
    # Close table and reopen it in correct way.
    tab = 0
    return table(tablename, readonly=readonly, lockoptions=lockoptions,
                 ack=ack)


# Create a description of a scalar column
def makescacoldesc(columnname, value,
                   datamanagertype='',
                   datamanagergroup='',
                   options=0, maxlen=0, comment='',
                   valuetype='', keywords={}):
    """Create description of a scalar column.

    A description for a scalar column can be created from a name for
    the column and a data value, which is used only to determine the
    type of the column. Note that a dict value is also possible.

    It is possible to create the column description in more detail
    by giving the data manager name, group, option, and comment as well.

    The data manager type tells which data manager (storage manager)
    is used to store the columns. The data manager type and group are
    explained in more detail in the `casacore Tables
    <../../casacore/doc/html/group__Tables__module.html>`_ documentation.

    It returns a dict with fields `name` and `desc` which can thereafter be used
    to build a table description using function :func:`maketabdesc`.

    `columname`
      Name of column
    `value`
      Example data value used to determine the column's data type.
      It is only used if argument `valuetype` is not given.
    `datamanagertype`
      Type of data manager which can be one of StandardStMan (default)
      or IncrementalStMan. The latter one can save disk space if many subsequent
      cells in the column will have the same value.
    `datamanagergroup`
      Data manager group. Only for the expert user.
    `options`
      Options. Need not be filled in.
    `maxlen`
      Maximum length of string values in a column.
      Default 0 means unlimited.
    `comment`
      Comment: informational for user.
    `valuetype`
      A string giving the column's data type. Possible data types are
      bool (or boolean), uchar (or byte), short, int (or integer), uint,
      float, double, complex, dcomplex, and string.
    'keywords'
      A dict defining initial keywords for the column.

    For example::

      scd1 = makescacoldesc("col2", ""))
      scd2 = makescacoldesc("col1", 1, "IncrementalStMan")
      td = maketabdesc([scd1, scd2])

    This creates a table description consisting of an integer column `col1`,
    and a string column `col2`. `col1` uses the IncrementalStMan storage manager,
    while `col2` uses the default storage manager StandardStMan.

    """
    vtype = valuetype
    if vtype == '':
        vtype = _value_type_name(value)
    rec2 = {'valueType': vtype,
            'dataManagerType': datamanagertype,
            'dataManagerGroup': datamanagergroup,
            'option': options,
            'maxlen': maxlen,
            'comment': comment,
            'keywords': keywords}
    return {'name': columnname,
            'desc': rec2}


# Create a description of an array column
def makearrcoldesc(columnname, value, ndim=0,
                   shape=[], datamanagertype='',
                   datamanagergroup='',
                   options=0, maxlen=0, comment='',
                   valuetype='', keywords={}):
    """Create description of an array column.

    A description for a scalar column can be created from a name for
    the column and a data value, which is used only to determine the
    type of the column. Note that a dict value is also possible.

    It is possible to create the column description in more detail
    by giving the dimensionality, shape, data manager name, group, option,
    and comment as well.

    The data manager type tells which data manager (storage manager)
    is used to store the columns. The data manager type and group are
    explained in more detail in the `casacore Tables
    <../../casacore/doc/html/group__Tables__module.html>`_ documentation.

    It returns a dict with fields `name` and `desc` which can thereafter be used
    to build a table description using function :func:`maketabdesc`.

    `name`
      The name of the column.
    `value`
      A data value, which is only used to determine the data type of the column.
      It is only used if argument `valuetype` is not given.
    `ndim`
      Optionally the number of dimensions. A value > 0 means that all
      arrays in the column must have that dimensionality. Note that the
      arrays can still differ in shape unless the shape vector is also given.
    `shape`
      An optional sequence of integers giving the shape of the array in each
      cell. If given, it forces option FixedShape (see below) and sets the
      number of dimensions (if not given). All arrays in the column get the
      given shape and the array is created as soon as a row is added.
      Note that the shape vector gives the shape in each table cell; the
      number of rows in the table should NOT be part of it.
    `datamanagertype`
      Type of data manager which can be one of StandardStMan (default),
      IncrementalStMan, TiledColumnStMan, TiledCellStMan, or TiledShapeStMan.
      The tiled storage managers are usually used for bigger data arrays.
    `datamanagergroup`
      Data manager group. Only for the expert user.
    `options`
      Optionally numeric array options which can be added to combine them.

      `1` means Direct.
          It tells that the data are directly stored in the table. Direct
          forces option FixedShape. If not given, the array is indirect, which
          means that the data will be stored in a separate file.
      `4` means FixedShape.
          This option does not need to be given, because it is enforced if
          the shape is given. FixedShape means that the shape of the array must
          be the same in each cell of the column. Otherwise the array shapes may
          be different in each column cell and is it possible that a cell does
          not contain an array at all.
          Note that when given (or implicitly by option Direct), the
          shape argument must be given as well.

      Default is 0, thus indirect and variable shaped.
    `maxlen`
      Maximum length of string values in a column.
      Default 0 means unlimited.
    `comment`
      Comment: informational for user.
    `valuetype`
      A string giving the column's data type. Possible data types are
      bool (or boolean), uchar (or byte), short, int (or integer), uint,
      float, double, complex, dcomplex, and string.
    'keywords'
      A dict defining initial keywords for the column.

    For example::

      acd1= makescacoldesc("arr1", 1., 0, [2,3,4])
      td = maketabdesc(acd1)

    This creates a table description consisting of an array column `arr1`
    containing 3-dim arrays of doubles with shape [2,3,4].

    """
    vtype = valuetype
    if vtype == '':
        vtype = _value_type_name(value)
    if len(shape) > 0:
        if ndim <= 0:
            ndim = len(shape)
    rec2 = {'valueType': vtype,
            'dataManagerType': datamanagertype,
            'dataManagerGroup': datamanagergroup,
            'ndim': ndim,
            'shape': shape,
            '_c_order': True,
            'option': options,
            'maxlen': maxlen,
            'comment': comment,
            'keywords': keywords}
    return {'name': columnname,
            'desc': rec2}


# Create a description of a column
def makecoldesc(columnname, desc):
    """Create column description using the description of another column.

    The other description can be obtained from a table using function
    :func:`getcoldesc` or from another column description dict using
    `otherdesc['desc']`.

    It returns a dict with fields `name` and `desc` which can thereafter be used
    to build a table description using function :func:`maketabdesc`.

    `columname`
      Name of column
    `desc`
      Description of the column

    For example::

      cd1 = makecoldesc("col2", t.getcoldesc('othercol'))
      td = maketabdesc(cd1)

    This creates a table description consisting of a column `col2` having
    the same description as column `othercol`.

    """
    return {'name': columnname,
            'desc': desc}


# Create a table description from a set of column descriptions
def maketabdesc(descs=[]):
    """Create a table description.

    Creates a table description from a set of column descriptions. The
    resulting table description can be used in the :class:`table` constructor.

    For example::

      scd1 = makescacoldesc("col2", "aa")
      scd2 = makescacoldesc("col1", 1, "IncrementalStMan")
      scd3 = makescacoldesc("colrec1", {})
      acd1 = makearrcoldesc("arr1", 1, 0, [2,3,4])
      acd2 = makearrcoldesc("arr2", 0.+0j)
      td = maketabdesc([scd1, scd2, scd3, acd1, acd2])
      t = table("mytable", td, nrow=100)

    | This creates a table description `td` from five column descriptions
      and then creates a 100-row table called `mytable` from the table
      description.
    | The columns contain respectivily strings, integer scalars, records,
      3D integer arrays with fixed shape [2,3,4], and complex arrays with
      variable shape.

    """
    rec = {}
    # If a single dict is given, make a list of it.
    if isinstance(descs, dict):
        descs = [descs]
    for desc in descs:
        colname = desc['name']
        if colname in rec:
            raise ValueError('Column name ' + colname + ' multiply used in table description')
        rec[colname] = desc['desc']
    return rec

def makedminfo(tabdesc, group_spec=None):
  """Creates a data manager information object.

  Create a data manager information dictionary outline from a table description.
  The resulting dictionary is a bare outline and is available for the purposes of
  further customising the data manager via the `group_spec` argument.

  The resulting dictionary can be used in the :class:`table` constructor and
  the :meth:`default_ms` and :meth:`default_ms_subtable` functions.

  `tabdesc`
    The table description
  `group_spec`
    The SPEC for a data manager group. In practice this is useful for
    setting the Default Tile Size and Maximum Cache Size for the Data Manager::

      {
        'WeightColumnGroup' : {
          'DEFAULTTILESHAPE': np.int32([4,4,4]),
          'MAXIMUMCACHESIZE': 1000,
        }
      }

    This should be used with care.

  """
  if group_spec is None:
    group_spec = {}

  class DMGroup(object):
    """
    Keep track of the columns, type and spec of each data manager group
    """
    def __init__(self):
      self.columns = []
      self.type = None
      self.spec = None

  dm_groups = defaultdict(DMGroup)

  # Iterate through the table columns, grouping them
  # by their dataManagerGroup
  for c, d in six.iteritems(tabdesc):
    if c in ('_define_hypercolumn_', '_keywords_', '_private_keywords_'):
      continue

    # Extract group and data manager type
    group = d.get("dataManagerGroup", "StandardStMan")
    type_ = d.get("dataManagerType", "StandardStMan")

    # Set defaults if necessary
    if not group:
      group = "StandardStMan"

    if not type_:
      type_ = "StandardStMan"

    # Obtain the (possibly empty) data manager group
    dm_group = dm_groups[group]

    # Add the column
    dm_group.columns.append(c)

    # Set the spec
    if dm_group.spec is None:
      dm_group.spec = group_spec.get(group, {})

    # Check that the data manager type is consistent across columns
    if dm_group.type is None:
      dm_group.type = type_
    elif not dm_group.type == type_:
      raise ValueError("Mismatched dataManagerType '%s' "
                        "for dataManagerGroup '%s' "
                        "Previously, the type was '%s'" %
                            (type_, group, dm_group.type))

  # Output a data manager entry
  return {
    '*%d'%(i+1): {
      'COLUMNS': dm_group.columns,
      'TYPE': dm_group.type,
      'NAME': group,
      'SPEC' : dm_group.spec,
      'SEQNR': i
    } for i, (group, dm_group)
    in enumerate(six.iteritems(dm_groups))
  }

# Create the old glish names for them.
tablecreatescalarcoldesc = makescacoldesc
tablecreatearraycoldesc = makearrcoldesc
tablecreatedesc = maketabdesc
tablecreatedm = makedminfo


# Define a hypercolumn in the table description.
def tabledefinehypercolumn(tabdesc,
                           name, ndim, datacolumns,
                           coordcolumns=False,
                           idcolumns=False):
    """Add a hypercolumn to a table description.

    It defines a hypercolumn and adds it the given table description.
    A hypercolumn is an entity used by the Tiled Storage Managers (TSM). It
    defines which columns have to be stored together with a TSM.

    It should only be used by expert users who want to use a TSM to its
    full extent. For a basic TSM s hypercolumn definition is not needed.

    tabledesc
      A table description (result from :func:`maketabdesc`).
    name
      Name of hypercolumn
    ndim
      Dimensionality of hypercolumn; normally 1 more than the dimensionality
      of the arrays in the data columns to be stored with the TSM
    datacolumns
      Data columns to be stored with TSM
    coordcolumns
      Optional coordinate columns to be stored with TSM
    idcolumns
      Optional id columns to be stored with TSM

    For example::

      scd1 = makescacoldesc("col2", "aa")
      scd2 = makescacoldesc("col1", 1, "IncrementalStMan")
      scd3 = makescacoldesc("colrec1", {})
      acd1 = makearrcoldesc("arr1", 1, 0, [2,3,4])
      acd2 = makearrcoldesc("arr2", as_complex(0))
      td = maketabdesc([scd1, scd2, scd3, acd1, acd2])
      tabledefinehypercolumn(td, "TiledArray", 4, ["arr1"])
      tab = table("mytable", tabledesc=td, nrow=100)

    | This creates a table description `td` from five column descriptions
      and then creates a 100-row table called mytable from the table
      description.
    | The columns contain respectivily strings, integer scalars, records,
      3D integer arrays with fixed shape [2,3,4], and complex arrays with
      variable shape.
    | The first array is stored with the Tiled Storage Manager (in this case
      the TiledColumnStMan).

    """
    rec = {'HCndim': ndim,
           'HCdatanames': datacolumns}
    if not isinstance(coordcolumns, bool):
        rec['HCcoordnames'] = coordcolumns
    if not isinstance(idcolumns, bool):
        rec['HCidnames'] = idcolumns
    if '_define_hypercolumn_' not in tabdesc:
        tabdesc['_define_hypercolumn_'] = {}
    tabdesc['_define_hypercolumn_'][name] = rec


def tabledelete(tablename, checksubtables=False, ack=True):
    """Delete a table on disk.

    It is the same as :func:`table.delete`, but without the need to open
    the table first.

    """
    tabname = _remove_prefix(tablename)
    t = table(tabname, ack=False)
    if t.ismultiused(checksubtables):
        six.print_('Table', tabname, 'cannot be deleted; it is still in use')
    else:
        t = 0
        table(tabname, readonly=False, _delete=True, ack=False)
        if ack:
            six.print_('Table', tabname, 'has been deleted')


def tableexists(tablename):
    """Test if a table exists."""
    result = True
    try:
        t = table(tablename, ack=False)
    except:
        result = False
    return result


def tableiswritable(tablename):
    """Test if a table is writable."""
    result = True
    try:
        t = table(tablename, readonly=False, ack=False)
        result = t.iswritable()
    except:
        result = False
    return result


def tablecopy(tablename, newtablename, deep=False, valuecopy=False, dminfo={},
              endian='aipsrc', memorytable=False, copynorows=False):
    """Copy a table.

    It is the same as :func:`table.copy`, but without the need to open
    the table first.

    """
    t = table(tablename, ack=False)
    return t.copy(newtablename, deep=deep, valuecopy=valuecopy,
                  dminfo=dminfo, endian=endian, memorytable=memorytable,
                  copynorows=copynorows)


def tablerename(tablename, newtablename):
    """Rename a table.

    The table with the given name is renamed (or moved) to the new name.

    """
    t = table(tablename, ack=False)
    t.rename(newtablename)


def tableinfo(tablename):
    """Get type info of a table.

    It is the same as :func:`table.info`, but without the need to open
    the table first.

    """
    t = table(tablename, ack=False)
    return t.info()


def tablesummary(tablename):
    """Get the summary of a table.

    It is the same as :func:`table.summary`, but without the need to open
    the table first.

    """
    t = table(tablename, ack=False)
    t.summary()


def tablestructure(tablename, dataman=True, column=True, subtable=False,
                   sort=False):
    """Print the structure of a table.

    It is the same as :func:`table.showstructure`, but without the need to open
    the table first.

    """
    t = table(tablename, ack=False)
    six.print_(t.showstructure(dataman, column, subtable, sort))
