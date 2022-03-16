# __init__.py: Python image functions
# Copyright (C) 2008
# Associated Universities, Inc. Washington DC, USA.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Correspondence concerning AIPS++ should be addressed as follows:
#        Internet email: aips2-request@nrao.edu.
#        Postal address: AIPS++ Project Office
#                        National Radio Astronomy Observatory
#                        520 Edgemont Road
#                        Charlottesville, VA 22903-2475 USA
#
# $Id$

"""Python interface to the Casacore images module.

A `casacore image <../../casacore/doc/html/group__Images__module.html>`_
represents an astronomical image of arbitrary dimensionality.
Several image formats are recognized:

`casacore paged image <../../casacore/doc/html/classcasa_1_1PagedImage.html>`_
  is the native casacore image format stored in a casacore table.
`HDF5 <http://www.hdfgroup.org/HDF5>`_
  is the HDF5 format often used in the earth science community.
`FITS <http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html>`_
  is the well-known astronomical FITS format
`miriad <http://www.atnf.csiro.au/computing/software/miriad>`_
  is the format used by the radio-astronomical MIRIAD package.

The following functionality exists:

- get and put data (slices)
- get or put a mask
- get meta data like coordinates and history
- get, put, or search optional image attributes (as used for LOFAR)
- get statistics
- form a subimage
- form an image expression which is treated as an ordinary image
- regrid the image
- write the image to a FITS file

"""

# Make image interface available.
from .image import image
