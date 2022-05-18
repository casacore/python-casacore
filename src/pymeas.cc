//# pymeas.cc: python module for MeasuresProxy object.
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
//# $Id: pymeas.cc,v 1.1 2006/09/28 05:55:00 mmarquar Exp $

#include <boost/python.hpp>
#include <boost/python/args.hpp>
#include <casacore/measures/Measures/MeasuresProxy.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycRecord.h>

using namespace boost::python;

namespace casacore { namespace python {
  void pymeas()
  {
    class_<MeasuresProxy> ("measures")
      .def (init<>())
      .def ("measure", &MeasuresProxy::measure)
      .def ("dirshow", &MeasuresProxy::dirshow)
      .def ("doframe", &MeasuresProxy::doframe)
      .def ("linelist", &MeasuresProxy::linelist)      
      .def ("obslist", &MeasuresProxy::obslist)
      .def ("source", &MeasuresProxy::source)
      .def ("line", &MeasuresProxy::line)      
      .def ("observatory", &MeasuresProxy::observatory)
      .def ("srclist", &MeasuresProxy::srclist)
      .def ("doptofreq", &MeasuresProxy::doptofreq)
      .def ("doptorv", &MeasuresProxy::doptorv)
      .def ("todop", &MeasuresProxy::todop)
      .def ("torest", &MeasuresProxy::torest)
      .def ("separation", &MeasuresProxy::separation)
      .def ("posangle", &MeasuresProxy::posangle)
      .def ("uvw", &MeasuresProxy::uvw)
      .def ("expand", &MeasuresProxy::expand)
      .def ("alltyp", &MeasuresProxy::alltyp)
        ;
  }
}}
