//# functionals.cc: python module for casacore functionals
//# Copyright (C) 2006,2007
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
//# $Id: pyfunctionals.cc,v 1.2 2006/10/17 03:37:27 gvandiep Exp $

#include "functionals.h"

#include <boost/python.hpp>

#include <pyrap/Converters/PycExcp.h>
#include <pyrap/Converters/PycBasicData.h>
#include <pyrap/Converters/PycArray.h>
#include <pyrap/Converters/PycRecord.h>

BOOST_PYTHON_MODULE(_functionals)
{
  casa::pyrap::register_convert_excp();
  casa::pyrap::register_convert_basicdata();
  casa::pyrap::register_convert_casa_record();

  casa::pyrap::functional();
}
