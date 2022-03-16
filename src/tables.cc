//# tables.cc: python module for AIPS++ table system
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
//# $Id: tables.cc,v 1.5 2006/10/17 03:37:27 gvandiep Exp $

#include "tables.h"

#include <casacore/python/Converters/PycExcp.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycValueHolder.h>
#include <casacore/python/Converters/PycRecord.h>
#include <casacore/python/Converters/PycArray.h>
#include <casacore/tables/Tables/TableProxy.h>

#include <casacore/meas/MeasUDF/Register.h>
#include <casacore/derivedmscal/DerivedMC/Register.h>

#include <boost/python.hpp>

BOOST_PYTHON_MODULE(_tables)
{
  casacore::python::register_convert_excp();
  casacore::python::register_convert_basicdata();
  casacore::python::register_convert_casa_valueholder();
  casacore::python::register_convert_casa_record();
  casacore::python::register_convert_std_vector<casacore::TableProxy>();

  casacore::python::pytable();
  casacore::python::pytablerow();
  casacore::python::pytableiter();
  casacore::python::pytableindex();

  casacore::python::pyms();

  // Register the TaQL meas and mscal functions.
  // Normally they are loaded as a shared library, but that cannot
  // be done if the program is built statically.
  register_meas();
  register_derivedmscal();
}

