# table.py: Python table functions
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
"""Access to Casacore tables.

The :class:`table` class is the main class to access a table. Its constructor
can open or create a table.

Several utility functions exist. Important ones are:

:func:`taql` (or its synonym `tablecommand`)
  executes a TaQL query command and returns a :class:`table` object.
:func:`tablefromascii`
  creates a table from an ASCII file and returns a :class:`table` object.

"""

from six import string_types
from ._tables import (Table,
                      _default_ms,
                      _default_ms_subtable,
                      _required_ms_desc,
                      _complete_ms_desc)

from .tablehelper import (_add_prefix, _remove_prefix, _do_remove_prefix,
                          _format_row)
import six


def default_ms(name, tabdesc=None, dminfo=None):
    """
    Creates a default Measurement Set called name. Any Table Description
    elements in tabdesc will overwrite the corresponding element in a default
    Measurement Set Table Description (columns, hypercolumns and keywords).

    In practice, you probably want to specify columns such as DATA, MODEL_DATA
    and CORRECTED_DATA (and their associated keywords and hypercolumns)
    in tabdesc.
    """

    # Default to empty dictionaries
    if tabdesc is None:
        tabdesc = {}

    if dminfo is None:
        dminfo = {}

    # Wrap the Table object
    return table(_default_ms(name, tabdesc, dminfo), _oper=3)


def default_ms_subtable(subtable, name=None, tabdesc=None, dminfo=None):
    """
    Creates a default Measurement Set subtable. Any Table Description
    elements in tabdesc will overwrite the corresponding element in a default
    Measurement Set Table Description (columns, hypercolumns and keywords).

    if name is given, it will be treated as a path that the table should
    be created in. Set to subtable if None

    if subtable is "" or "MAIN" a standard MeasurementSet with subtables will
    be created.
    """

    if name is None:
        name = subtable

    # Default to empty dictionaries
    if tabdesc is None:
        tabdesc = {}

    if dminfo is None:
        dminfo = {}

    # Wrap the Table object
    return table(_default_ms_subtable(subtable, name, tabdesc, dminfo),
                 _oper=3)


# Execute a TaQL command on a table.
def taql(command, style='Python', tables=[], globals={}, locals={}):
    """Execute a TaQL command and return a table object.

    A `TaQL <../../doc/199.html>`_
    command is an SQL-like command to do a selection of rows and/or
    columns in a table.

    The default style used in a TaQL command is python, which means 0-based
    indexing, C-ordered arrays, and non-inclusive end in ranges.

    It is possible to use python variables directly in the command using
    `$var` where `var` is the name of the variable to use. For example::

      t = table('3c343.MS')
      value = 5.1
      t1 = taql('select from $t where COL > $value')

    In this example the table `$t` is replaced by a sequence number
    (such as `$1`) and `$value` by its value 5.1.
    The table object of `t` will be appended to a copy of the `tables`
    argument such that the sequence number inserted matches the table object
    in the list.
    The more advanced user can already use `$n` in the query string and
    supply the associated table object in the `tables` argument
    (where `n` represents the (n-1)th `tables` element).

    The :func:`query` command makes use of this feature.

    The arguments `globals` and `locals` can be used to pass in a dict
    containing the possible variables used in the TaQL command. They can
    be obtained with the python functions locals() and globals().
    If `locals` is empty, the local variables in the calling function will
    be used, so normally one does not need to use these arguments.

    """
    # Substitute possible tables given as $name.
    cmd = command
    # Copy the tables argument and make sure it is a list
    tabs = []
    for tab in tables:
        tabs += [tab]
    try:
        import casacore.util
        if len(locals) == 0:
            # local variables in caller are 3 levels up from getlocals
            locals = casacore.util.getlocals(3)
        cmd = casacore.util.substitute(cmd, [(table, '', tabs)],
                                       globals, locals)
    except Exception:
        pass
    if style:
        cmd = 'using style ' + style + ' ' + cmd
    tab = table(cmd, tabs, _oper=2)
    result = tab._getcalcresult()
    # If result is empty, it was a normal TaQL command resulting in a table.
    # Otherwise it is a record containing calc values.
    if len(result) == 0:
        return tab
    return result['values']


# alias
tablecommand = taql


