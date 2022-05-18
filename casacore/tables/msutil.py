# msutil.py: Utility MeasurementSet functions
# Copyright (C) 2011
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
from six import string_types
import numpy as np
import six
from casacore.tables.table import (table, taql,
                                   _required_ms_desc,
                                   _complete_ms_desc)
from casacore.tables.tableutil import (makescacoldesc, makearrcoldesc,
                                       makecoldesc, maketabdesc)


def required_ms_desc(table=None):
    """
    Obtain the required table description for a given table.

    If "" or "MAIN", the description for a MeasurementSet is returned.
    Otherwise, a the description for a MeasurementSet subtable is returned.
    """
    # Default to MAIN table
    if table is None:
        table = ""

    return _required_ms_desc(table)


def complete_ms_desc(table=None):
    """
    Obtain the complete table description for a given table.

    If "" or "MAIN", the description for a MeasurementSet is returned.
    Otherwise, a the description for a MeasurementSet subtable is returned.
    """
    # Default to MAIN table
    if table is None:
        table = ""

    return _complete_ms_desc(table)


def addImagingColumns(msname, ack=True):
    """ Add the columns to an MS needed for the casa imager.

    It adds the columns MODEL_DATA, CORRECTED_DATA, and IMAGING_WEIGHT.
    It also sets the CHANNEL_SELECTION keyword needed for the older casa
    imagers.

    A column is not added if already existing.
    """
    # numpy is needed
    import numpy as np
    # Open the MS
    t = table(msname, readonly=False, ack=False)
    cnames = t.colnames()
    # Get the description of the DATA column.
    try:
        cdesc = t.getcoldesc('DATA')
    except:
        raise ValueError('Column DATA does not exist')
    # Determine if the DATA storage specification is tiled.
    hasTiled = False
    try:
        dminfo = t.getdminfo("DATA")
        if dminfo['TYPE'][:5] == 'Tiled':
            hasTiled = True
    except:
        hasTiled = False
    # Use TiledShapeStMan if needed.
    if not hasTiled:
        dminfo = {'TYPE': 'TiledShapeStMan',
                  'SPEC': {'DEFAULTTILESHAPE': [4, 32, 128]}}
    # Add the columns(if not existing). Use the description of the DATA column.
    if 'MODEL_DATA' in cnames:
        six.print_("Column MODEL_DATA not added; it already exists")
    else:
        dminfo['NAME'] = 'modeldata'
        cdesc['comment'] = 'The model data column'
        t.addcols(maketabdesc(makecoldesc('MODEL_DATA', cdesc)), dminfo)
        if ack:
            six.print_("added column MODEL_DATA")
    if 'CORRECTED_DATA' in cnames:
        six.print_("Column CORRECTED_DATA not added; it already exists")
    else:
        dminfo['NAME'] = 'correcteddata'
        cdesc['comment'] = 'The corrected data column'
        t.addcols(maketabdesc(makecoldesc('CORRECTED_DATA', cdesc)), dminfo)
        if ack:
            six.print_("'added column CORRECTED_DATA")
    if 'IMAGING_WEIGHT' in cnames:
        six.print_("Column IMAGING_WEIGHT not added; it already exists")
    else:
        # Add IMAGING_WEIGHT which is 1-dim and has type float.
        # It needs a shape, otherwise the CASA imager complains.
        shp = []
        if 'shape' in cdesc:
            shp = cdesc['shape']
        if len(shp) > 0:
            shp = [shp[0]]  # use nchan from shape
        else:
            shp = [t.getcell('DATA', 0).shape[0]]  # use nchan from actual data
        cd = makearrcoldesc('IMAGING_WEIGHT', 0, ndim=1, shape=shp,
                            valuetype='float')
        dminfo = {'TYPE': 'TiledShapeStMan',
                  'SPEC': {'DEFAULTTILESHAPE': [32, 128]}}
        dminfo['NAME'] = 'imagingweight'
        t.addcols(maketabdesc(cd), dminfo)
        if ack:
            six.print_("added column IMAGING_WEIGHT")
    # Add or overwrite keyword CHANNEL_SELECTION.
    if 'CHANNEL_SELECTION' in t.colkeywordnames('MODEL_DATA'):
        t.removecolkeyword('MODEL_DATA', 'CHANNEL_SELECTION')
    # Define the CHANNEL_SELECTION keyword containing the channels of
    # all spectral windows.
    tspw = table(t.getkeyword('SPECTRAL_WINDOW'), ack=False)
    nchans = tspw.getcol('NUM_CHAN')
    chans = [[0, nch] for nch in nchans]
    t.putcolkeyword('MODEL_DATA', 'CHANNEL_SELECTION', np.int32(chans))
    if ack:
        six.print_("defined keyword CHANNEL_SELECTION in column MODEL_DATA")
    # Flush the table to make sure it is written.
    t.flush()


