//# pyimages.cc: python module for aips++ images system
//# Copyright (C) 2008
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
//# $Id$

#include <images/Images/ImageProxy.h>
#include <pyrap/Converters/PycBasicData.h>
#include <pyrap/Converters/PycValueHolder.h>
#include <pyrap/Converters/PycRecord.h>
#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace boost::python;

namespace casa { namespace pyrap {

  void pyimages()
  {
    // Note that all constructors must have a different number of arguments.
    class_<ImageProxy> ("Image")
            // 1 arg: open image or create from array
      .def (init<ValueHolder, String, vector<ImageProxy> >())
	    //  2 arg: concat from image names
      .def (init<Vector<String>, Int>())
	    //  3 arg: concat from images objects
      .def (init<std::vector<ImageProxy>, Int, Int, Int>())

      // Member functions.
      // Functions starting with un underscore are wrapped in image.py.
      .def ("ispersistent", &ImageProxy::isPersistent)
      .def ("name", &ImageProxy::name,
            (boost::python::arg("strippath")=false))
      .def ("shape", &ImageProxy::shape)
      .def ("ndim", &ImageProxy::ndim)
      .def ("size", &ImageProxy::size)
      .def ("datatype", &ImageProxy::dataType)
      .def ("_getdata", &ImageProxy::getData)
      .def ("_getmask", &ImageProxy::getMask)
      .def ("_putdata", &ImageProxy::putData)
      .def ("haslock", &ImageProxy::hasLock,
 	    (boost::python::arg("write")=false))
      .def ("lock", &ImageProxy::lock,
 	    (boost::python::arg("write")=false,
 	     boost::python::arg("nattempts")=0))
      .def ("unlock", &ImageProxy::unlock)
      .def ("_subimage", &ImageProxy::subImage)
      .def ("coordinates", &ImageProxy::coordSys)
      .def ("imageinfo", &ImageProxy::imageInfo)
      .def ("miscinfo", &ImageProxy::miscInfo)
      .def ("unit", &ImageProxy::unit)
    ;
  }

}}
