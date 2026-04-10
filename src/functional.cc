//# functionals.cc: python module for casacore functionals.
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
//# $Id: pyfunctional.cc,v 1.1 2006/09/29 06:42:55 mmarquar Exp $

#include <boost/python.hpp>
#include <boost/python/args.hpp>
#include <casacore/scimath/Functionals/FunctionalProxy.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycRecord.h>

using namespace boost::python;

namespace casacore { namespace python {

  
  void functional()
  {
    class_<FunctionalProxy> ("_functional")
    .def ( init< const Record&, int>())
      .def ("_f", &FunctionalProxy::f)
      .def ("_fc", &FunctionalProxy::fc)
      .def ("_fdf", &FunctionalProxy::fdf)
      .def ("_fdfc", &FunctionalProxy::fdfc)
      .def ("_add", &FunctionalProxy::add)
      .def ("_addc", &FunctionalProxy::addc)
      .def ("todict", &FunctionalProxy::asrecord)
      .def ("npar", &FunctionalProxy::npar)
      .def ("ndim", &FunctionalProxy::ndim)
      .def ("_setparameters", &FunctionalProxy::setparameters)
      .def ("_setparametersc", &FunctionalProxy::setparametersc)
      .def ("_setpar", &FunctionalProxy::setpar)
      .def ("_setparc", &FunctionalProxy::setparc)
      .def ("_parameters", &FunctionalProxy::parameters)
      .def ("_parametersc", &FunctionalProxy::parametersc)
      .def ("_setmasks", &FunctionalProxy::setmasks)
      .def ("_masks", &FunctionalProxy::masks)
      .def ("_setmask", &FunctionalProxy::setmask)
      ;
  }
} }
