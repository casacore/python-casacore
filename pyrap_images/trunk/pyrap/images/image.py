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

    def get (self, blc=(), trc=(), inc=()):
        return self._getdata (blc, trc, inc);

    def getmask (self, blc=(), trc=(), inc=()):
        return self._getmask (blc, trc, inc);

    def put (self, value, blc=(), trc=(), inc=()):
        return self._putdata (value, blc, inc);

    def info (self):
        return {'coordinates' : self.coordinates(),
                'imageinfo'   : self.imageinfo(),
                'miscinfo'    : self.miscinfo(),
                'unit'        : self.unit()
                }

    def coordinates(self):
        return coordinatesystem(Image.coordinates(self))
