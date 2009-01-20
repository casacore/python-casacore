====================
Module :mod:`tables`
====================

.. automodule:: pyrap.tables

Utility functions
-----------------
:func:`taql` or `tablecommand()`
  Execute TaQL query command
:func:`tablefromascii`
  Create table from ASCII file
:func:`maketabdesc` or `tablecreatedesc`
  Create table description
:func:`makescacoldesc` or `tablecreatescalarcoldesc`
  Create description of column holding scalars
:func:`makearrcoldesc` or `tablecreatearraycoldesc`
  Create description of column holding arrays
:func:`tabledefinehypercolumn`
  Advanced definition of hypercolumn for tiled storage managers
:func:`tableexists`
  Test if a table exists
:func:`tableiswritable`
  Test if a table is writable
:func:`tablecopy`
  Copy a table
:func:`tabledelete`
  Delete a table
:func:`tablerename`
  Rename a table
:func:`tableinfo`
  Get the type info of a table
:func:`tablesummary`
  Get a summary of the table

.. autofunction:: pyrap.tables.taql
.. autofunction:: pyrap.tables.tablefromascii
.. autofunction:: pyrap.tables.maketabdesc
.. autofunction:: pyrap.tables.makescacoldesc
.. autofunction:: pyrap.tables.makearrcoldesc
.. autofunction:: pyrap.tables.tabledefinehypercolumn
.. autofunction:: pyrap.tables.tableexists
.. autofunction:: pyrap.tables.tableiswritable
.. autofunction:: pyrap.tables.tablecopy
.. autofunction:: pyrap.tables.tabledelete
.. autofunction:: pyrap.tables.tablerename
.. autofunction:: pyrap.tables.tableinfo
.. autofunction:: pyrap.tables.tablesummary

Class :class:`tables.table`
---------------------------
.. autoclass:: pyrap.tables.table
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tablecolumn`
---------------------------------
.. autoclass:: pyrap.tables.tablecolumn
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tablerow`
------------------------------
.. autoclass:: pyrap.tables.tablerow
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tableiter`
-------------------------------
.. autoclass:: pyrap.tables.tableiter
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tableindex`
--------------------------------
.. autoclass:: pyrap.tables.tableindex
   :members:
   :undoc-members:
   :inherited-members:

.. automodule:: pyrap.tables.tableutil
