//# functionals.cc: python module for casacore functionals.
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
//# $Id: pyfunctional.cc,v 1.1 2006/09/29 06:42:55 mmarquar Exp $

#include <boost/python.hpp>
#include <boost/python/args.hpp>
#include <scimath/Functionals/FunctionalProxy.h>
#include <pyrap/Converters/PycBasicData.h>
#include <pyrap/Converters/PycRecord.h>

using namespace boost::python;

namespace casa { namespace pyrap {
  void functional()
  {
    class_<FunctionalProxy> ("_functional")
    .def ( init< const Record&, int>())
      .def ("names", &FunctionalProxy::names)
      .def ("f", &FunctionalProxy::f)
      .def ("fdf", &FunctionalProxy::fdf)
      .def ("add", &FunctionalProxy::add)
      .def ("fc", &FunctionalProxy::fc)
      .def ("fdfc", &FunctionalProxy::fdfc)
      .def ("addc", &FunctionalProxy::addc)
      .def ("todict", &FunctionalProxy::asrecord)
      .def ("npar", &FunctionalProxy::npar)
      .def ("setparameters", &FunctionalProxy::setparameters)
      .def ("setparametersc", &FunctionalProxy::setparametersc)
      .def ("setpar", &FunctionalProxy::setpar)
      .def ("setparc", &FunctionalProxy::setparc)
      .def ("parameters", &FunctionalProxy::parameters)
      .def ("parametersc", &FunctionalProxy::parametersc)
      .def ("setmasks", &FunctionalProxy::setmasks)
      .def ("masks", &FunctionalProxy::masks)
      .def ("setmask", &FunctionalProxy::setmask)
      ;
  }
} }
