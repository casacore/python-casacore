//# fitting.cc: python module for casacore fitting
//# Copyright (C) 2006,2007
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
//# $Id: fitting.cc,v 1.1 2006/10/20 06:30:03 mmarquar Exp $


#include <boost/python.hpp>

#include "fitting.h"

#include <casacore/python/Converters/PycExcp.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycRecord.h>
#include <casacore/python/Converters/PycArray.h>

BOOST_PYTHON_MODULE(_fitting)
{
  casacore::python::register_convert_excp();
  casacore::python::register_convert_basicdata();
  casacore::python::register_convert_casa_record();
  casacore::python::fit();
}
