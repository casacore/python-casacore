# image.py: Python image functions
# Copyright (C) 2008
# Associated Universities, Inc. Washington DC, USA.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Library General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
# License for more details.
#
# You should have received a copy of the GNU Library General Public License
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

# Make interface to class ImageProxy available.
from _images import Image
import numpy, numpy.core.ma

from pyrap.images.coordinates import coordinatesystem

class image(Image):
    """
        The Python interface to casacore images
    """

    def __init__(self, imagename, axis=0, maskname="", images=(), values=None,
                 coordsys=None, overwrite=True, ashdf5=False, mask=(),
                 shape=None, tileshape=()):
        coord = {}
        if not coordsys is None:
            coord = coordsys.dict()
        if isinstance(imagename, Image):
            # Create from the value returned by subimage, etc.
            Image.__init__ (self, imagename)
        else:
            opened = False
            if isinstance(imagename, tuple)  or  isinstance(imagename, list):
                if len(imagename) == 0:
                    raise ValueError('No images given in list or tuple');
                if isinstance(imagename[0], str):
                    # Concatenate from image names
                    Image.__init__ (self, imagename, axis)
                    opened = True
                elif isinstance(imagename[0], image):
                    # Concatenate from image objects
                    Image.__init__ (self, imagename, axis, 0, 0)
                    opened = True
            if not opened:
                if not isinstance(imagename, str):
                    raise ValueError("first argument must be name or sequence of images or names")
                if shape is None:
                    if values is None:
                        # Open an image from name or expression
                        # Copy the tables argument and make sure it is a list
                        imgs = []
                        for img in images:
                            imgs += [img]
                        try:
                            # Substitute possible $ arguments
                            from pyrap.util import substitute
                            imagename = substitute(imagename, [(image, '', imgs)])
                        except:
                            print "Probably could not import pyrap.util"
                            pass
                        Image.__init__ (self, imagename, maskname, imgs)
                    else:
                        # Create an image from an array
                        # The values can be a masked array;
                        #  use the mask if no explicit mask is given
                        if isinstance(values, numpy.core.ma.MaskedArray):
                            if len(mask) == 0:
                                mask = numpy.core.ma.getmaskarray(values)
                            values = values.data
                        if len(mask) > 0:
                            mask = -mask;  # casa and numpy have opposite flags
                        Image.__init__ (self, values, mask, coord,
                                        imagename, overwrite, ashdf5,
                                        maskname, tileshape)
                else:
                    # Create an image from a shape (values gives the data type)
                    # default type is float.
                    if values is None:
                        values = float(0)
                    Image.__init__ (self, shape, values, coord,
                                    imagename, overwrite, ashdf5,
                                    maskname, tileshape, 0)

    def __str__ (self):
        return self.name();

    def __len__ (self):
        return self.size();

    def coordinates(self):
        return coordinatesystem(Image.coordinates(self))

    def getdata (self, blc=(), trc=(), inc=()):
        return self._getdata (blc, trc, inc);

    # Negate the mask; in numpy True means invalid.
    def getmask (self, blc=(), trc=(), inc=()):
        return -self._getmask (blc, trc, inc);

    # Get data and mask;
    def get (self, blc=(), trc=(), inc=()):
        return numpy.core.ma.masked_array (self.getdata(blc,trc,inc),
                                           self.getmask(blc,trc,inc))

    def putdata (self, value, blc=(), trc=(), inc=()):
        return self._putdata (value, blc, inc);

    def putmask (self, value, blc=(), trc=(), inc=()):
        # casa and numpy have opposite flags
        return self._putmask (-value, blc, inc);

    def put (self, value, blc=(), trc=(), inc=()):
        if isinstance(value, numpy.core.ma.MaskedArray):
            self.putdata (value.data, blc, trc, inc);
            self.putmask (numpy.core.ma.getmaskarray(value), blc, trc, inc);
        else:
            self.putdata (value, blc, trc, inc);

    def info (self):
        return {'coordinates' : Image.coordinates(self),
                'imageinfo'   : self.imageinfo(),
                'miscinfo'    : self.miscinfo(),
                'unit'        : self.unit()
                }

    def saveas (self, filename, overwrite=True, hdf5=False,
                copymask=True, newmaskname="", newtileshape=()):
        self._saveas (filename, overwrite, hdf5,
                      copymask, newmaskname,
                      newtileshape)

    def _adaptAxes (self, axes):
        # If axes is a single integer value, turn it into a list.
        if isinstance(axes, int):
            axes = [axes]
        # ImageProxy expects Fortran-numbered axes.
        # So reverse the axes.
        n = self.ndim() - 1
        axout = []
        for i in range(len(axes),0,-1):
            axout += [n-axes[i-1]]
        return axout

    def statistics (self, axes=(), minMaxValues=(), exclude=False, robust=True):
        return self._statistics (self._adaptAxes(axes), "",
                                 minMaxValues, exclude, robust)

    def regrid (self, axes, coordsys, outname="", overwrite=True,
                outshape=(), interpolation="linear",
                decimate=10, replicate=False,
                refchange=True, forceregrid=False):
        return image(self._regrid (self._adaptAxes(axes),
                                   outname, overwrite,
                                   outshape, coordsys.dict(),
                                   interpolation, decimate, replicate,
                                   refchange, forceregrid))

    def subimage(self, blc=(), trc=(), inc=(), dropdegenerate=False):
        return image(Image.subimage(self, blc, trc, inc, dropdegenerate))