def removeImagingColumns(msname):
    # Open the MS
    t = table(msname, readonly=False, ack=False)
    # Remove if the column exists.
    cnames = t.colnames()
    removeNames = []
    for col in ['MODEL_DATA', 'CORRECTED_DATA', 'IMAGING_WEIGHT']:
        if col in cnames:
            removeNames.append(col)
    if len(removeNames) > 0:
        t.removecols(removeNames)
        t.flush()


def addDerivedMSCal(msname):
    """ Add the derived columns like HA to an MS or CalTable.

    It adds the columns HA, HA1, HA2, PA1, PA2, LAST, LAST1, LAST2, AZEL1,
    AZEL2, and UVW_J2000.
    They are all bound to the DerivedMSCal virtual data manager.

    It fails if one of the columns already exists.

    """

    # Open the MS
    t = table(msname, readonly=False, ack=False)
    colnames = t.colnames()
    # Check that the columns needed by DerivedMSCal are present.
    # Note that ANTENNA2 and FEED2 are not required.
    for col in ["TIME", "ANTENNA1", "FIELD_ID", "FEED1"]:
        if col not in colnames:
            raise ValueError("Columns " + colnames +
                             " should be present in table " + msname)
    scols1 = ['HA', 'HA1', 'HA2', 'PA1', 'PA2']
    scols2 = ['LAST', 'LAST1', 'LAST2']
    acols1 = ['AZEL1', 'AZEL2']
    acols2 = ['UVW_J2000']
    descs = []
    # Define the columns and their units.
    for col in scols1:
        descs.append(makescacoldesc(col, 0.,
                                    keywords={"QuantumUnits": ["rad"]}))
    for col in scols2:
        descs.append(makescacoldesc(col, 0.,
                                    keywords={"QuantumUnits": ["d"]}))
    for col in acols1:
        descs.append(makearrcoldesc(col, 0.,
                                    keywords={"QuantumUnits": ["rad", "rad"]}))
    for col in acols2:
        descs.append(makearrcoldesc(col, 0.,
                                    keywords={"QuantumUnits": ["m", "m", "m"],
                                              "MEASINFO": {"Ref": "J2000",
                                                           "type": "uvw"}}))
    # Add all columns using DerivedMSCal as data manager.
    dminfo = {"TYPE": "DerivedMSCal", "NAME": "", "SPEC": {}}
    t.addcols(maketabdesc(descs), dminfo)
    # Flush the table to make sure it is written.
    t.flush()


def removeDerivedMSCal(msname):
    """ Remove the derived columns like HA from an MS or CalTable.

    It removes the columns using the data manager DerivedMSCal.
    Such columns are HA, HA1, HA2, PA1, PA2, LAST, LAST1, LAST2, AZEL1,
    AZEL2, and UVW_J2000.

    It fails if one of the columns already exists.

    """

    # Open the MS
    t = table(msname, readonly=False, ack=False)
    # Remove the columns stored as DerivedMSCal.
    dmi = t.getdminfo()
    for x in dmi.values():
        if x['TYPE'] == 'DerivedMSCal':
            t.removecols(x['COLUMNS'])
    t.flush()


