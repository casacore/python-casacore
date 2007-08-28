//# PycArrayNP.cc: Convert an Array to a Python numpy array
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
//# $Id: PycArrayNP.cc,v 1.2 2006/11/07 00:17:23 gvandiep Exp $

#if defined(AIPS_USENUMPY)

#include <pyrap/Converters/PycArrayNP.h>
#include <casa/Arrays/ArrayMath.h>
#include <casa/Utilities/Assert.h>
#include <casa/Exceptions/Error.h>
#include <numpy/arrayobject.h>
#include <boost/python/dict.hpp>

typedef npy_bool       Bool;
typedef npy_int8       Int8;
typedef npy_int16      Int16;
typedef npy_uint16     UInt16;
typedef npy_int32      Int32;
typedef npy_uint32     UInt32;
typedef npy_long       Long;
typedef npy_float32    Float32;
typedef npy_float64    Float64;
typedef npy_complex64  Complex32;
typedef npy_complex128 Complex64;


#define PYC_USE_PYARRAY "numpy"
namespace casa { namespace pyrap { namespace numpy {

  Bool importArray()
  {
    // numpy has diferent versions of import_array (from version 1.0.1 on).
    // Therefore import_array1 is used.
    import_array1(True);
    return True;
  }

  Array<String> ArrayCopyStr_toArray (const IPosition& shape,
				      void* data, uInt slen)
  {
    // This code converts from a numpy String array.
    // The longest string determines the length of each value.
    // They are padded with zeroes if shorter.
    using namespace boost::python;
    Array<String> arr(shape);
    String* to = arr.data();
    const char* src = static_cast<const char*>(data);
    uInt nr = arr.size();
    for (uInt i=0; i<nr; ++i) {
      if (src[slen-1] == 0) {
	to[i] = String(src);
      } else {
	to[i] = String(src, slen);
      }
      src += slen;
    }
    return arr;
  }

#include <pyrap/Converters/PycArrayComCC.h>

}}}

#endif
