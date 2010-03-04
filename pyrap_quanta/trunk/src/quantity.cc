//# quantity.cc: python module for Quantum<Vector<Double> > objects.
//# Copyright (C) 2007
//# Australia Telescope National Facility, AUSTRALIA
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
//# Correspondence concerning pyrap should be addressed as follows:
//#        Internet email: pyrap-devel@googlegroups.com
//#        Postal address: Australia Telescope National Facility
//#                        PO Box 76
//#                        Epping NSW 1710
//#                        AUSTRALIA
//#
//# $Id:$

#include <casa/Quanta.h>
#include <casa/Quanta/QLogical.h>
#include <casa/Quanta/QuantumHolder.h>
#include <casa/Quanta/MVTime.h>
#include <casa/Quanta/MVAngle.h>

#include <casa/Containers/Record.h>
#include <casa/Exceptions/Error.h>
#include <casa/sstream.h>
#include <casa/BasicSL/String.h>

#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace boost::python;


namespace casa {
  namespace pyrap {

  Quantity fromString(const String& str) {
    QuantumHolder qh;
    String err;
    if ( !qh.fromString(err, str) ) {
      throw(AipsError(err));
    }
    return qh.asQuantity();
  }
   

  String printTime(const Quantity& q, const String& fmt) {
    MVTime mvt(q);
    if (fmt == "") {
      return mvt.string();
    }
    return mvt.string(MVTime::giveMe(fmt));
  }

  String printAngle(const Quantity& q, const String& fmt) {
    MVAngle mva(q);
    if (fmt ==  "") {
      return mva.string();
    }
    return mva.string(MVAngle::giveMe(fmt));
  }

  String printQuantum(const Quantity& q,  const String& fmt) {
    if (q.get().getFullUnit() == Unit("s")) {
      return printTime(q, fmt);
    } else if  (q.get().getFullUnit() == Unit("rad")) {
      return printAngle(q, fmt);      
    }
    ostringstream oss;
    q.print(oss);
    return String(oss);
  }

  // these functions take Unit as argument, enable outside access through
  // strings
  Quantity getWithUnit(const Quantity& q, const String& u)  {
    Unit unit(u);
    return q.get(unit);
  }
  Double getValueWithUnit(const Quantity& q, const String& u)  {
    Unit unit(u);
    return q.getValue(unit);
  }

  Quantity fromRecord(const Record& rec) {
    QuantumHolder qh;
    String err;
    if ( !qh.fromRecord(err, rec) ) {
      throw(AipsError(err));
    }
    return qh.asQuantity();
  }

  bool conforms(const Quantity& left, const Quantity& right) {
    return (left.getFullUnit().getValue() == right.getFullUnit().getValue());
  }

  Record toRecord(const Quantity& q) {
    QuantumHolder qh(q);
    String err;
    Record rec;
    if ( !qh.toRecord(err, rec) ) {
      throw(AipsError(err));
    }
    return rec;
  }

  Quantity toTime(const Quantity& q) {
    if (q.check(UnitVal::TIME)) {
      return q;
    } else {
      Quantity q0 = MVTime(q).get();
      return q0;
    }    
  }

  Quantity toAngle(const Quantity& q) {
    if (q.check(UnitVal::ANGLE)) {
      return q;
    } else {
      Quantity q0 = MVAngle(q).get();
      return q0;
    }    
  }
    
    Double toUnixTime(const Quantity& q) {
      // MJD = JD - 2400000.5
      // unix = (JD - 2440587.5) * 86400.0
      const Double mjdsecToUnixsec = (2400000.5 - 2440587.5) * 86400.0;
      Quantity qt = toTime(q);
      return qt.get().getValue() + mjdsecToUnixsec;
    }

    Quantity norm(const Quantity& self, Double a) {
      return Quantity(MVAngle(self)(a).degree(), "deg");
    }

}}

namespace casa { namespace pyrap {
  void quantity()
  {
    class_<Quantity> ("Quantity")
      .def (init< >())
      .def (init< const Quantity& > ())
      .def (init< Double, const String& >())
      .def ("__repr__", &printQuantum, (boost::python::arg("self"),
					boost::python::arg("fmt")=""))
      .def ("get_value", (const Double& ( Quantity::* )( ) const)(&Quantity::getValue),
	    return_value_policy < copy_const_reference> ()
	    )
      .def ("get_value", &getValueWithUnit)
      .def ("get_unit", &Quantity::getUnit,
	    return_value_policy < copy_const_reference> ())
      .def ("convert", (void ( Quantity::* )( const Quantity& ) )(&Quantity::convert))
      .def ("convert", (void ( Quantity::* )( ) )(&Quantity::convert))
      .def ("set_value", &Quantity::setValue)
      .def ("get", (Quantity ( Quantity::* )( ) const)(&Quantity::get))
      .def ("canonical", (Quantity ( Quantity::* )( ) const)(&Quantity::get))
      .def ("get", (Quantity ( Quantity::* )( const Quantity& ) const)(&Quantity::get))
      .def ("get", &getWithUnit)
      .def ("conforms", &conforms)
      .def ("totime", &toTime)
      .def ("to_time", &toTime)
      .def ("toangle", &toAngle)
      .def ("to_angle", &toAngle)
      .def ("to_unix_time", &toUnixTime)
      .def ("to_dict", &toRecord)
      .def ("norm", &norm,  (boost::python::arg("self"), boost::python::arg("a")=-0.5))
      .def (-self)
      .def (self - self)
      .def (self -= self)
      .def (self -= Double())
      .def (self - Double() )
      .def (Double() - self)
      .def (+self)
      .def (self + self)
      .def (self += self)
      .def (self += Double())
      .def (self + Double() )
      .def (Double() + self)
      .def (self * self)
      .def (self *= self)
      .def (self *= Double())
      .def (self * Double() )
      .def (Double() * self)
      .def (self / self)
      .def (self /= self)
      .def (self /= Double())
      .def (self / Double() )
      .def (Double() / self)
      .def (self == self)
      .def (self == Double())
      .def (Double() == self)
      .def (self != self)
      .def (self != Double())
      .def (Double() != self)

      .def (self < self)
      .def (self < Double())
      .def (Double() < self)
      .def (self <= self)
      .def (self <= Double())
      .def (Double() <= self)

      .def (self > self)
      .def (self > Double())
      .def (Double() > self)
      .def (self >= self)
      .def (self >= Double())
      .def (Double() >= self)     
      .def ("formatted", &printQuantum)
      ;
    def ("from_string", &fromString);
    def ("from_dict", &fromRecord);
      
  }
}}
