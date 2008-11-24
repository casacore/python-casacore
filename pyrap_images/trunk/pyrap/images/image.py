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

from pyrap.images.coordinates import coordinatesystem

class image(Image):
    """
        The Python interface to casacore images
    """

    def __init__(self, imagenames, axis=0, mask="", images=()):
        opened = False
        if isinstance(imagenames, tuple)  or  isinstance(imagenames, list):
            if len(imagenames) == 0:
                raise ValueError('No images given in list or tuple');
            if isinstance(imagenames[0], str):
                # Concatenate from image names
                Image.__init__ (self, imagenames, axis)
                opened = True
            elif isinstance(imagenames[0], image):
                # Concatenate from image objects
                Image.__init__ (self, imagenames, axis, 0, 0)
                opened = True
        if not opened:
            # Open an image from name or expression or create from an array
            Image.__init__ (self, imagenames, mask, images)

    def __str__ (self):
        return self.name();
    
    def __len__ (self):
        return self.size();

    def coordinates(self):
        return coordinatesystem(Image.coordinates(self))

    def get (self, blc=(), trc=(), inc=()):
        return self._getdata (blc, trc, inc);

    def getmask (self, blc=(), trc=(), inc=()):
        return self._getmask (blc, trc, inc);

    def put (self, value, blc=(), trc=(), inc=()):
        return self._putdata (value, blc, inc);

    def info (self):
        return {'coordinates' : Image.coordinates(self),
                'imageinfo'   : self.imageinfo(),
                'miscinfo'    : self.miscinfo(),
                'unit'        : self.unit()
                }

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
                outshape=(), coordsys={}, interpolation="linear",
                decimate=10, replicate=False,
                refchange=True, forceregrid=False):
        return self._regrid (self._adaptAxes(axes),
                             outname, overwrite, outshape, coordsys,
                             interpolation, decimate, replicate,
                             refchange, forceregrid)
