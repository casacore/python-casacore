//# PycArrayNA.cc: Convert an Array to a Python numarray array
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
//# $Id: PycArrayNA.cc,v 1.2 2006/11/07 00:17:23 gvandiep Exp $

#if defined(AIPS_USENUMARRAY)

#include <pyrap/Converters/PycArrayNA.h>
#include <casa/Arrays/ArrayMath.h>
#include <casa/Utilities/Assert.h>
#include <casa/Exceptions/Error.h>
#include <numarray/arrayobject.h>
#include <boost/python/dict.hpp>

// Define numarray types as numpy's ones.
// numarray has no bool; define char as such.
#define NPY_BOOL       PyArray_CHAR
#define NPY_INT8       PyArray_SBYTE
#define NPY_UINT8      PyArray_UBYTE
#define NPY_INT16      PyArray_SHORT
#define NPY_UINT16     PyArray_USHORT
#define NPY_INT32      PyArray_INT
#define NPY_UINT32     PyArray_UINT
#define NPY_INT64      PyArray_LONG
#define NPY_UINT64     PyArray_LONG
#define NPY_FLOAT32    PyArray_FLOAT
#define NPY_FLOAT64    PyArray_DOUBLE
#define NPY_COMPLEX64  PyArray_CFLOAT
#define NPY_COMPLEX128 PyArray_CDOUBLE
#define NPY_OBJECT     PyArray_OBJECT
#define NPY_STRING     PyArray_INT

// Make the numarray typedefs equal to those used in numpy.
typedef ::Bool    npy_bool;
typedef Int8      npy_int8;
typedef UInt8     npy_uint8;
typedef Int16     npy_int16;
typedef UInt16    npy_uint16;
typedef Int32     npy_int32;
typedef UInt32    npy_uint32;
typedef Int64     npy_int64;
typedef UInt64    npy_uint64;
typedef Float32   npy_float32;
typedef Float64   npy_float64;
typedef Complex32 npy_complex64;
typedef Complex64 npy_complex128;

#define PYC_USE_PYARRAY "numarray"
namespace casa { namespace pyrap { namespace numarray {

  Bool importArray()
  {
    import_array();
    return True;
  }

  Array<String> ArrayCopyStr_toArray (const IPosition&,
				      void*, uInt)
  {
    throw AipsError ("PycArray: numarray string arrays are not supported");
  }

#include <pyrap/Converters/PycArrayComCC.h>

}}}

#endif
