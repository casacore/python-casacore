====================
Module :mod:`tables`
====================

.. automodule:: casacore.tables

Table utility functions
-----------------------
:func:`default_ms`
  Create a default MS.
:func:`default_ms_subtable`
  Create a default MS subtable.
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
:func:`makecoldesc`
  Create description of any column
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

MeasurementSet utility functions
--------------------------------
:func:`addImagingColumns`
  Add MeasurementSet columns needed for the CASA imager
:func:`removeImagingColumns`
  Remove CASA imager columns CORRECTED_DATA, MODEL_DATA, and
  IMAGING_WEIGHT
:func:`addDerivedMSCal`
  Add the DerivedMSCal virtual columns like PA1, HA1 to a MeasurementSet
:func:`removeDerivedMSCal`
  Remove the DerivedMSCal virtual columns like PA1, HA1 from a MeasurementSet
:func:`msconcat`
  Concatenate spectral windows in different MSs to a single MS (in a virtual way)
:func:`required_ms_desc`
  Obtained the table descriptor describing a basic MS or an MS subtable.
:func:`complete_ms_desc`
  Obtain the table descriptor describing a complete MS or MS subtable.

Utility functions details
-------------------------
.. autofunction:: casacore.tables.taql
.. autofunction:: casacore.tables.tablefromascii
.. autofunction:: casacore.tables.maketabdesc
.. autofunction:: casacore.tables.makedminfo
.. autofunction:: casacore.tables.makescacoldesc
.. autofunction:: casacore.tables.makearrcoldesc
.. autofunction:: casacore.tables.makecoldesc
.. autofunction:: casacore.tables.tabledefinehypercolumn
.. autofunction:: casacore.tables.tableexists
.. autofunction:: casacore.tables.tableiswritable
.. autofunction:: casacore.tables.tablecopy
.. autofunction:: casacore.tables.tabledelete
.. autofunction:: casacore.tables.tablerename
.. autofunction:: casacore.tables.tableinfo
.. autofunction:: casacore.tables.tablesummary
.. autofunction:: casacore.tables.addImagingColumns
.. autofunction:: casacore.tables.removeImagingColumns
.. autofunction:: casacore.tables.addDerivedMSCal
.. autofunction:: casacore.tables.removeDerivedMSCal
.. autofunction:: casacore.tables.msconcat

Class :class:`tables.table`
---------------------------
.. autoclass:: casacore.tables.table
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tablecolumn`
---------------------------------
.. autoclass:: casacore.tables.tablecolumn
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tablerow`
------------------------------
.. autoclass:: casacore.tables.tablerow
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tableiter`
-------------------------------
.. autoclass:: casacore.tables.tableiter
   :members:
   :undoc-members:
   :inherited-members:

Class :class:`tables.tableindex`
--------------------------------
.. autoclass:: casacore.tables.tableindex
   :members:
   :undoc-members:
   :inherited-members:

.. automodule:: casacore.tables.tableutil
.. automodule:: casacore.tables.msutil
