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
#include <casa/Containers/Record.h>
#include <casa/Exceptions/Error.h>
#include <casa/sstream.h>
#include <casa/BasicSL/String.h>

#include <boost/python.hpp>
//#include <boost/python/args.hpp>
using namespace boost::python;


namespace casa {
  typedef Quantum<Vector<Double> > QProxy;
  typedef Vector<Double> VD;

  QProxy fromString(const String& str) {
    QuantumHolder qh;
    String err;
    if ( !qh.fromString(err, str) ) {
      throw(AipsError(err));
    }
    return qh.asQuantumVectorDouble();
  }
  
  String printQuantum(const QProxy& q) {
    ostringstream oss;
    q.print(oss);
    return String(oss);
  }

  // these functions take Unit as argument, enable outside access through
  // strings
  QProxy getWithUnit(const QProxy& q, const String& u)  {
    Unit unit(u);
    return q.get(unit);
  }
  VD getValueWithUnit(const QProxy& q, const String& u)  {
    Unit unit(u);
    return q.getValue(unit);
  }

  QProxy fromRecord(const Record& rec) {
    QuantumHolder qh;
    String err;
    if ( !qh.fromRecord(err, rec) ) {
      throw(AipsError(err));
    }
    return qh.asQuantumVectorDouble();
  }

  Record toRecord(const QProxy& q) {
    QuantumHolder qh(q);
    String err;
    Record rec;
    if ( !qh.toRecord(err, rec) ) {
      throw(AipsError(err));
    }
    return rec;
  }

}

/*
#include <casa/Quanta/QLogical.cc>
#include <casa/Quanta/QMath.cc>
#include <casa/BasicMath/Math.cc>
#include <casa/Arrays/ArrayLogical.cc>
namespace casa {
  template Bool operator!=(Quantum<Vector<Double> > const &, 
			   Quantum<Vector<Double> > const &);
  template Bool operator==(Quantum<Vector<Double> > const &, 
			   Quantum<Vector<Double> > const &);
  template Quantum<Vector<Double> > pow(Quantum<Vector<Double> > const &, Int);
  template Array<Bool> operator<(const Array<Double>&, const Array<Double>&);
}

*/
namespace casa { namespace pyrap {
  void quantity()
  {
    class_<QProxy> ("Quantity")
      .def (init< >())
      .def (init< const QProxy& > ())
      .def (init< const VD&, const String& >())
      //      .def ("__str__", &printQuantum)
      .def ("_get_value", (const VD& ( QProxy::* )( ) const)(&QProxy::getValue),
	    return_value_policy < copy_const_reference> ()
	    )
      .def ("_get_value", &getValueWithUnit)
      .def ("get_unit", &QProxy::getUnit,
	    return_value_policy < copy_const_reference> ())
      .def ("convert", (void ( QProxy::* )( const QProxy& ) )(&QProxy::convert))
      .def ("convert", (void ( QProxy::* )( ) )(&QProxy::convert))
      .def ("set_value", &QProxy::setValue)
      .def ("get", (QProxy ( QProxy::* )( ) const)(&QProxy::get))
      .def ("canonical", (QProxy ( QProxy::* )( ) const)(&QProxy::get))
      .def ("get", (QProxy ( QProxy::* )( const QProxy& ) const)(&QProxy::get))
      .def ("get", &getWithUnit)
      .def (-self)
      .def (self - self)
      .def (self -= self)
      .def (self -= VD())
      .def (self - VD() )
      .def (VD() - self)
      .def (+self)
      .def (self + self)
      .def (self += self)
      .def (self += VD())
      .def (self + VD() )
      .def (VD() + self)
      .def (self * self)
      .def (self *= self)
      .def (self *= VD())
      .def (self * VD() )
      .def (VD() * self)
      .def (self / self)
      .def (self /= self)
      .def (self /= VD())
      .def (self / VD() )
      .def (VD() / self)
      .def (self == self)
      .def (self == VD())
      .def (VD() == self)
      .def (self != self)
      .def (self != VD())
      .def (VD() != self)

      
      .def (self < self)
      .def (self < VD())
      .def (VD() < self)
      .def (self <= self)
      .def (self <= VD())
      .def (VD() <= self)

      .def (self > self)
      .def (self > VD())
      .def (VD() > self)
      .def (self >= self)
      .def (self >= VD())
      .def (VD() >= self)
      
      ;
    def ("from_string", &fromString);
    def ("from_dict", &fromRecord);
    def ("todict", &toRecord);
      
  }
}}
