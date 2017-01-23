//# pytable.cc: python module for TableProxy object.
//# Copyright (C) 2006
//# Associated Universities, Inc. Washington DC, USA.
//#
//# This library is free software; you can redistribute it and/or modify it
//# under the terms of the GNU Library General Public License as published by
//# the Free Software Foundation; either version 2 of the License, or (at your
//# option) any later version.
//#
//# This library is distributed in the hope that it will be useful, but WITHOUT
//# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
//# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
//# License for more details.
//#
//# You should have received a copy of the GNU Library General Public License
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

#include <casacore/tables/Tables/TableDesc.h>
#include <casacore/tables/Tables/TabPath.h>

#include <casacore/python/Converters/PycExcp.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycValueHolder.h>
#include <casacore/python/Converters/PycRecord.h>
#include <casacore/python/Converters/PycArray.h>

#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace casacore;

using namespace boost::python;

namespace casacore {
namespace python {

  void pytabpath()
  {
    class_<TabPath> ("TabPath", init<>())
      .def (init<String>())
      .def ("found", &TabPath::found,
        (boost::python::arg("name"),
         boost::python::arg("dir")))
      ;
  }

  void pytabledesc()
  {
    // Note that all constructors must have a different number of arguments.
    scope table_desc_scope = class_<TableDesc> ("TableDesc",
            init<>())
        //  1 arg: copy constructor
      .def (init<TableDesc>())
      .def (init<String, TableDesc::TDOption>())
      .def (init<String, String, TableDesc::TDOption>())
      .def (init<TableDesc, String, String, TableDesc::TDOption, Bool>())
      .def (init<TableDesc, String, String, TabPath, TableDesc::TDOption, Bool>())
      .def (init<TableDesc, TableDesc::TDOption>())
      ;


    enum_<TableDesc::TDOption>("TDOption")
      .value("Old", TableDesc::Old)
      .value("New", TableDesc::New)
      .value("NewNoReplace", TableDesc::NewNoReplace)
      .value("Scratch", TableDesc::Scratch)
      .value("Update", TableDesc::Update)
      .value("Delete", TableDesc::Delete)
      .export_values()
      ;
  }
}
}
