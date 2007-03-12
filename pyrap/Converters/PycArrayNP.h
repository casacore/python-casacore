//# PycArrayNP.h: Class to convert an Array to/from a Python numpy array
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
//# $Id: PycArrayNP.h,v 1.1 2006/11/06 00:14:44 gvandiep Exp $


#ifndef PYRAP_PYCARRAYNP_H
#define PYRAP_PYCARRAYNP_H


#include <casa/Containers/ValueHolder.h>
#include <casa/Arrays/Array.h>
#include <boost/python.hpp>
#include <boost/python/object.hpp>

namespace casa { namespace pyrap { namespace numpy {

//# Define the common functions if numpy is used.
#if defined(AIPS_USENUMPY)
#define PYC_USE_PYARRAY "numpy"
#endif
#include <pyrap/Converters/PycArrayComH.h>
#undef PYC_USE_PYARRAY

}}}

#endif
