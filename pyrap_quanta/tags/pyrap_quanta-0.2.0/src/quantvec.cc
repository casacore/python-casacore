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

  /*
  QProxy qpfromString(const String& str) {
    QuantumHolder qh;
    String err;
    if ( !qh.fromString(err, str) ) {
      throw(AipsError(err));
    }
    return qh.asQuantumVectorDouble();
  }
  */

  String qpprintQuantum(const QProxy& q) {
    ostringstream oss;
    q.print(oss);
    return String(oss);
  }

  // these functions take Unit as argument, enable outside access through
  // strings
  QProxy qpgetWithUnit(const QProxy& q, const String& u)  {
    Unit unit(u);
    return q.get(unit);
  }
  VD qpgetValueWithUnit(const QProxy& q, const String& u)  {
    Unit unit(u);
    return q.getValue(unit);
  }

  QProxy qpfromRecord(const Record& rec) {
    QuantumHolder qh;
    String err;
    if ( !qh.fromRecord(err, rec) ) {
      throw(AipsError(err));
    }
    return qh.asQuantumVectorDouble();
  }

  bool qpconforms(const QProxy& left, const QProxy& right) {
    return (left.getFullUnit().getValue() == right.getFullUnit().getValue());
  }

  Record qptoRecord(const QProxy& q) {
    QuantumHolder qh(q);
    String err;
    Record rec;
    if ( !qh.toRecord(err, rec) ) {
      throw(AipsError(err));
    }
    return rec;
  }

  QProxy qptoTime(const QProxy& q) {
    if (q.check(UnitVal::TIME)) {
      return q;
    } else {
      QuantumHolder qh(q);
      Quantity q0 = MVTime(qh.asQuantity()).get();
      QuantumHolder qh2(q0);
      return qh2.asQuantumVectorDouble();
    }
    
  }

}

namespace casa { namespace pyrap {
  void quantvec()
  {
    class_<QProxy> ("QuantVec")
      .def (init< >())
      .def (init< const QProxy& > ())
      .def (init< const VD&, const String& >())
      //      .def ("__str__", &printQuantum)
      .def ("_get_value", (const VD& ( QProxy::* )( ) const)(&QProxy::getValue),
	    return_value_policy < copy_const_reference> ()
	    )
      .def ("_get_value", &qpgetValueWithUnit)
      .def ("get_unit", &QProxy::getUnit,
	    return_value_policy < copy_const_reference> ())
      .def ("convert", (void ( QProxy::* )( const QProxy& ) )(&QProxy::convert))
      .def ("convert", (void ( QProxy::* )( ) )(&QProxy::convert))
      .def ("set_value", &QProxy::setValue)
      .def ("get", (QProxy ( QProxy::* )( ) const)(&QProxy::get))
      .def ("canonical", (QProxy ( QProxy::* )( ) const)(&QProxy::get))
      .def ("get", (QProxy ( QProxy::* )( const QProxy& ) const)(&QProxy::get))
      .def ("get", &qpgetWithUnit)
      .def ("conforms", &qpconforms)
      .def ("totime", &qptoTime)
      .def ("to_dict", &qptoRecord)
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
    //def ("from_string", &qpfromString);
    def ("from_dict_v", &qpfromRecord);
      
  }
}}