def msconcat(names, newname, concatTime=False):
    """Virtually concatenate multiple MeasurementSets.

    Multiple MeasurementSets are concatenated into a single MeasurementSet.
    The concatenation is done in an entirely or almost entirely virtual way,
    so hardly any data are copied. It makes the command very fast and hardly
    any extra disk space is needed.

    The MSs can be concatenated in time or frequency (spectral windows).
    If concatenated in time, no indices need to be updated and the
    concatenation is done in a single step.

    If spectral windows are concatenated, the data-description-ids and
    spectral-window-ids in the resulting MS and its subtables are updated
    to make them unique.
    The spectral concatenation is done in two steps and results in two MSs:

    1. The input MSs are virtually concatenated resulting in the
       MeasurementSet `<newname>_CONCAT`.
    2. The MeasurementSet <newname> is created. It references all columns
       in `<newname>_CONCAT` with the exception of the DATA_DESC_ID column.
       This column is copied and updated to make the ids correct.
       Furthermore the MS contains a copy of all subtables (with the exception
       of SORTED_TABLE), where the DATA_DESCRIPTION and SPECTRAL_WINDOW
       subtables are the concatenation of those subtables in the input MSs.
       The ids in the resulting subtables are updated.

    The FEED, FREQ_OFFSET, SOURCE, and SYSCAL subtables also have a
    SPECTRAL_WINDOW_ID column. Currently these subtables are not concatenated
    nor are their ids updated.

    `names`
      A sequence containing the names of the MeasurementSets to concatenate.
    `newname`
      The name of the resulting MeasurementSet. A MeasurementSet with this
      name followed by `_CONCAT` will also be created (and must be kept).
    `concatTime`
      False means that the spectral windows ids will be adjusted as explained
      above.

    """

    if len(names) == 0:
        raise ValueError('No input MSs given')
    # Concatenation in time is straightforward.
    if concatTime:
        t = table(names[0])
        if 'SYSCAL' in t.fieldnames():
            tn = table(names, concatsubtables='SYSCAL')
        else:
            tn = table(names)
        t.close()
        tn.rename(newname)
        return
    # First concatenate the given tables as another table.
    # The SPECTRAL_WINDOW and DATA_DESCRIPTION subtables are concatenated
    # and changed later.
    # Those subtables cannot be concatenated here, because the deep copy of
    # them fails due to the rename of the main table.
    tn = table(names)
    tdesc = tn.getdesc()
    tn.rename(newname + '_CONCAT')
    tn.flush()
    # Now create a table where all columns forward to the concatenated table,
    # but create a stored column for the data description id, because it has
    # to be changed.
    # The new column is filled at the end.
    tnew = table(newname, tdesc, nrow=tn.nrows(), dminfo={
        '1': {'TYPE': 'ForwardColumnEngine',
              'NAME': 'ForwardData',
              'COLUMNS': tn.colnames(),
              'SPEC': {'FORWARDTABLE': tn.name()}}})
    # Remove the DATA_DESC_ID column and recreate it in a stored way.
    tnew.removecols('DATA_DESC_ID')
    tnew.addcols(makecoldesc('DATA_DESC_ID', tdesc['DATA_DESC_ID']),
                 dminfo={'TYPE': 'IncrementalStMan',
                         'NAME': 'DDID',
                         'SPEC': {}})
    # Copy the table keywords.
    keywords = tn.getkeywords()
    tnew.putkeywords(keywords)
    # Copy all column keywords.
    for col in tn.colnames():
        tnew.putcolkeywords(col, tn.getcolkeywords(col))
    # Make a deep copy of all subtables (except SORTED_TABLE).
    for key in keywords:
        if key != 'SORTED_TABLE':
            val = keywords[key]
            if isinstance(val, string_types):
                tsub = table(val, ack=False)
                tsubn = tsub.copy(newname + '/' + key, deep=True)
                tnew.putkeyword(key, tsubn)
    tnew.flush()
    # Now we have to take care that the subbands are numbered correctly.
    # The DATA_DESCRIPTION and SPECTRAL_WINDOW subtables are concatenated.
    # The ddid in the main table and spwid in DD subtable have to be updated.
    tnewdd = table(tnew.getkeyword('DATA_DESCRIPTION'),
                   readonly=False, ack=False)
    tnewspw = table(tnew.getkeyword('SPECTRAL_WINDOW'),
                    readonly=False, ack=False)
    nrdd = 0
    nrspw = 0
    nrmain = 0
    for name in names:
        t = table(name, ack=False)
        tdd = table(t.getkeyword('DATA_DESCRIPTION'), ack=False)
        tspw = table(t.getkeyword('SPECTRAL_WINDOW'), ack=False)
        # The first table already has its subtable copied.
        # Append the subtables of the other ones.
        if nrdd > 0:
            tnewdd.addrows(tdd.nrows())
            for i in range(tdd.nrows()):
                tnewdd[nrdd + i] = tdd[i]  # copy row i
            tnewspw.addrows(tspw.nrows())
            for i in range(tspw.nrows()):
                tnewspw[nrspw + i] = tspw[i]
        tnewdd.putcol('SPECTRAL_WINDOW_ID',
                      tdd.getcol('SPECTRAL_WINDOW_ID') + nrspw,
                      nrdd, tdd.nrows())
        tnew.putcol('DATA_DESC_ID',
                    t.getcol('DATA_DESC_ID') + nrdd,
                    nrmain, t.nrows())
        nrdd += tdd.nrows()
        nrspw += tspw.nrows()
        nrmain += t.nrows()
    # Overwrite keyword CHANNEL_SELECTION.
    if 'MODEL_DATA' in tnew.colnames():
        if 'CHANNEL_SELECTION' in tnew.colkeywordnames('MODEL_DATA'):
            tnew.removecolkeyword('MODEL_DATA', 'CHANNEL_SELECTION')
            # Define the CHANNEL_SELECTION keyword containing the channels of
            # all spectral windows.
            tspw = table(tnew.getkeyword('SPECTRAL_WINDOW'), ack=False)
            nchans = tspw.getcol('NUM_CHAN')
            chans = [[0, nch] for nch in nchans]
            tnew.putcolkeyword('MODEL_DATA', 'CHANNEL_SELECTION',
                               np.int32(chans))
    # Future work:
    #   If SOURCE subtables have to concatenated, the FIELD and DOPPLER
    #   have to be dealt with as well.
    #   The FEED table can be concatenated; the FEED_ID can stay the same,
    #   but spwid has to be updated.
    #   The FREQ_OFFSET table is stand-alone, thus can simply be concatenated
    #   and have spwid updated.
    #   The SYSCAL table can be very large, so it might be better to virtually
    #   concatenate it instead of making a copy (just like the main table).
    # Flush the table and subtables.
    tnew.flush(True)


