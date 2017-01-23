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

#include <casacore/ms/MeasurementSets/MeasurementSet.h>

#include <casacore/python/Converters/PycExcp.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycValueHolder.h>
#include <casacore/python/Converters/PycRecord.h>
#include <casacore/python/Converters/PycArray.h>

#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace casacore;

using namespace boost::python;

namespace casacore { namespace python {
  void pyms()
  {
    // Note that all constructors must have a different number of arguments.
    class_<MeasurementSet> ("MeasurementSet",
            init<>())
        //  1 arg: copy constructor
      .def (init<MeasurementSet>())
      .def ("antennaTableName", &MeasurementSet::antennaTableName)
      .def ("requiredTableDesc", &MeasurementSet::requiredTableDesc,
        return_value_policy<reference_existing_object>())
      .staticmethod("requiredTableDesc")

      ;
  }
}}
