//# pytable.cc: python module for TableProxy object.
//# Copyright (C) 2006
//# Associated Universities, Inc. Washington DC, USA.
//#
//# This library is free software; you can redistribute it and/or modify it
//# under the terms of the GNU Lesser General Public License as published by
//# the Free Software Foundation; either version 3 of the License, or (at your
//# option) any later version.
//#
//# This library is distributed in the hope that it will be useful, but WITHOUT
//# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
//# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
//# License for more details.
//#
//# You should have received a copy of the GNU Lesser General Public License
//# along with this library; if not, write to the Free Software Foundation,
//# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
//#
//# Correspondence concerning AIPS++ should be addressed as follows:
//#        Internet email: aips2-request@nrao.edu.
//#        Postal address: AIPS++ Project Office
//#                        National Radio Astronomy Observatory
//#                        520 Edgemont Road
//#                        Charlottesville, VA 22903-2475 USA
//#
//# $Id: pytable.cc,v 1.5 2006/11/08 00:12:55 gvandiep Exp $

#include <casacore/tables/Tables/TableProxy.h>

#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycValueHolder.h>
#include <casacore/python/Converters/PycRecord.h>

#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace boost::python;

namespace casacore { namespace python {

  void pytable()
  {
    // Note that all constructors must have a different number of arguments.
    class_<TableProxy> ("Table",
            init<>())
	    //  1 arg: copy constructor
      .def (init<TableProxy>())
	    //  2 arg: table query command
      .def (init<String, std::vector<TableProxy> >())
	    //  3 arg: open single table
      .def (init<String, Record, int>())
	    //  4 arg: open multiple tables as concatenation
      .def (init<Vector<String>, Vector<String>, Record, int>())
	    //  5 arg: concatenate open tables
      .def (init<std::vector<TableProxy>, Vector<String>, int, int, int>())
	    //  7 arg: create new table
      .def (init<String, Record, String, String, int, Record, Record>())
	    // 11 arg: read ascii
      .def (init<String, String, String, Bool, IPosition, String, String ,int, int, Vector<String>, Vector<String> >())

      // Member functions
      // Functions starting with an underscore are wrapped in table.py.
      .def ("_flush", &TableProxy::flush,
            (boost::python::arg("recursive")))
      .def ("_resync", &TableProxy::resync)
      .def ("_close", &TableProxy::close)
      .def ("_toascii", &TableProxy::toAscii,
 	    (boost::python::arg("asciifile"),
 	     boost::python::arg("headerfile"),
 	     boost::python::arg("columnnames"),
 	     boost::python::arg("sep"),
 	     boost::python::arg("precision"),
 	     boost::python::arg("usebrackets")))
      .def ("_rename", &TableProxy::rename,
 	    (boost::python::arg("newtablename")))
      .def ("_copy", &TableProxy::copy,
 	    (boost::python::arg("newtablename"),
 	     boost::python::arg("memorytable"),
	     boost::python::arg("deep"),
 	     boost::python::arg("valuecopy"),
 	     boost::python::arg("endian"),
 	     boost::python::arg("dminfo"),
 	     boost::python::arg("copynorows")))
      .def ("_copyrows", &TableProxy::copyRows,
 	    (boost::python::arg("outtable"),
 	     boost::python::arg("startrowin"),
 	     boost::python::arg("startrowout"),
 	     boost::python::arg("nrow")))
      .def ("_selectrows", &TableProxy::selectRows,
 	    (boost::python::arg("rownrs"),
 	     boost::python::arg("name")))
      .def ("_iswritable", &TableProxy::isWritable)
      .def ("_endianformat", &TableProxy::endianFormat)
      .def ("_lock", &TableProxy::lock,
 	    (boost::python::arg("write"),
 	     boost::python::arg("nattempts")))
      .def ("_unlock", &TableProxy::unlock)
      .def ("_haslock", &TableProxy::hasLock,
 	    (boost::python::arg("write")))
      .def ("_lockoptions", &TableProxy::lockOptions)
      .def ("_datachanged", &TableProxy::hasDataChanged)
      .def ("_ismultiused", &TableProxy::isMultiUsed,
 	    (boost::python::arg("checksubtables")))
      .def ("_name", &TableProxy::tableName)
      .def ("_partnames", &TableProxy::getPartNames,
 	    (boost::python::arg("recursive")))
      .def ("_info", &TableProxy::tableInfo)
      .def ("_putinfo", &TableProxy::putTableInfo,
 	    (boost::python::arg("value")))
      .def ("_addreadmeline", &TableProxy::addReadmeLine,
 	    (boost::python::arg("value")))
      .def ("_setmaxcachesize", &TableProxy::setMaximumCacheSize,
	    (boost::python::arg("columnname"),
	     boost::python::arg("nbytes")))
      .def ("_rownumbers", &TableProxy::rowNumbers,
	    (boost::python::arg("table")))
      .def ("_colnames", &TableProxy::columnNames)
      .def ("_isscalarcol", &TableProxy::isScalarColumn,
	    (boost::python::arg("columnname")))
      .def ("_coldatatype", &TableProxy::columnDataType,
	    (boost::python::arg("columnname")))
      .def ("_colarraytype", &TableProxy::columnArrayType,
	    (boost::python::arg("columnname")))
      .def ("_ncols", &TableProxy::ncolumns)
      .def ("_nrows", &TableProxy::nrows)
      .def ("_addcols", &TableProxy::addColumns,
	    (boost::python::arg("desc"),
             boost::python::arg("dminfo"),
             boost::python::arg("addtoparent")))
      .def ("_renamecol", &TableProxy::renameColumn,
	    (boost::python::arg("oldname"),
	     boost::python::arg("newname")))
      .def ("_removecols", &TableProxy::removeColumns,
	    (boost::python::arg("columnnames")))
      .def ("_addrows", &TableProxy::addRow,
	    (boost::python::arg("nrows")))
      .def ("_removerows", &TableProxy::removeRow,
	    (boost::python::arg("rownrs")))
      .def ("_iscelldefined", &TableProxy::cellContentsDefined,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr")))
      .def ("_getcell", &TableProxy::getCell,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr")))
      .def ("_getcellvh", &TableProxy::getCellVH,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr"),
             boost::python::arg("value")))
      .def ("_getcellslice", &TableProxy::getCellSliceIP,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr"),
	     boost::python::arg("blc"),
	     boost::python::arg("trc"),
	     boost::python::arg("inc")))
      .def ("_getcellslicevh", &TableProxy::getCellSliceVHIP,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr"),
	     boost::python::arg("blc"),
	     boost::python::arg("trc"),
	     boost::python::arg("inc"),
             boost::python::arg("value")))
      .def ("_getcol", &TableProxy::getColumn,
	    (boost::python::arg("columnname"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr")))
      .def ("_getcolvh", &TableProxy::getColumnVH,
	    (boost::python::arg("columnname"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr"),
             boost::python::arg("value")))
      .def ("_getvarcol", &TableProxy::getVarColumn,
	    (boost::python::arg("columnname"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr")))
      .def ("_getcolslice", &TableProxy::getColumnSliceIP,
	    (boost::python::arg("columnname"),
	     boost::python::arg("blc"),
	     boost::python::arg("trc"),
	     boost::python::arg("inc"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr")))
      .def ("_getcolslicevh", &TableProxy::getColumnSliceVHIP,
	    (boost::python::arg("columnname"),
	     boost::python::arg("blc"),
	     boost::python::arg("trc"),
	     boost::python::arg("inc"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr"),
             boost::python::arg("value")))
      .def ("_putcell", &TableProxy::putCell,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr"),
	     boost::python::arg("value")))
      .def ("_putcellslice", &TableProxy::putCellSliceIP,
	    (boost::python::arg("columnname"),
	     boost::python::arg("rownr"),
	     boost::python::arg("value"),
	     boost::python::arg("blc"),
	     boost::python::arg("trc"),
	     boost::python::arg("inc")))
      .def ("_putcol", &TableProxy::putColumn,
	    (boost::python::arg("columnname"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr"),
	     boost::python::arg("value")))
      .def ("_putvarcol", &TableProxy::putVarColumn,
	    (boost::python::arg("columnname"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr"),
	     boost::python::arg("value")))
      .def ("_putcolslice", &TableProxy::putColumnSliceIP,
	    (boost::python::arg("columnname"),
	     boost::python::arg("value"),
	     boost::python::arg("blc"),
	     boost::python::arg("trc"),
	     boost::python::arg("inc"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr")))
      .def ("_getcolshapestring", &TableProxy::getColumnShapeString,
	    (boost::python::arg("columnname"),
	     boost::python::arg("startrow"),
	     boost::python::arg("nrow"),
	     boost::python::arg("rowincr"),
	     boost::python::arg("reverseaxes")))
      .def ("_getkeyword", &TableProxy::getKeyword,
	    (boost::python::arg("columnname"),
	     boost::python::arg("keyword"),
	     boost::python::arg("keywordindex")))
      .def ("_getkeywords", &TableProxy::getKeywordSet,
	    (boost::python::arg("columnname")))
      .def ("_putkeyword", &TableProxy::putKeyword,
	    (boost::python::arg("columnname"),
	     boost::python::arg("keyword"),
	     boost::python::arg("keywordindex"),
	     boost::python::arg("makesubrecord"),
	     boost::python::arg("value")))
      .def ("_putkeywords", &TableProxy::putKeywordSet,
	    (boost::python::arg("columnname"),
	     boost::python::arg("value")))
      .def ("_removekeyword", &TableProxy::removeKeyword,
	    (boost::python::arg("columnname"),
	     boost::python::arg("keyword"),
	     boost::python::arg("keywordindex")))
      .def ("_getfieldnames", &TableProxy::getFieldNames,
	    (boost::python::arg("columnname"),
	     boost::python::arg("keyword"),
	     boost::python::arg("keywordindex")))
      .def ("_getdminfo", &TableProxy::getDataManagerInfo)
      .def ("_getdmprop", &TableProxy::getProperties,
	    (boost::python::arg("name"),
	     boost::python::arg("bycolumn")))
      .def ("_setdmprop", &TableProxy::setProperties,
	    (boost::python::arg("name"),
             boost::python::arg("properties"),
	     boost::python::arg("bycolumn")))
      .def ("_getdesc", &TableProxy::getTableDescription,
	    (boost::python::arg("actual"),
	     boost::python::arg("_cOrder")=true))
      .def ("_getcoldesc", &TableProxy::getColumnDescription,
	    (boost::python::arg("columnname"),
 	     boost::python::arg("actual"),
	     boost::python::arg("_cOrder")=true))
      .def ("_showstructure", &TableProxy::showStructure,
	    (boost::python::arg("dataman"),
 	     boost::python::arg("column"),
 	     boost::python::arg("subtable"),
	     boost::python::arg("sort")))
      .def ("_getasciiformat", &TableProxy::getAsciiFormat)
      .def ("_getcalcresult", &TableProxy::getCalcResult)
      ;
  }

}}
