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

    def __init__(self, imagename, axis=0, mask="", images=()):
        if isinstance(imagename, Image):
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
                # Open an image from name or expression or create from an array
                # Copy the tables argument and make sure it is a list
                imgs = []
                for img in images:
                    imgs += [img]
                try:
                    from pyrap.util import substitute
                    imagename = substitute(imagename, [(image, '', imgs)])
                except:
                    pass
                Image.__init__ (self, imagename, mask, imgs)

    def __str__ (self):
        return self.name();
    
    def __len__ (self):
        return self.size();

    def coordinates(self):
        return coordinatesystem(Image.coordinates(self))

    def getdata (self, blc=(), trc=(), inc=()):
        return self._getdata (blc, trc, inc);

    def getmask (self, blc=(), trc=(), inc=()):
        return self._getmask (blc, trc, inc);

    # Get data and mask; negate mask as for numpy True is invalid.
    def get (self, blc=(), trc=(), inc=()):
        return numpy.core.ma.masked_array (self.getdata(blc,trc,inc),
                                           -self.getmask(blc,trc,inc))

    def put (self, value, blc=(), trc=(), inc=()):
        return self._putdata (value, blc, inc);

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

    def regrid (self, axes, outname="", overwrite=True,
                outshape=(), coordsys=None, interpolation="linear",
                decimate=10, replicate=False,
                refchange=True, forceregrid=False):
        return image(self._regrid (self._adaptAxes(axes),
                                   outname, overwrite,
                                   outshape, coordsys.dict(),
                                   interpolation, decimate, replicate,
                                   refchange, forceregrid))

    def subimage(self, blc=(), trc=(), inc=(), dropdegenerate=False):
        return image(Image.subimage(self, blc, trc, inc, dropdegenerate))
