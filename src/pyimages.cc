//# pyimages.cc: python module for aips++ images system
//# Copyright (C) 2008
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
//# $Id$

#include <casacore/images/Images/ImageProxy.h>
#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycValueHolder.h>
#include <casacore/python/Converters/PycRecord.h>
#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace boost::python;

namespace casacore { namespace python {

  void pyimages()
  {
    // Note that all constructors must have a different number of arguments.
    class_<ImageProxy> ("Image")
            // 1 arg: copy constructor
      .def (init<ImageProxy>())
	    // 2 arg: concat from image names
      .def (init<Vector<String>, Int>())
            // 3 arg: open image or image expression
      .def (init<String, String, std::vector<ImageProxy> >())
	    // 4 arg: concat from images objects
      .def (init<std::vector<ImageProxy>, Int, Int, Int>())
            // 8 arg: create image from array
      .def (init<ValueHolder, ValueHolder, Record, String, Bool, Bool,
            String, IPosition>())
            // 9 arg: create image from shape
      .def (init<IPosition, ValueHolder, Record, String, Bool, Bool,
            String, IPosition, Int>())

      // Member functions.
      // Functions starting with un underscore are wrapped in image.py.
      .def ("_ispersistent", &ImageProxy::isPersistent) 
      .def ("_name", &ImageProxy::name,
            (boost::python::arg("strippath")))
      .def ("_shape", &ImageProxy::shape)
      .def ("_ndim", &ImageProxy::ndim)
      .def ("_size", &ImageProxy::size)
      .def ("_datatype", &ImageProxy::dataType)
      .def ("_imagetype", &ImageProxy::imageType)
      .def ("_getdata", &ImageProxy::getData)
      .def ("_getmask", &ImageProxy::getMask)
      .def ("_putdata", &ImageProxy::putData)
      .def ("_putmask", &ImageProxy::putMask)
      .def ("_haslock", &ImageProxy::hasLock,
 	    (boost::python::arg("write")))
      .def ("_lock", &ImageProxy::lock,
 	    (boost::python::arg("write"),
 	     boost::python::arg("nattempts")))
      .def ("_unlock", &ImageProxy::unlock)
      .def ("_attrgroupnames", &ImageProxy::attrGroupNames)
      .def ("_attrcreategroup", &ImageProxy::createAttrGroup,
            (boost::python::arg("groupname")))
      .def ("_attrnames", &ImageProxy::attrNames,
            (boost::python::arg("groupname")))
      .def ("_attrnrows", &ImageProxy::attrNrows,
            (boost::python::arg("groupname")))
      .def ("_attrget", &ImageProxy::getAttr,
            (boost::python::arg("groupname"),
             boost::python::arg("attrname"),
             boost::python::arg("rownr")))
      .def ("_attrgetrow", &ImageProxy::getAttrRow,
            (boost::python::arg("groupname"),
             boost::python::arg("rownr")))
      .def ("_attrgetunit", &ImageProxy::getAttrUnit,
            (boost::python::arg("groupname"),
             boost::python::arg("attrname")))
      .def ("_attrgetmeas", &ImageProxy::getAttrMeas,
            (boost::python::arg("groupname"),
             boost::python::arg("attrname")))
      .def ("_attrput", &ImageProxy::putAttr,
            (boost::python::arg("groupname"),
             boost::python::arg("attrname"),
             boost::python::arg("rownr"),
             boost::python::arg("value"),
             boost::python::arg("unit"),
             boost::python::arg("meas")))
      .def ("_subimage", &ImageProxy::subImage,
            (boost::python::arg("blc"),
             boost::python::arg("trc"),
             boost::python::arg("inc"),
             boost::python::arg("dropdegenerate")))
      .def ("_coordinates", &ImageProxy::coordSys)
      .def ("_toworld", &ImageProxy::toWorld,
            (boost::python::arg("pixel"),
             boost::python::arg("reverseAxes")))
      .def ("_topixel", &ImageProxy::toPixel,
            (boost::python::arg("world"),
             boost::python::arg("reverseAxes")))
      .def ("_imageinfo", &ImageProxy::imageInfo)
      .def ("_miscinfo", &ImageProxy::miscInfo)
      .def ("_unit", &ImageProxy::unit)
      .def ("_history", &ImageProxy::history)
      .def ("_tofits", &ImageProxy::toFits,
            (boost::python::arg("filename"),
             boost::python::arg("overwrite"),
             boost::python::arg("velocity"),
             boost::python::arg("optical"),
             boost::python::arg("bitpix"),
             boost::python::arg("minpix"),
             boost::python::arg("maxpix")))
      .def ("_saveas", &ImageProxy::saveAs,
            (boost::python::arg("filename"),
             boost::python::arg("overwrite"),
             boost::python::arg("hdf5"),
             boost::python::arg("copymask"),
             boost::python::arg("newmaskname"),
             boost::python::arg("newtileshape")))
      .def ("_statistics", &ImageProxy::statistics,
            (boost::python::arg("axes"),
             boost::python::arg("mask"), 
             boost::python::arg("minMaxValues"),
             boost::python::arg("exclude"),
             boost::python::arg("robust")))
      .def ("_regrid", &ImageProxy::regrid,
            (boost::python::arg("axes"),
             boost::python::arg("outname"),
             boost::python::arg("overwrite"),
             boost::python::arg("outshape"),
             boost::python::arg("coordsys"),
             boost::python::arg("interpolation"),
             boost::python::arg("decimate"),
             boost::python::arg("replicate"),
             boost::python::arg("refchange"),
             boost::python::arg("forceregrid")))
    ;
  }

}}