def msregularize(msname, newname):
    """ Regularize an MS

    The output MS will be such that it has the same number of baselines
    for each time stamp. Where needed fully flagged rows are added.

    Possibly missing rows are written into a separate MS <newname>-add.
    It is concatenated with the original MS and sorted in order of TIME,
    DATADESC_ID, ANTENNA1,ANTENNA2 to form a new regular MS. Note that
    the new MS references the input MS (it does not copy the data).
    It means that changes made in the new MS are also made in the input MS.

    If no rows were missing, the new MS is still created referencing the
    input MS.
    """

    # Find out all baselines.
    t = table(msname)
    t1 = t.sort('unique ANTENNA1,ANTENNA2')
    nadded = 0
    # Now iterate in time,band over the MS.
    for tsub in t.iter(['TIME', 'DATA_DESC_ID']):
        nmissing = t1.nrows() - tsub.nrows()
        if nmissing < 0:
            raise ValueError("A time/band chunk has too many rows")
        if nmissing > 0:
            # Rows needs to be added for the missing baselines.
            ant1 = str(t1.getcol('ANTENNA1')).replace(' ', ',')
            ant2 = str(t1.getcol('ANTENNA2')).replace(' ', ',')
            ant1 = tsub.getcol('ANTENNA1')
            ant2 = tsub.getcol('ANTENNA2')
            t2 = taql('select from $t1 where !any(ANTENNA1 == $ant1 &&' +
                      ' ANTENNA2 == $ant2)')
            six.print_(nmissing, t1.nrows(), tsub.nrows(), t2.nrows())
            if t2.nrows() != nmissing:
                raise ValueError("A time/band chunk behaves strangely")
            # If nothing added yet, create a new table.
            # (which has to be reopened for read/write).
            # Otherwise append to that new table.
            if nadded == 0:
                tnew = t2.copy(newname + "_add", deep=True)
                tnew = table(newname + "_add", readonly=False)
            else:
                t2.copyrows(tnew)
            # Set the correct time and band in the new rows.
            tnew.putcell('TIME',
                         range(nadded, nadded + nmissing),
                         tsub.getcell('TIME', 0))
            tnew.putcell('DATA_DESC_ID',
                         range(nadded, nadded + nmissing),
                         tsub.getcell('DATA_DESC_ID', 0))
            nadded += nmissing
    # Combine the existing table and new table.
    if nadded > 0:
        # First initialize data and flags in the added rows.
        taql('update $tnew set DATA=0+0i')
        taql('update $tnew set FLAG=True')
        tcomb = table([t, tnew])
        tcomb.rename(newname + '_adds')
        tcombs = tcomb.sort('TIME,DATA_DESC_ID,ANTENNA1,ANTENNA2')
    else:
        tcombs = t.query(offset=0)
    tcombs.rename(newname)
    six.print_(newname, 'has been created; it references the original MS')
    if nadded > 0:
        six.print_(' and', newname + '_adds', 'containing', nadded, 'new rows')
    else:
        six.print_(' no rows needed to be added')
