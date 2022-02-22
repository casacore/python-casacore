//# quantity.cc: python module for Quantum<Vector<Double> > objects.
//# Copyright (C) 2007
//# Australia Telescope National Facility, AUSTRALIA
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
//# Correspondence concerning pyrap should be addressed as follows:
//#        Internet email: pyrap-devel@googlegroups.com
//#        Postal address: Australia Telescope National Facility
//#                        PO Box 76
//#                        Epping NSW 1710
//#                        AUSTRALIA
//#
//# $Id:$

#include <casacore/casa/Quanta.h>
#include <casacore/casa/Quanta/QLogical.h>
#include <casacore/casa/Quanta/QuantumHolder.h>
#include <casacore/casa/Quanta/MVTime.h>
#include <casacore/casa/Quanta/MVAngle.h>

#include <casacore/casa/Containers/Record.h>
#include <casacore/casa/Exceptions/Error.h>
#include <casacore/casa/sstream.h>
#include <casacore/casa/BasicSL/String.h>

#include <boost/python.hpp>
#include <boost/python/args.hpp>

using namespace boost::python;

namespace casacore {
  namespace python {

  typedef Quantum<Vector<Double> > QProxy;
  typedef Vector<Double> VD;

    /*
  String qpprintQuantum(const QProxy& q) {
    ostringstream oss;
    q.print(oss);
    return String(oss);
  }
    */
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
      VD values = q.getValue();
      Unit u = q.getUnit();
      Unit outu;
      VD outvals(values.nelements());
      for (uInt i=0; i < values.nelements(); ++i) {
	Quantity q0 = MVTime(Quantity(values[i], u)).get();
	outu = q0.getUnit();
	cout << q0 << endl;
	outvals[i] = q0.getValue();
      }
      return QProxy(outvals, outu);
    }
  }

  QProxy qptoAngle(const QProxy& q) {
    if (q.check(UnitVal::ANGLE)) {
      return q;
    } else {
      VD values = q.getValue();
      Unit u = q.getUnit();
      Unit outu;
      VD outvals(values.nelements());
      for (uInt i=0; i < values.nelements(); ++i) {
	Quantity q0 = MVAngle(Quantity(values[i], u)).get();
	outu = q0.getUnit();
	cout << q0 << endl;
	outvals[i] = q0.getValue();
      }
      return QProxy(outvals, outu);
    }
    
  }


    QProxy norm(const QProxy& self, Double a) {
      VD val = self.get().getValue();
      VD outval(val.nelements());
      for (uInt i=0; i< val.nelements(); ++i) {
	outval(i) = MVAngle(val[i])(a).degree();
      }
      return QProxy(outval, "deg");
    }

  String printTime(const QProxy& q, const String& fmt) {
    ostringstream oss;
    VD val = q.get().getValue();
    size_t n = val.nelements();
    Unit u = q.get().getUnit(); 
    oss << "[";
    for (size_t i=0; i < n; ++i) {
      MVTime mvt(Quantity(val[i], u));
      if (fmt =="") {
	oss << mvt.string();
      } else {
	oss <<  mvt.string(MVTime::giveMe(fmt));
      }
      if ( i < n-1 ) {
	oss << ", ";
      }
    }
    oss << "]";
    return String(oss);
  }
  
  String printAngle(const QProxy& q, const String& fmt) {
    ostringstream oss;
    VD val = q.get().getValue();
    size_t n = val.nelements();
    Unit u = q.get().getUnit(); 
    oss << "[";
    for (size_t i=0; i < n; ++i) {
      MVAngle mva(Quantity(val[i], u));
      if (fmt =="") {
	oss << mva.string();
      } else {
	oss <<  mva.string(MVAngle::giveMe(fmt));
      }
      if ( i < n-1 ) {
	oss << ", ";
      }
    }
    oss << "]";
    return String(oss);
  }
  
  String qpprintQuantum(const QProxy& q,  const String& fmt) {
    if (q.get().getFullUnit() == Unit("s")) {
      return printTime(q, fmt);
      } else if  (q.get().getFullUnit() == Unit("rad")) {
      return printAngle(q, fmt);      
    }
    ostringstream oss;
    q.print(oss);
    return String(oss);
  }

}}

namespace casacore { namespace python {

  void quantvec()
  {
    class_<QProxy> ("QuantVec")
      .def (init< >())
      .def (init< const QProxy& > ())
      .def (init< const VD&, const String& >())
      .def ("__repr__", &qpprintQuantum, (boost::python::arg("self"),
					boost::python::arg("fmt")=""))
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
      .def ("get", 
	    (QProxy ( QProxy::* )( const QProxy& ) const)(&QProxy::get))
      .def ("get", &qpgetWithUnit)
      .def ("conforms", &qpconforms)
      .def ("norm", &norm, (boost::python::arg("self"), boost::python::arg("a")=-0.5))
      .def ("totime", &qptoTime)
      .def ("to_time", &qptoTime)
      .def ("toangle", &qptoAngle)
      .def ("to_angle", &qptoAngle)
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
      .def ("formatted", &qpprintQuantum)
      ;
    def ("from_dict_v", &qpfromRecord);
      
  }
}}