class table(Table):
    """The Python interface to Casacore tables.

    One can open or create tables, get or put data in them, make selections,
    get meta information (like storage managers used), etc.
    It is possible to lock/unlock a table for concurrent access.

    A table consists of numbered rows and named columns. A column can hold
    scalar values or arrays of any dimensionality and shape. Furthermore the
    table and each column can hold a possibly nested keyword set
    (e.g. to define the units).

    The classes :class:`tablecolumn`, :class:`tableiter`, :class:`tableindex`,
    and :class:`tablerow` tablecolumn can be used for easier access to tables.
    Module tableutil contains some useful utility functions, for instance
    :func:`tablefromascii` to create a table from an ASCII file.

    Several functions accept or return arrays for which numpy arrays are used.
    One dimensional arrays can also be passed as sequences (e.g., a list).
    A scalar value can also be passed to functions expecting an array and
    results in a 1-dim array of length 1.
    Scalar arguments can be passed as normal python scalars, but also as
    numpy scalars (which have a special data type).
    If needed and if possible, data type conversion is done automatically.

    A `table` object contains a :class:`tablerow` object which contains
    all columns. Similar to `tablerow` the `table` object can be indexed
    in the standard python way to get (or put) values in one or more rows.
    For example::

      t = table('~/3c343.MS')
      print t[0]

    The `table` class supports the context manager idiom
    (__enter__ and __exit__).
    When used in a `with` statement, the table will be flushed and closed
    automatically, which is handy when writing a table.
    For example::

      with table('my.ms') as t:
        t.putcell ('SPECTRAL_WINDOW_ID', 0, 0)


    Usually a table is kept on disk, but it can also reside in memory.
    Furthermore, results of sort and selection are kept as so-called
    reference tables which are kept in memory (but can be made persistent).

    `table('tablename', tabledesc)`
      creates a new table using the given table description which can be
      obtained from an existing table (using table.getdesc) or created
      (using tableutil.maketabdesc).
      If `memorytable=True`, the table is created in memory.
    `table('tablename', readonly=False)`
      | opens an existing table for read/write. Default is for readonly.
      | In general it is a bad idea to open a subtable using a path like
        'my.ms/ANTENNA', because it will fail if 'my.ms' is a selection instead
        of a plain table. Therefore a double colon can be used like
        'my.ms::ANTENNA' making the table system handle it in a correct way.
    `table(['table1','table2',...])`
      opens a virtual table as the concatenation of the given tables.
      The tables have to have the same columns.
    `table([tableobject1,tableobject2,...])`
      opens a virtual table as the concatenation of the given table objects.
      The tables have to have the same columns.

    The following arguments can be used.

    `tablename`
      | name of the table to be opened or created. As in most UNIX shells
        a table name can contain environment variables and a tilde with
        optional user name.
      | This argument can be a sequence of names in which case they are
        opened as a (virtual) concatenation of tables.
      | It can also be a sequence of table objects to be concatenated.
    `tabledesc`
      description of table to be created. If given as a dict (which should
      be created by :func:`maketabdesc`, the table is created. Otherwise
      it should exist and is opened.
    `nrow`
      initial number of rows in table to be created (default 0).
    `readonly = True/False`
      tell if a table has to be opened readonly (default) or read/write.
    `lockoptions`
      see below
    `ack=False`
      prohibit the printing of a message telling if the table was
      opened or created successfully.
    `dminfo`
      a dict (as returned by :func:`getdminfo`) giving specific data manager
      info for one or more columns. In this way expert users can
      tell how data are stored (or use virtual data managers).
    `endian`
      | endianness of the data in table to be created
      | 'little' = as little endian
      | 'big'    = as big endian
      | 'local'  = use the endianness of the machine being used
      | 'aipsrc' = use a defined in an .aipsrc file (defaults to local)
    `memorytable=True`
      create table in memory instead of on disk.
    `concatsubtables`
      if tables are concatenated, it should contain a sequence of the
      names of subtables to be concatenated as well (default none).
      Non-mentioned subtables are considered to be identical in each table,
      so only the subtable of the first table is used as subtable for the
      concatenated table.

    Locking/unlocking to share a table in a concurrent environment is
    controlled by the lockoptions argument.

    `auto`
      let the system take care of locking. It locks when needed,
      but unlocking is usually not done automatically.
    `autonoread`
      as `auto`, but no read locking is needed. This must be
      used with care, because it means that reading can be done
      while the table object is not synchronized with the table
      file (as is normally done when a lock is acquired).
      The method :func:`resync` can be used to explicitly synchronize
      the table object with the file.
    `user`
      the user takes care by explicit calls to lock and unlock
    `usernoread`
      as `user` and the no readlocking behaviour of `autonoread`.
    `permanent`
      use a permanent write lock; the constructor fails if the
      lock cannot be acquired because the table is already
      in use in another process
    `permanentwait`
      as above, but wait until the lock is acquired.
    `default`
      this is the default option.
      If the given table is already open, the locking option
      in use is not changed. Otherwise it reverts to `auto`.

    If auto locking is used, it is possible to give a record containing
    the fields option, interval, and/or maxwait (see :func:`lockoptions`
    for their meaning). In this way advanced users can have full control
    over the locking process. In practice this is hardly ever needed.

    For example::

      t = table('3c343.ms')                  # open table readonly
      t = table('3c343.ms', readonly=False)  # open table read/write
      t1= table('new.tab', t.getdesc())      # create table
      t = table([t1,t2,t3,t4])               # concatenate 4 tables

    """

    def __init__(self, tablename, tabledesc=False, nrow=0, readonly=True,
                 lockoptions='default', ack=True, dminfo={}, endian='aipsrc',
                 memorytable=False, concatsubtables=[],
                 _columnnames=[], _datatypes=[],
                 _oper=0, _delete=False):
        """Open or create a table."""
        if _oper == 1:
            # This is the readascii constructor.
            tabname = _remove_prefix(tablename)
            Table.__init__(self, tabname, tabledesc, nrow, readonly,
                           lockoptions, ack, dminfo, endian, memorytable,
                           _columnnames, _datatypes)
        elif _oper == 2:
            # This is the query or calc constructor.
            Table.__init__(self, tablename, tabledesc)
            if len(self._getcalcresult()) != 0:
                # Do not make row object for a calc result
                return
        elif _oper == 3:
            # This is the constructor taking a Table (used by copy).
            Table.__init__(self, tablename)
        else:
            # This is the constructor for a normal table open.
            # It can be done in several forms:
            #  - open single existing table (PlainTable)
            #  - open multiple existing tables (ConcatTable)
            #  - create a new table (PlainTable or MemoryTable)
            #  - concatenate open tables (ConcatTable)
            tabname = _remove_prefix(tablename)
            lockopt = lockoptions
            if isinstance(lockoptions, string_types):
                lockopt = {'option': lockoptions}
            if isinstance(tabledesc, dict):
                # Create a new table.
                memtype = 'plain'
                if (memorytable):
                    memtype = 'memory'
                Table.__init__(self, tabname, lockopt, endian,
                               memtype, nrow, tabledesc, dminfo)
                if ack:
                    six.print_('Successful creation of',
                               lockopt['option'] + '-locked table',
                               tabname + ':',
                               self.ncols(), 'columns,',
                               self.nrows(), 'rows')
            else:
                # Deal with existing tables.
                if not tabname:
                    raise ValueError("No tables or names given")
                # Open an existing table
                opt = 1
                typstr = 'readonly'
                if not readonly:
                    typstr = 'read/write'
                    opt = 5
                    if _delete:
                        opt = 6
                if isinstance(tabname, string_types):
                    Table.__init__(self, tabname, lockopt, opt)
                    if ack:
                        six.print_('Successful', typstr, 'open of',
                                   lockopt['option'] + '-locked table',
                                   tabname + ':',
                                   self.ncols(), 'columns,',
                                   self.nrows(), 'rows')
                elif isinstance(tabname[0], string_types):
                    # Concatenate and open named tables.
                    Table.__init__(self, tabname, concatsubtables,
                                   lockopt, opt)
                    if ack:
                        six.print_('Successful', typstr, 'open of',
                                   lockopt['option'] +
                                   '-locked concatenated tables',
                                   tabname, ':', self.ncols(), 'columns,',
                                   self.nrows(), 'rows')
                else:
                    # Concatenate already open tables.
                    Table.__init__(self, tabname, concatsubtables, 0, 0, 0)
                    if ack:
                        six.print_('Successful virtual concatenation of',
                                   len(tabname), 'tables:', self.ncols(),
                                   'columns,', self.nrows(), 'rows')
        # Create a row object for this table.
        self._makerow()

    def __enter__(self):
        """Function to enter a with block."""
        return self

    def __exit__(self, type, value, traceback):
        """Function to exit a with block which closes the table object."""
        self.close()

    def _makerow(self):
        """Internal method to make its tablerow object."""
        from .tablerow import _tablerow
        self._row = _tablerow(self, [])

    def __str__(self):
        """Return the table name and the basic statistics"""
        return (_add_prefix(self.name()) + "\n%d rows" % self.nrows() +
                "\n" + "%d columns: " % len(self.colnames()) +
                " ".join(self.colnames()))

    def __len__(self):
        """Return the number of rows in the table."""
        return int(self._nrows())

    def __getattr__(self, name):
        """Get the tablecolumn object or keyword value.

        | A tablecolumn object is returned if it names a column.
        | The value of a keyword is returned if it names a keyword.
          If the keyword is a subtable, it opens the table and returns a
          table object.
        | The values of all keywords is returned if name equals _ or keys.

        An AttributeError is raised if the name is column nor keyword.

        For example::

          print t.DATA[i]           # print row i of column DATA
          print t.MS_VERSION        # print the MS version
          print t.keys              # print values of all keywords
          subtab = t.FEED           # open the FEED subtable

        """
        # First try if it is a column.
        try:
            return self.col(name)
        except Exception:
            pass
        # Now try if it is a keyword.
        try:
            val = self.getkeyword(name)
            # See if the keyword represents a subtable and try to open it.
            if val != _do_remove_prefix(val):
                try:
                    return table(val, ack=False)
                except Exception:
                    pass
            return val
        except Exception:
            pass
        # _ or keys means all keywords.
        if name == '_' or name == 'keys':
            return self.getkeywords()
        # Unknown name.
        raise AttributeError("table has no attribute/column/keyword " + name)

    def __getitem__(self, key):
        """Get the values from one or more rows."""
        return self._row._getitem(key, self.nrows())

    def __setitem__(self, key, value):
        """Put value into one or more rows."""
        self._row._setitem(key, value, self.nrows())

    def col(self, columnname):
        """Return a tablecolumn object for the given column.

        If multiple operations need to be done on a column,
        a :class:`tablecolumn` object is somewhat easier to use than the
        table object because the column name does not have to be repeated
        each time.

        It is also possible to use a column name as an attribute, It is an
        easier way to get a column object.

        For example::

          tc = t.col('DATA')
          tc[0:10]       # get first 10 rows of column DATA
          t.DATA[0:10]   # does the same in an easier way

        """
        from .tablecolumn import tablecolumn
        return tablecolumn(self, columnname)

    def row(self, columnnames=[], exclude=False):
        """Return a tablerow object which includes (or excludes) the
        given columns.

        :class:`tablerow` makes it possible to get/put values in one or
        more rows.

        """
        from .tablerow import tablerow
        return tablerow(self, columnnames, exclude)

    def iter(self, columnnames, order='', sort=True):
        """Return a tableiter object.

        :class:`tableiter` lets one iterate over a table by returning in each
        iteration step a reference table containing equal values for the given
        columns.
        By default a sort is done on the given columns to get the correct
        iteration order.

        `order`
          | 'ascending'  is iterate in ascending order (is the default).
          | 'descending' is iterate in descending order.
        `sort=False`
          do not sort (because table is already in correct order).

        For example, iterate by time through a measurementset table::

          t = table('3c343.MS')
          for ts in t.iter('TIME'):
            print ts.nrows()

        """
        from .tableiter import tableiter
        return tableiter(self, columnnames, order, sort)

    def index(self, columnnames, sort=True):
        """Return a tableindex object.

        :class:`tableindex` lets one get the row numbers of the rows holding
        given values for the columns for which the index is created.
        It uses an in-memory index on which a binary search is done.
        By default the table is sorted on the given columns to get the correct
        index order.

        For example::

          t = table('3c343.MS')
          tinx = t.index('ANTENNA1')
          print tinx.rownumbers(0)       # print rownrs containing ANTENNA1=0

        """
        from .tableindex import tableindex
        return tableindex(self, columnnames, sort)

    def flush(self, recursive=False):
        """Flush the table to disk.

        Until a flush or unlock is performed, the results of operations might
        not be stored on disk yet.
        | If `recursive=True`, all subtables are flushed as well.

        """
        self._flush(recursive)

    def resync(self):
        """Resync the table object with the file contents.

        Usually concurrent access is handled by acquiring read and write locks.
        However, a table can be opened without the need for read locking using
        lock option `usernoread` or `autonoread`. in that case
        synchronization of the table object and actual file contents can be
        done manually using this method.

        """
        self._resync()

    def close(self):
        """Flush and close the table which invalidates the table object."""
        self._row = 0
        self._close()

    def done(self):
        """Flush and close the table which invalidates the table object."""
        self.close()

    def toascii(self, asciifile, headerfile='', columnnames=(), sep=' ',
                precision=(), usebrackets=True):
        """Write the table in ASCII format.

        It is approximately the inverse of the from-ASCII-contructor.

        `asciifile`
          The name of the resulting ASCII file.
        `headerfile`
          The name of an optional file containing the header info. If not
          given or if equal to argument `asciifile`, the headers are written
          at the beginning of the ASCII file.
        `columnnames`
          The names of the columns to be written. If not given or if the first
          name is empty, all columns are written.
        `sep`
          The separator to be used between values. Only the first character
          of a string is used. If not given or mepty, a blank is used.
        `precision`
          For each column the precision can be given. It is only used for
          columns containing floating point numbers. A value <=0 means using
          the default which is 9 for single and 18 for double precision.
        `usebrackets`
          If True, arrays and records are written enclosed in [].
          Multi-dimensional arrays have [] per dimension. In this way variable
          shaped array can be read back correctly. However, it is not supported
          by :func:`tablefromascii`.
          If False, records are not written and arrays are written linearly
          with the shape defined in the header as supported byI
          :func:`tablefromascii`.

        Note that columns containing records or variable shaped arrays are
        ignored, because they cannot be written to ASCII. It is told which
        columns are ignored.

        For example::

          t  = table('3c343.MS')
          t1 = t.query('ANTENNA1 != ANTENNA2')   # do row selection
          t1.toascii ('3c343.txt')               # write selection as ASCII

        """
        msg = self._toascii(asciifile, headerfile, columnnames, sep,
                            precision, usebrackets)
        if len(msg) > 0:
            six.print_(msg)

    def rename(self, newtablename):
        """Rename the table.

        It renames the table and, if needed, adjusts the names of its
        subtables.

        """
        self._rename(newtablename)

    def copy(self, newtablename, deep=False, valuecopy=False, dminfo={},
             endian='aipsrc', memorytable=False, copynorows=False):
        """Copy the table and return a table object for the copy.

        It copies all data in the columns and keywords.
        Besides the table, all its subtables are copied too.
        By default a shallow copy is made (usually by copying files).
        It means that the copy of a reference table is also a reference table.
        Use `deep=True` to make a deep copy which turns a reference table
        into a normal table.

        `deep=True`
          a deep copy of a reference table is made.
        `valuecopy=True`
          values are copied, which reorganizes normal tables and removes wasted
          space. It implies `deep=True`. It is slower than a normal copy.
        `dminfo`
          gives the option to specify data managers to change the way columns
          are stored. This is a dict as returned by method :func:`getdminfo`.
        `endian`
          specifies the endianness of the new table when a deep copy is made:
          |  'little' = as little endian
          |  'big'    = as big endian
          |  'local'  = use the endianness of the machine being used
          |  'aipsrc' = use as defined in an .aipsrc file (defaults to local)
        `memorytable=True`
          do not copy to disk, but to a table kept in memory.
        `copynorows=True`
          only copy the column layout and keywords, but no data.

        For example::

          t  = table('3c343.MS')
          t1 = t.query('ANTENNA1 != ANTENNA2')   # do row selection
          t2 = t1.copy ('3c343.sel', True)       # make deep copy
          t2 = t.copy ('new.tab', True, True)    # reorganize storage

        """
        t = self._copy(newtablename, memorytable, deep, valuecopy,
                       endian, dminfo, copynorows)
        # copy returns a Table object, so turn that into table.
        return table(t, _oper=3)

    def copyrows(self, outtable, startrowin=0, startrowout=-1, nrow=-1):
        """Copy the contents of rows from this table to outtable.

        The contents of the columns with matching names are copied.
        The other arguments can be used to specify where to start copying.
        By default the entire input table is appended to the output table.
        Rows are added to the output table if needed.

        `startrowin`
          Row where to start in the input table.
        `startrowout`
          Row where to start in the output table,
          | -1 means write at the end of the output table.
        `nrow`
          Number of rows to copy
          | -1 means from startrowin till the end of the input table

        The following example appends row to the table itself, thus doubles
        the number of rows::

          t:=table('test.ms',readonly=F)
          t.copyrows(t)

        """
        self._copyrows(outtable, startrowin, startrowout, nrow)

    def iswritable(self):
        """Return if the table is writable."""
        return self._iswritable()

    def endianformat(self):
        """Return the endian format ('little' or 'big') in which the table
        is written."""
        return self._endianformat()

    def lock(self, write=True, nattempts=0):
        """Acquire a read or write lock on a table.

        `write=False` means a read lock, otherwise a write lock.
        | nattempts defines the nr of attempts (one attempt per second) to do
        before giving up. The default 0 means unlimited.
        An exception is thrown if no lock could be acquired.

        If the table has already been locked appropriately, nothing will be
        done. Thus locks do NOT nest.

        """
        self._lock(write, nattempts)

    def unlock(self):
        """Unlock the table.

        Flush the table data and release a read or write lock on the table
        acquired by lock().
        Nothing will be done if the table is not locked.

        """
        self._unlock()

    def haslock(self, write=True):
        """Test if the table is read or write locked."""
        return self._haslock(write)

    def lockoptions(self):
        """Return the lockoptions.

        They are returned as a dict with fields:

        'option'
          the locking mode (user, usernoread, auto, autonoread, permanent,
          permanentwait).
        `interval`
          In case of AutoLocking the inspection interval defines how often
          the table system checks if another process needs a lock on the table.
        `maxwait`
          the maximum time to wait when acquiring a lock in AutoLocking mode.

        """
        return self._lockoptions()

    def datachanged(self):
        """Tell if data in the table have changed since the last time
        called."""
        return self._datachanged()

    def ismultiused(self, checksubtables=False):
        """Tell if the table is used in other processes.

        `checksubtables=True` means it will also check it for subtables.

        """
        return self._ismultiused(checksubtables)

    def name(self):
        """Return the table name."""
        return self._name()

    def partnames(self, recursive=False):
        """Return the names of the tables this table consists of.

        A table can be a reference to another table (e.g. for a selection) or
        a concatenation of other tables. This function returns the names of
        such table parts.
        For a plain table it simply returns the name of that table.

        In its turn a table part can be a reference or concatenated table.
        `recursive=True` means that it follows table parts until the end.

        """
        return self._partnames(recursive)

    def info(self):
        """Return the table info (table type, subtype, and readme lines)."""
        return self._info()

    def putinfo(self, value):
        """Put the table info.

        The table info is a dict containing the fields:

        """
        self._putinfo(value)

    def addreadmeline(self, value):
        """Add a readme line to the table info."""
        self._addreadmeline(value)

    def setmaxcachesize(self, columnname, nbytes):
        """Set the maximum cache size for the data manager used by the column.

        It can sometimes be useful to limit the size of the cache used by
        a column stored with the tiled storage manager.
        This method requires some more knowledge about the table system
        and is not meant for the casual user.

        """
        self._setmaxcachesize(columnname, nbytes)

    def rownumbers(self, table=None):
        """Return a list containing the row numbers of this table.

        This method can be useful after a selection or a sort.
        It returns the row numbers of the rows in this table with respect
        to the given table. If no table is given, the original table is used.

        For example::

          t = table('W53.MS')
          t1 = t.selectrows([1,3,5,7,9])  # select a few rows
          t1.rownumbers(t)
          # [1 3 5 7 9]
          t2 = t1.selectrows([2,5])       # select rows from the selection
          t2.rownumbers(t1)
          # [2 5]                         # rownrs of t2 in table t1
          t2.rownumbers(t)
          # [3 9]                         # rownrs of t2 in t
          t2.rownumbers()
          # [3 9]

        The last statements show that the method returns the row numbers
        referring to the given table. Table t2 contains rows 2 and 5 in
        table t1, which are rows 3 and 9 in table t.

        """
        if table is None:
            return self._rownumbers(Table())
        return self._rownumbers(table)

    def colnames(self):
        """Get the names of all columns in the table."""
        return self._colnames()

    def isscalarcol(self, columnname):
        """Tell if the column contains scalar values."""
        return self._isscalarcol(columnname)

    def isvarcol(self, columnname):
        """Tell if the column holds variable shaped arrays."""
        desc = self.getcoldesc(columnname)
        return 'ndim' in desc and 'shape' not in desc

    def coldatatype(self, columnname):
        """Get the data type of a column.

        It returns a string which can have the values:
        ``boolean integer float double complex dcomplex string record``

        """
        return self._coldatatype(columnname)

    def colarraytype(self, columnname):
        """Get the array type of a column holding arrays.

        It tells if an array is fixed or variable shaped and if it is stored
        directly or indirectly. This is done by means of a string like
        ``Indirect, variable sized arrays``

        """
        return self._colarraytype(columnname)

    def ncols(self):
        """Return the number of columns in the table."""
        return self._ncols()

    def nrows(self):
        """Return the number of rows in the table."""
        return int(self._nrows())

    def addrows(self, nrows=1):
        """Add one or more rows to the table."""
        self._addrows(nrows)

    def removerows(self, rownrs):
        """Remove the given rows from the table.

        The row numbers can be given in a sequence in any order. The rows will
        be removed from the end of the table towards the beginning. This is
        needed because the removal of a row decrements the row number of higher
        rows.

        Thus::

          t.removerow ([10,20])

        is different from::

          t.removerow(10)
          t.removerow(20)

        because in the latter row 20 was row 21 before the removal of row 10.

        Some storage managers (in particular the tiled ones) do not allow
        removal of rows, so the operation may fail.

        Rows can always be removed from a reference table. It does NOT remove
        the rows from the referenced table.

        """
        self._removerows(rownrs)

    def getcolshapestring(self, columnname,
                          startrow=0, nrow=-1, rowincr=1):
        """Get the shapes of all cells in the column in string format.

        It returns the shape in a string like [10,20,30].

        If the column contains fixed shape arrays, a single shape is returned.
        Otherwise a list of shape strings is returned.

        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        """
        return self._getcolshapestring(columnname,
                                       startrow, nrow, rowincr,
                                       True)   # reverse axes

    def iscelldefined(self, columnname, rownr):
        """Tell if a column cell contains a value.

        Columns containing variable shaped arrays can be empty. For these cases
        this method returns True. Doing :func:`getcell` on an empty cell
        results in an exception.

        Note that an empty cell is not the same as an empty array. A cell can
        contain an empty array (of any dimensionality) as a value.

        Also note that a cell in a column containing scalars or fixed shaped
        arrays cannot be empty.

        """
        return self._iscelldefined(columnname, rownr)

    def getcell(self, columnname, rownr):
        """Get data from a column cell.

        Get the contents of a cell which can be returned as a scalar value,
        a numpy array, or a dict depending on the contents of the cell.

        """
        return self._getcell(columnname, rownr)

    def getcellnp(self, columnname, rownr, nparray):
        """Get data from a column cell into the given numpy array .

        Get the contents of a cell containing an array into the
        given numpy array. The numpy array has to be C-contiguous
        with a shape matching the shape of the column cell.
        Data type coercion will be done as needed.

        """
        if not nparray.flags.c_contiguous or nparray.size == 0:
            raise ValueError("Argument 'nparray' has to be a contiguous " +
                             "numpy array")
        return self._getcellvh(columnname, rownr, nparray)

    def getcellslice(self, columnname, rownr, blc, trc, inc=[]):
        """Get a slice from a column cell holding an array.

        The columnname and (0-relative) rownr indicate the table cell.

        The slice to get is defined by the blc, trc, and optional inc arguments
        (blc = bottom-left corner, trc=top-right corner, inc=stride). Not all
        axes have to be filled in for blc, trc, and inc. Missing axes default
        to begin, end, and 1. A negative blc or trc defaults to begin or end.
        Note that trc is inclusive (unlike python indexing).

        """
        return self._getcellslice(columnname, rownr,
                                  blc, trc, inc)

    def getcellslicenp(self, columnname, nparray, rownr, blc, trc, inc=[]):
        """Get a slice from a column cell into the given numpy array.

        The columnname and (0-relative) rownr indicate the table cell.

        The numpy array has to be C-contiguous with a shape matching the
        shape of the slice. Data type coercion will be done as needed.

        The slice to get is defined by the blc, trc, and optional inc arguments
        (blc = bottom-left corner, trc=top-right corner, inc=stride). Not all
        axes have to be filled in for blc, trc, and inc. Missing axes default
        to begin, end, and 1. A negative blc or trc defaults to begin or end.
        Note that trc is inclusive (unlike python indexing).

        """
        if not nparray.flags.c_contiguous or nparray.size == 0:
            raise ValueError("Argument 'nparray' has to be a contiguous " +
                             "numpy array")
        return self._getcellslicevh(columnname, rownr,
                                    blc, trc, inc, nparray)

    def getcol(self, columnname, startrow=0, nrow=-1, rowincr=1):
        """Get the contents of a column or part of it.

        It is returned as a numpy array.
        If the column contains arrays, they should all have the same shape.
        An exception is thrown if they differ in shape. In that case the
        method :func:`getvarcol` should be used instead.

        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        """
        #        try:     # trial code to read using a vector of rownrs
        #            nr = len(startrow)
        #            if nrow < 0:
        #                nrow = nr
        #            if nrow == 0:
        #                return numpy.array()
        #            for inx in range(nrow):
        #                i = inx*
        #        except:
        return self._getcol(columnname, startrow, nrow, rowincr)

    def getcolnp(self, columnname, nparray, startrow=0, nrow=-1, rowincr=1):
        """Get the contents of a column or part of it into the given
        numpy array.

        The numpy array has to be C-contiguous with a shape matching the
        shape of the column (part). Data type coercion will be done as needed.

        If the column contains arrays, they should all have the same shape.
        An exception is thrown if they differ in shape. In that case the
        method :func:`getvarcol` should be used instead.

        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        """
        if (not nparray.flags.c_contiguous) or nparray.size == 0:
            raise ValueError("Argument 'nparray' has to be a contiguous " +
                             "numpy array")
        return self._getcolvh(columnname, startrow, nrow, rowincr, nparray)

    def getvarcol(self, columnname, startrow=0, nrow=-1, rowincr=1):
        """Get the contents of a column or part of it.

        It is similar to :func:`getcol`, but the result is returned as a
        dict of numpy arrays.
        It can deal with a column containing variable shaped arrays.

        """
        return self._getvarcol(columnname, startrow, nrow, rowincr)

    def getcolslice(self, columnname, blc, trc, inc=[],
                    startrow=0, nrow=-1, rowincr=1):
        """Get a slice from a table column holding arrays.

        The slice in each array is given by blc, trc, and inc
        (as in getcellslice).
        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        It returns a numpy array where the first axis is formed by the column
        cells. The other axes are the array axes.

        """
        return self._getcolslice(columnname, blc, trc, inc,
                                 startrow, nrow, rowincr)

    def getcolslicenp(self, columnname, nparray, blc, trc, inc=[],
                      startrow=0, nrow=-1, rowincr=1):
        """Get a slice from a table column into the given numpy array.

        The numpy array has to be C-contiguous with a shape matching the
        shape of the column (slice). Data type coercion will be done as needed.

        The slice in each array is given by blc, trc, and inc
        (as in getcellslice).
        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        It returns a numpy array where the first axis is formed by the column
        cells. The other axes are the array axes.

        """
        if not nparray.flags.c_contiguous or nparray.size == 0:
            raise ValueError("Argument 'nparray' has to be a contiguous "
                             + "numpy array")
        return self._getcolslicevh(columnname, blc, trc, inc,
                                   startrow, nrow, rowincr, nparray)

    def putcell(self, columnname, rownr, value):
        """Put a value into one or more table cells.

        The columnname and (0-relative) rownrs indicate the  table cells.
        rownr can be a single row number or a sequence of row numbers.
        If multiple rownrs are given, the given value is put in all those rows.

        The given value has to be convertible to the data type of the column.
        If the column contains scalar values, the given value must be a scalar.
        The value for a column holding arrays can be given as:

        - a scalar resulting in a 1-dim array of 1 element
        - a sequence (list, tuple) resulting in a 1-dim array
        - a numpy array of any dimensionality

        Note that the arrays in a column may have a fixed dimensionality or
        shape. In that case the dimensionality or shape of the array to put
        has to conform.

        """
        self._putcell(columnname, rownr, value)

    def putcellslice(self, columnname, rownr, value, blc, trc, inc=[]):
        """Put into a slice of a table cell holding an array.

        The columnname and (0-relative) rownr indicate the table cell.
        Unlike putcell only a single row can be given.

        The slice to put is defined by the blc, trc, and optional inc
        arguments (blc = bottom-left corner, trc=top-right corner, inc=stride).
        Not all axes have to be filled in for blc, trc, and inc.
        Missing axes default to begin, end, and 1. A negative blc or trc
        defaults to begin or end.
        Note that trc is inclusive (unlike python indexing).

        As in putcell the array can be given by a scalar, sequence, or numpy
        array. The shape of the array to put has to match the slice shape.

        """
        self._putcellslice(columnname, rownr, value,
                           blc, trc, inc)

    def putcol(self, columnname, value, startrow=0, nrow=-1, rowincr=1):
        """Put an entire column or part of it.

        If the column contains scalar values, the given value should be a 1-dim
        array. Otherwise it is a numpy array where the first axis is formed by
        the column cells.

        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        """
        self._putcol(columnname, startrow, nrow, rowincr, value)

    def putvarcol(self, columnname, value, startrow=0, nrow=-1, rowincr=1):
        """Put an entire column or part of it.

        It is similar to putcol, but the shapes of the arrays in the column
        can vary. The value has to be a dict of numpy arrays.

        The column can be sliced by giving a start row (default 0), number of
        rows (default all), and row stride (default 1).

        """
        self._putvarcol(columnname, startrow, nrow, rowincr, value)

    def putcolslice(self, columnname, value, blc, trc, inc=[],
                    startrow=0, nrow=-1, rowincr=1):
        """Put into a slice in a table column holding arrays.

        Its arguments are the same as for getcolslice and putcellslice.

        """
        self._putcolslice(columnname, value, blc, trc, inc,
                          startrow, nrow, rowincr)

    def addcols(self, desc, dminfo={}, addtoparent=True):
        """Add one or more columns.

        Columns can always be added to a normal table.
        They can also be added to a reference table and optionally to its
        parent table.

        `desc`
          contains a description of the column(s) to be added. It can be given
          in three ways:

          - a dict created by :func:`maketabdesc`. In this way multiple
            columns can be added.
          - a dict created by :func:`makescacoldesc`, :func:`makearrcoldesc`,
            or :func:`makecoldesc`. In this way a single column can be added.
          - a dict created by :func:`getcoldesc`. The key 'name' containing
            the column name has to be defined in such a dict.

        `dminfo`
          can be used to provide detailed data manager info to tell how the
          column(s) have to be stored. The dminfo of an existing column can be
          obtained using method :func:`getdminfo`.
        `addtoparent`
          defines if the column should also be added to the parent table in
          case the current table is a reference table (result of selection).
          If True, it will be added to the parent if it does not exist yet.

        For example, add a column using the same data manager type as another
        column::

          coldmi = t.getdminfo('colarrtsm')     # get dminfo of existing column
          coldmi["NAME"] = 'tsm2'               # give it a unique name
          t.addcols (maketabdesc(makearrcoldesc("colarrtsm2",0., ndim=2)),
                     coldmi)

        """
        tdesc = desc
        # Create a tabdesc if only a coldesc is given.
        if 'name' in desc:
            import casacore.tables.tableutil as pt
            if len(desc) == 2 and 'desc' in desc:
                # Given as output from makecoldesc
                tdesc = pt.maketabdesc(desc)
            elif 'valueType' in desc:
                # Given as output of getcoldesc (with a name field added)
                cd = pt.makecoldesc(desc['name'], desc)
                tdesc = pt.maketabdesc(cd)
        self._addcols(tdesc, dminfo, addtoparent)
        self._makerow()

    def renamecol(self, oldname, newname):
        """Rename a single table column.

        Renaming a column in a reference table does NOT rename the column in
        the referenced table.

        """
        self._renamecol(oldname, newname)
        self._makerow()

    def removecols(self, columnnames):
        """Remove one or more columns.

        Note that some storage managers (in particular the tiled ones) do not
        allow the removal of one of its columns. In that case all its columns
        have to be removed together.

        Columns can always be removed from a reference table. It does NOT
        remove the columns from the referenced table.

        """
        self._removecols(columnnames)
        self._makerow()

    def keywordnames(self):
        """Get the names of all table keywords."""
        return self._getfieldnames('', '', -1)

    def colkeywordnames(self, columnname):
        """Get the names of all keywords of a column."""
        return self._getfieldnames(columnname, '', -1)

    def fieldnames(self, keyword=''):
        """Get the names of the fields in a table keyword value.

        The value of a keyword can be a struct (python dict). This method
        returns the names of the fields in that struct.
        Each field in a struct can be a struct in itself. Names of fields in a
        sub-struct can be obtained by giving a keyword name consisting of
        multiple parts separated by dots (e.g. 'key1.sub1.sub2').

        If an empty keyword name is given (which is the default), all table
        keyword names are shown and its behaviour is the same as
        :func:`keywordnames`.

        Instead of a keyword name an index can be given which returns the names
        of the struct value of the i-th keyword.

        """
        if isinstance(keyword, string_types):
            return self._getfieldnames('', keyword, -1)
        else:
            return self._getfieldnames('', '', keyword)

    def colfieldnames(self, columnname, keyword=''):
        """Get the names of the fields in a column keyword value.

        The value of a keyword can be a struct (python dict). This method
        returns the names of the fields in that struct.
        Each field in a struct can be a struct in itself. Names of fields in a
        sub-struct can be obtained by giving a keyword name consisting of
        multiple parts separated by dots (e.g. 'key1.sub1.sub2').

        If an empty keyword name is given (which is the default), all keyword
        names of the column are shown and its behaviour is the same as
        :func:`colkeywordnames`.

        Instead of a keyword name an index can be given which returns the names
        of the struct value of the i-th keyword.

        """
        if isinstance(keyword, string_types):
            return self._getfieldnames(columnname, keyword, -1)
        else:
            return self._getfieldnames(columnname, '', keyword)

    def getkeyword(self, keyword):
        """Get the value of a table keyword.

        The value of a keyword can be a:

        - scalar which is returned as a normal python scalar.
        - an array which is returned as a numpy array.
        - a reference to a table which is returned as a string containing its
          name prefixed by 'Table :'. It can be opened using the normal table
          constructor which will remove the prefix.
        - a struct which is returned as a dict. A struct is fully nestable,
          thus each field in the struct can have one of the values described
          here.

        Similar to method :func:`fieldnames` a keyword name can be given
        consisting of multiple parts separated by dots. This represents
        nested structs, thus gives the value of a field in a struct
        (in a struct, etc.).

        Instead of a keyword name an index can be given which returns the value
        of the i-th keyword.

        """
        if isinstance(keyword, string_types):
            return self._getkeyword('', keyword, -1)
        else:
            return self._getkeyword('', '', keyword)

    def getcolkeyword(self, columnname, keyword):
        """Get the value of a column keyword.

        It is similar to :func:`getkeyword`.

        """
        if isinstance(keyword, string_types):
            return self._getkeyword(columnname, keyword, -1)
        else:
            return self._getkeyword(columnname, '', keyword)

    def getkeywords(self):
        """Get the value of all table keywords.

        It is returned as a dict. See :func:`getkeyword` for the possible
        value types.

        """
        return self._getkeywords('')

    def getcolkeywords(self, columnname):
        """Get the value of all keywords of a column.

        It is returned as a dict. See :func:`getkeyword` for the possible
        value types.

        """
        return self._getkeywords(columnname)

    def getsubtables(self):
        """Get the names of all subtables."""
        keyset = self.getkeywords()
        names = []
        for key, value in keyset.items():
            if isinstance(value, string_types) and value.find('Table: ') == 0:
                names.append(_do_remove_prefix(value))
        return names

    def putkeyword(self, keyword, value, makesubrecord=False):
        """Put the value of a table keyword.

        The value of a keyword can be a:

        - scalar which can be given a normal python scalar or numpy scalar.
        - an array which can be given as a numpy array. A 1-dimensional array
          can also be given as a sequence (tuple or list).
        - a reference to a table which can be given as a table object or as a
          string containing its name prefixed by 'Table :'.
        - a struct which can be given as a dict. A struct is fully nestable,
          thus each field in the dict can be one of the values described here.
          The only exception is that a table value can only be given by the
          string.

        If the keyword already exists, the type of the new value should match
        the existing one (e.g. a scalar cannot be replaced by an array).

        Similar to method :func:`getkeyword` a keyword name can be given
        consisting of multiple parts separated by dots. This represents nested
        structs, thus puts the value into a field in a struct (in a struct,
        etc.).
        If `makesubrecord=True` structs will be created for the keyword name
        parts that do not exist.

        Instead of a keyword name an index can be given which returns the value
        of the i-th keyword.

        """
        val = value
        if isinstance(val, table):
            val = _add_prefix(val.name())
        if isinstance(keyword, string_types):
            return self._putkeyword('', keyword, -1, makesubrecord, val)
        else:
            return self._putkeyword('', '', keyword, makesubrecord, val)

    def putcolkeyword(self, columnname, keyword, value, makesubrecord=False):
        """Put the value of a column keyword.

        It is similar to :func:`putkeyword`.

        """
        val = value
        if isinstance(val, table):
            val = _add_prefix(val.name())
        if isinstance(keyword, string_types):
            return self._putkeyword(columnname, keyword, -1,
                                    makesubrecord, val)
        else:
            return self._putkeyword(columnname, '', keyword,
                                    makesubrecord, val)

    def putkeywords(self, value):
        """Put the value of multiple table keywords.

        The value has to be a dict, so each field in the dict is a keyword.
        It puts all keywords similar to :func:`putkeyword`.

        """
        return self._putkeywords('', value)

    def putcolkeywords(self, columnname, value):
        """Put the value of multiple keywords in a column.

        The value has to be a dict, so each field in the dict is a keyword.
        It puts all keywords similar to :func:`putkeyword`.

        """
        return self._putkeywords(columnname, value)

    def removekeyword(self, keyword):
        """Remove a table keyword.

        Similar to :func:`getkeyword` the name can consist of multiple parts.
        In that case a field in a struct will be removed.

        Instead of a keyword name an index can be given which removes
        the i-th keyword.

        """
        if isinstance(keyword, string_types):
            self._removekeyword('', keyword, -1)
        else:
            self._removekeyword('', '', keyword)

    def removecolkeyword(self, columnname, keyword):
        """Remove a column keyword.

        It is similar to :func:`removekeyword`.

        """
        if isinstance(keyword, string_types):
            self._removekeyword(columnname, keyword, -1)
        else:
            self._removekeyword(columnname, '', keyword)

    def getdesc(self, actual=True):
        """Get the table description.

        By default it returns the actual description (thus telling the
        actual array shapes and data managers used).
        `actual=False` means that the original description as made by
        :func:`maketabdesc` is returned.
        """

        tabledesc = self._getdesc(actual, True)

        # Strip out 0 length "HCcoordnames" and "HCidnames"
        # as these aren't valid. (See tabledefinehypercolumn)
        hcdefs = tabledesc.get('_define_hypercolumn_', {})

        for c, hcdef in six.iteritems(hcdefs):
            if "HCcoordnames" in hcdef and len(hcdef["HCcoordnames"]) == 0:
                del hcdef["HCcoordnames"]
            if "HCidnames" in hcdef and len(hcdef["HCidnames"]) == 0:
                del hcdef["HCidnames"]

        return tabledesc

    def getcoldesc(self, columnname, actual=True):
        """Get the description of a column.

        By default it returns the actual description (thus telling the
        actual array shapes and data managers used).
        `actual=False` means that the original description as made by
        :func:`makescacoldesc` or :func:`makearrcoldesc` is returned.

        """
        return self._getcoldesc(columnname, actual, True)

    def coldesc(self, columnname, actual=True):
        """Make the description of a column.

        Make the description object of the given column as
        :func:`makecoldesc` is doing with the description given by
        :func:`getcoldesc`.

        """
        import casacore.tables.tableutil as pt
        return pt.makecoldesc(columnname, self.getcoldesc(columnname, actual))

    def getdminfo(self, columnname=None):
        """Get data manager info.

        Each column in a table is stored using a data manager. A storage
        manager is a data manager storing the physically in a file.
        A virtual column engine is a data manager that does not store data
        but calculates it on the fly (e.g. scaling floats to short to
        reduce storage needs).

        By default this method returns a dict telling the data managers used.
        Each field in the dict is a dict containing:

        - NAME telling the (unique) name of the data manager
        - TYPE telling the type of data manager (e.g. TiledShapeStMan)
        - SEQNR telling the sequence number of the data manager
          (is ''i'' in table.f<i> for storage managers)
        - SPEC is a dict holding the data manager specification
        - COLUMNS is a list giving the columns stored by this data manager

        When giving a column name the data manager info of that particular
        column is returned (without the COLUMNS field).
        It can, for instance, be used when adding a column using
        :func:`addcols` that should use the same data manager type as an
        existing column. However, when doing that care should be taken to
        change the NAME because each data manager name has to be unique.

        """
        dminfo = self._getdminfo()
        if columnname is None:
            return dminfo
        # Find the info for the given column
        for fld in dminfo.values():
            if columnname in fld["COLUMNS"]:
                fldc = fld.copy()
                del fldc['COLUMNS']  # remove COLUMNS field
                return fldc
        raise KeyError("Column " + columnname + " does not exist")

    def getdmprop(self, name, bycolumn=True):
        """Get properties of a data manager.

        Each column in a table is stored using a data manager. A storage
        manager is a data manager storing the physically in a file.
        A virtual column engine is a data manager that does not store data
        but calculates it on the fly (e.g. scaling floats to short to
        reduce storage needs).

        Some data managers have properties that can be changed on the fly
        (e.g. cachesize for a tiled storage manager). The properties of
        a given data manager are returned as a dict; function :func:`setdmprop`
        can be used to change the properties. Note the properties are also part
        of the data manager info returned by :func:`getdminfo`.

        The data manager can be specified in two ways: by data manager name
        or by the name of a column using the data manager. The argument
        `bycolumn` defines which way is used (default is by column name).

        """
        return self._getdmprop(name, bycolumn)

    def setdmprop(self, name, properties, bycolumn=True):
        """Set properties of a data manager.

        Properties (e.g. cachesize) of a data manager can be changed by
        defining them appropriately in the properties argument (a dict).
        Current values can be obtained using function :func:`getdmprop` which
        also serves as a template. The dict can contain more fields; only
        the fields with the names as returned by getdmprop are handled.

        The data manager can be specified in two ways: by data manager name
        or by the name of a column using the data manager. The argument
        `bycolumn` defines which way is used (default is by column name).

        """
        return self._setdmprop(name, properties, bycolumn)

    def showstructure(self, dataman=True, column=True, subtable=False,
                      sort=False):
        """Show table structure in a formatted string.

        The structure of this table and optionally its subtables is shown.
        It shows the data manager info and column descriptions.
        Optionally the columns are sorted in alphabetical order.

        `dataman`
          Show data manager info? If False, only column info is shown.
          If True, data manager info and columns per data manager are shown.
        `column`
          Show column description per data manager? Only takes effect if
          dataman=True.
        `subtable`
          Show the structure of all subtables (recursively).
          The names of subtables are always shown.
        'sort'
          Sort the columns in alphabetical order?

        """
        return self._showstructure(dataman, column, subtable, sort)

    def summary(self, recurse=False):
        """Print a summary of the table.

        It prints the number of columns and rows, column names, and table and
        column keywords.
        If `recurse=True` it also prints the summary of all subtables, i.e.
        tables referenced by table keywords.

        """
        six.print_('Table summary:', self.name())
        six.print_('Shape:', self.ncols(), 'columns by', self.nrows(), 'rows')
        six.print_('Info:', self.info())
        tkeys = self.getkeywords()
        if (len(tkeys) > 0):
            six.print_('Table keywords:', tkeys)
        columns = self.colnames()
        if (len(columns) > 0):
            six.print_('Columns:', columns)
            for column in columns:
                ckeys = self.getcolkeywords(column)
                if (len(ckeys) > 0):
                    six.print_(column, 'keywords:', ckeys)
        if (recurse):
            for key, value in tkeys.items():
                tabname = _remove_prefix(value)
                six.print_('Summarizing subtable:', tabname)
                lt = table(tabname)
                if (not lt.summary(recurse)):
                    break
        return True

    def selectrows(self, rownrs):
        """Return a reference table containing the given rows."""
        t = self._selectrows(rownrs, name='')
        # selectrows returns a Table object, so turn that into table.
        return table(t, _oper=3)

    def query(self, query='', name='', sortlist='', columns='',
              limit=0, offset=0, style='Python'):
        """Query the table and return the result as a reference table.

        This method queries the table. It forms a
        `TaQL <../../doc/199.html>`_
        command from the given arguments and executes it using the
        :func:`taql` function.
        The result is returned in a so-called reference table which
        references the selected columns and rows in the original table.
        Usually a reference table is temporary, but it can be made
        persistent by giving it a name.
        Note that a reference table is handled as any table, thus can be
        queried again.

        All arguments are optional, but at least one of `query`, `name`,
        `sortlist`, and `columns` should be used.
        See the `TaQL note <../../doc/199.html>`_ for the
        detailed description of the the arguments representing the various
        parts of a TaQL command.

        `query`
          The WHERE part of a TaQL command.
        `name`
          The name of the reference table if it is to be made persistent.
        `sortlist`
          The ORDERBY part of a TaQL command. It is a single string in which
          commas have to be used to separate sort keys.
        `columns`
          The columns to be selected (projection in data base terms). It is a
          single string in which commas have to be used to separate column
          names. Apart from column names, expressions can be given as well.
        `limit`
          If > 0, maximum number of rows to be selected.
        `offset`
          If > 0, ignore the first N matches.
        `style`
          The TaQL syntax style to be used (defaults to Python).

        """
        if not query and not sortlist and not columns and \
           limit <= 0 and offset <= 0:
            raise ValueError('No selection done (arguments query, ' +
                             'sortlist, columns, limit, and offset are empty)')
        command = 'select '
        if columns:
            command += columns
        command += ' from $1'
        if query:
            command += ' where ' + query
        if sortlist:
            command += ' orderby ' + sortlist
        if limit > 0:
            command += ' limit %d' % limit
        if offset > 0:
            command += ' offset %d' % offset
        if name:
            command += ' giving ' + name
        return tablecommand(command, style, [self])

    def sort(self, sortlist, name='',
             limit=0, offset=0, style='Python'):
        """Sort the table and return the result as a reference table.

        This method sorts the table. It forms a
        `TaQL <../../doc/199.html>`_
        command from the given arguments and executes it using the
        :func:`taql` function.
        The result is returned in a so-called reference table which references
        the columns and rows in the original table. Usually a reference
        table is temporary, but it can be made persistent by giving it a name.
        Note that a reference table is handled as any table, thus can be
        queried again.

        `sortlist`
          The ORDERBY part of a TaQL command. It is a single string in which
          commas have to be used to separate sort keys. A sort key can be the
          name of a column, but it can be an expression as well.
        `name`
          The name of the reference table if it is to be made persistent.
        `limit`
          If > 0, maximum number of rows to be selected after the sort step.
          It can, for instance, be used to select the N highest values.
        `offset`
          If > 0, ignore the first `offset` matches after the sort step.
        `style`
          The TaQL syntax style to be used (defaults to Python).

        """
        command = 'select from $1 orderby ' + sortlist
        if limit > 0:
            command += ' limit %d' % limit
        if offset > 0:
            command += ' offset %d' % offset
        if name:
            command += ' giving ' + name
        return tablecommand(command, style, [self])

    def select(self, columns, name='', style='Python'):
        """Select columns and return the result as a reference table.

        This method represents the SELECT part of a TaQL command using the
        given columns (or column expressions). It forms a
        `TaQL <../../doc/199.html>`_
        command from the given arguments and executes it using the
        :func:`taql` function.
        The result is returned in a so-called reference table which references
        the columns and rows in the original table. Usually a reference
        table is temporary, but it can be made persistent by giving it a name.
        Note that a reference table is handled as any table, thus can be
        queried again.

        `columns`
          The columns to be selected (projection in data base terms). It is a
          single string in which commas have to be used to separate column
          names. Apart from column names, expressions can be given as well.
        `name`
          The name of the reference table if it is to be made persistent.
        `style`
          The TaQL syntax style to be used (defaults to Python).

        """
        command = 'select ' + columns + ' from $1'
        if name:
            command += ' giving ' + name
        return tablecommand(command, style, [self])

    def calc(self, expr, style='Python'):
        """Do a TaQL calculation

        The TaQL CALC command can be used to get the result of a calculation on
        table data. It is, however, also possible to use it without table data.

        For instance, to use it for converting units::

          t = table('',{})
          t.calc ('(1 \\in)cm')

        `expr`
          The CALC expression
        `style`
          The TaQL syntax style to be used (defaults to Python).

        """
        return tablecommand('calc from $1 calc ' + expr, style, [self])

    def browse(self, wait=True, tempname="/tmp/seltable"):
        """ Browse a table using casabrowser or a simple wxwidget
        based browser.

        By default the casabrowser is used if it can be found (in your PATH).
        Otherwise the wxwidget one is used if wx can be loaded.

        The casabrowser can only browse tables that are persistent on disk.
        This gives problems for tables resulting from a query because they are
        held in memory only (unless an output table name was given).

        To make browsing of such tables possible, the argument `tempname` can
        be used to specify a table name that will be used to form a persistent
        table that can be browsed. Note that such a table is very small as it
        does not contain data, but only references to rows in the original
        table.
        The default for `tempname` is '/tmp/seltable'.

        If needed, the table can be deleted using the :func:`tabledelete`
        function.

        If `wait=False`, the casabrowser is started in the background.
        In that case the user should delete a possibly created copy of a
        temporary table.

        """
        import os
        # Test if casabrowser can be found.
        # On OS-X 'which' always returns 0, so use test on top of it.
        # Nothing is written on stdout if not found.
        if os.system('test `which casabrowser`x != x') == 0:
            waitstr1 = ""
            waitstr2 = "foreground ..."
            if not wait:
                waitstr1 = " &"
                waitstr2 = "background ..."
            if self.iswritable():
                six.print_("Flushing data and starting casabrowser in the " +
                           waitstr2)
            else:
                six.print_("Starting casabrowser in the " + waitstr2)
            self.flush()
            self.unlock()
            if os.system('test -e ' + self.name() + '/table.dat') == 0:
                os.system('casabrowser ' + self.name() + waitstr1)
            elif len(tempname) > 0:
                six.print_("  making a persistent copy in table " + tempname)
                self.copy(tempname)
                os.system('casabrowser ' + tempname + waitstr1)
                if wait:
                    from casacore.tables import tabledelete
                    six.print_("  finished browsing")
                    tabledelete(tempname)

                else:
                    six.print_(" after browsing use tabledelete('" + tempname +
                               "') to delete the copy")
            else:
                six.print_("Cannot browse because the table is in memory only")
                six.print_("You can browse a (shallow) persistent copy " +
                           "of the table like: ")
                six.print_("   t.browse(True, '/tmp/tab1')")
        else:
            try:
                import wxPython
            except ImportError:
                six.print_('casabrowser nor wxPython can be found')
                return
            from wxPython.wx import wxPySimpleApp
            import sys
            app = wxPySimpleApp()
            from wxtablebrowser import CasaTestFrame
            frame = CasaTestFrame(None, sys.stdout, self)
            frame.Show(True)
            app.MainLoop()

    def view(self, wait=True, tempname="/tmp/seltable"):
        """ View a table using casaviewer, casabrowser, or wxwidget
        based browser.

        The table is viewed depending on the type:

        MeasurementSet
          is viewed using casaviewer.
        Image
          is viewed using casaviewer.
        other
          are browsed using the :func:`browse` function.

        If the casaviewer cannot be found, all tables are browsed.

        The casaviewer can only display tables that are persistent on disk.
        This gives problems for tables resulting from a query because they are
        held in memory only (unless an output table name was given).

        To make viewing of such tables possible, the argument `tempname` can
        be used to specify a table name that will be used to form a persistent
        table that can be browsed. Note that such a table is very small as it
        does not contain data, but only references to rows in the original
        table. The default for `tempname` is '/tmp/seltable'.

        If needed, the table can be deleted using the :func:`tabledelete`
        function.

        If `wait=False`, the casaviewer is started in the background.
        In that case the user should delete a possibly created copy of a
        temporary table.

        """
        import os
        # Determine the table type.
        # Test if casaviewer can be found.
        # On OS-X 'which' always returns 0, so use test on top of it.
        viewed = False
        type = self.info()["type"]
        if type == "Measurement Set" or type == "Image":
            if os.system('test -x `which casaviewer` > /dev/null 2>&1') == 0:
                waitstr1 = ""
                waitstr2 = "foreground ..."
                if not wait:
                    waitstr1 = " &"
                    waitstr2 = "background ..."
                if self.iswritable():
                    six.print_("Flushing data and starting casaviewer " +
                               "in the " + waitstr2)
                else:
                    six.print_("Starting casaviewer in the " + waitstr2)
                self.flush()
                self.unlock()
                if os.system('test -e ' + self.name() + '/table.dat') == 0:
                    os.system('casaviewer ' + self.name() + waitstr1)
                    viewed = True
                elif len(tempname) > 0:
                    six.print_("  making a persistent copy in table " +
                               tempname)
                    self.copy(tempname)
                    os.system('casaviewer ' + tempname + waitstr1)
                    viewed = True
                    if wait:
                        from casacore.tables import tabledelete
                        six.print_("  finished viewing")
                        tabledelete(tempname)
                    else:
                        six.print_("  after viewing use tabledelete('" +
                                   tempname + "') to delete the copy")
                else:
                    six.print_("Cannot browse because the table is " +
                               "in memory only.")
                    six.print_("You can browse a (shallow) persistent " +
                               "copy of the table like:")
                    six.print_("   t.view(True, '/tmp/tab1')")
        # Could not view the table, so browse it.
        if not viewed:
            self.browse(wait, tempname)

    def _repr_html_(self):
        """Give a nice representation of tables in notebooks."""
        out = "<table class='taqltable' style='overflow-x:auto'>\n"

        # Print column names (not if they are all auto-generated)
        if not(all([colname[:4] == "Col_" for colname in self.colnames()])):
            out += "<tr>"
            for colname in self.colnames():
                out += "<th><b>"+colname+"</b></th>"
            out += "</tr>"

        cropped = False
        rowcount = 0
        for row in self:
            rowout = _format_row(row, self.colnames(), self)
            rowcount += 1
            out += rowout
            if "\n" in rowout:  # Double space after multiline rows
                out += "\n"
            out += "\n"
            if rowcount >= 20:
                cropped = True
                break

        if out[-2:] == "\n\n":
            out = out[:-1]

        out += "</table>"

        if cropped:
            out += ("<p style='text-align:center'>(" +
                    str(self.nrows()-20)+" more rows)</p>\n")

        return out
