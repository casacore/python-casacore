# image.py: Python image functions
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


from six import string_types, integer_types
from ._images import Image
import numpy
import numpy.ma as nma
from casacore.images.coordinates import coordinatesystem
import six


class image(Image):
    """The Python interface to casacore images.

    An image can be constructed in a variety of ways:

    - Opening an existing image. The image format is determined automatically
      and can be
      `casacore <http://casacore.googlecode.com>`_,
      `HDF5 <http://www.hdfgroup.org/HDF5>`_,
      `FITS <http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html>`_,
      or `MIRIAD <http://www.atnf.csiro.au/computing/software/miriad>`_.
      FITS and MIRIAD always have data type float, but casacore and HDF5 images
      can have data type float, double, complex, or dcomplex.
    - Open an image expression by giving a `LEL expression
      <../../casacore/doc/notes/223.html>`_ string.
      Note that in an expression `$im` can be used similar to TaQL commands
      (see function :func:`tables.taql`).
    - Create a new temporary image from a shape or a numpy array.
    - Virtually concatenate a number of images along a given axis. This can
      be used to form a spectral line image cube from separate channel images.

    The following arguments can be given:

    `imagename`
      | It can be given in several forms:
      | If it is a tuple or list, the image is opened as the virtual
        concatenation of the given image names or objects.
      | Otherwise it should be a string giving the image name (or expression).
        If argument `values` or `shape` is given, a new image with that name
        is created using the values or shape. If the name is empty, a temporary
        image is created which can be written later using :func:`saveas`.
      | Otherwise it is tried to open an existing image with that name.
      | If the open fails, it is opened as a LEL image expression.
    `axis`
      The axis number along which images have to be concatenated.
    `maskname`
      | The name of the mask to be used when opening an existing image. If not
        given, the default image mask is used.
      | If an image is created, a mask with this name is created.
    `images`
      Possible images objects to be used for $n arguments in an expression
      string.
    'values`
      If given, the image will be created and these values will be stored in it.
      It should be a numpy array or masked array. If it is a masked array,
      its mask acts as the `mask` argument described below.
      The data type of the image is derived from the array's data type.
    `coordsys`
      The coordinate system to be used when creating an image.
      If not given, an appropriate default coordnate system will be used.
    `overwrite`
      If False, an exception is raised if the new image file already exists.
      Default is True.
    `ashdf5`
      If True, the image is created in HDF5 format, otherwise in casacore
      format. Default is casacore format.
    `mask`
      | An optional mask to be stored in the image when creating the image.
        If a mask is given, but no maskname is given, the mask will get the
        name `mask0`.
      | The mask can also be given in argument `values` (see above).
      | Note that the casacore images use the convention that a mask value
        True means good and False means bad. However, numpy uses the opposite.
        Therefore the mask will be negated, so a numpy masked can be given
        directly.
    `shape`
      If given, the image will be created. If `values` is also given, its
      shape should match. If `values` is not given, an image with data type
      double will be created.
    `tileshape`
      Advanced users can give the tile shape to be used. See the
      :mod:`tables` module for more information about Tiled Storage Managers.

    For example::

      im = image('3c343.fits')          # open existing fits image
      im = image('a.img1 - a.img2')     # open as expression
      im = image(shape=(256,256))       # create temp image
      im = image('a', shape=(256,256))  # create image a

    """

    def __init__(self, imagename, axis=0, maskname="", images=(), values=None,
                 coordsys=None, overwrite=True, ashdf5=False, mask=(),
                 shape=None, tileshape=()):
        coord = {}
        if coordsys is not None:
            coord = coordsys.dict()
        if isinstance(imagename, Image):
            # Create from the value returned by subimage, etc.
            Image.__init__(self, imagename)
        else:
            opened = False
            if isinstance(imagename, tuple) or isinstance(imagename, list):
                if len(imagename) == 0:
                    raise ValueError('No images given in list or tuple')
                if isinstance(imagename[0], string_types):
                    # Concatenate from image names
                    Image.__init__(self, imagename, axis)
                    opened = True
                elif isinstance(imagename[0], image):
                    # Concatenate from image objects
                    Image.__init__(self, imagename, axis, 0, 0)
                    opened = True
            if not opened:
                if not isinstance(imagename, string_types):
                    raise ValueError("first argument must be name or" +
                                     " sequence of images or names")
                if shape is None:
                    if values is None:
                        # Open an image from name or expression
                        # Copy the tables argument and make sure it is a list
                        imgs = []
                        for img in images:
                            imgs += [img]
                        try:
                            # Substitute possible $ arguments
                            import casacore.util as cu
                            imagename = cu.substitute(imagename,
                                                      [(image, '', imgs)],
                                                      locals=cu.getlocals(3))
                        except:
                            six.print_("Probably could not import casacore.util")
                            pass
                        Image.__init__(self, imagename, maskname, imgs)
                    else:
                        # Create an image from an array
                        # The values can be a masked array
                        #  use the mask if no explicit mask is given
                        if isinstance(values, nma.MaskedArray):
                            if len(mask) == 0:
                                mask = nma.getmaskarray(values)
                            values = values.data
                        if len(mask) > 0:
                            mask = ~mask  # casa and numpy have opposite flags
                        Image.__init__(self, values, mask, coord,
                                       imagename, overwrite, ashdf5,
                                       maskname, tileshape)
                else:
                    # Create an image from a shape (values gives the data type)
                    # default type is float.
                    if values is None:
                        values = numpy.array([0], dtype='float32')[0]
                    Image.__init__(self, shape, values, coord,
                                   imagename, overwrite, ashdf5,
                                   maskname, tileshape, 0)

    def __str__(self):
        """Get image name."""
        return self.name(strippath=True)

    def __len__(self):
        """Get nr of pixels in the image."""
        return self._size()

    def ispersistent(self):
        """Test if the image is persistent, i.e. stored on disk."""
        return self._ispersistent()

    def name(self, strippath=False):
        """Get image name."""
        return self._name(strippath)

    def shape(self):
        """Get image shape."""
        return self._shape()

    def ndim(self):
        """Get dimensionality of the image."""
        return self._ndim()

    def size(self):
        """Get nr of pixels in the image."""
        return self._size()

    def datatype(self):
        """Get data type of the image."""
        return self._datatype()

    def imagetype(self):
        """Get image type of the image (PagedImage, HDF5Image, etc.)."""
        return self._imagetype()

    def attrgroupnames(self):
        """Get the names of all attribute groups."""
        return self._attrgroupnames()

    def attrcreategroup(self, groupname):
        """Create a new attribute group."""
        self._attrcreategroup(groupname)

    def attrnames(self, groupname):
        """Get the names of all attributes in this group."""
        return self._attrnames(groupname)

    def attrnrows(self, groupname):
        """Get the number of rows in this attribute group."""
        return self._attrnrows(groupname)

    def attrget(self, groupname, attrname, rownr):
        """Get the value of an attribute in the given row in a group."""
        return self._attrget(groupname, attrname, rownr)

    def attrgetcol(self, groupname, attrname):
        """Get the value of an attribute for all rows in a group."""
        values = []
        for rownr in range(self.attrnrows(groupname)):
            values.append(self.attrget(groupname, attrname, rownr))
        return values

    def attrfindrows(self, groupname, attrname, value):
        """Get the row numbers of all rows where the attribute matches the given value."""
        values = self.attrgetcol(groupname, attrname)
        return [i for i in range(len(values)) if values[i] == value]

    def attrgetrow(self, groupname, key, value=None):
        """Get the values of all attributes of a row in a group.

        If the key is an integer, the key is the row number for which
        the attribute values have to be returned.

        Otherwise the key has to be a string and it defines the name of an
        attribute. The attribute values of the row for which the key matches
        the given value is returned.
        It can only be used for unique attribute keys. An IndexError exception
        is raised if no or multiple matches are found.
        """
        if not isinstance(key, string_types):
            return self._attrgetrow(groupname, key)
        # The key is an attribute name whose value has to be found.
        rownrs = self.attrfindrows(groupname, key, value)
        if len(rownrs) == 0:
            raise IndexError("Image attribute " + key + " in group " +
                             groupname + " has no matches for value " +
                             str(value))
        if len(rownrs) > 1:
            raise IndexError("Image attribute " + key + " in group " +
                             groupname + " has multiple matches for value " +
                             str(value))
        return self._attrgetrow(groupname, rownrs[0])

    def attrgetunit(self, groupname, attrname):
        """Get the unit(s) of an attribute in a group."""
        return self._attrgetunit(groupname, attrname)

    def attrgetmeas(self, groupname, attrname):
        """Get the measinfo (type, frame) of an attribute in a group."""
        return self._attrgetmeas(groupname, attrname)

    def attrput(self, groupname, attrname, rownr, value, unit=[], meas=[]):
        """Put the value and optionally unit and measinfo
           of an attribute in a row in a group."""
        return self._attrput(groupname, attrname, rownr, value, unit, meas)

    def getdata(self, blc=(), trc=(), inc=()):
        """Get image data.

        Using the arguments blc (bottom left corner), trc (top right corner),
        and inc (stride) it is possible to get a data slice.

        The data is returned as a numpy array. Its dimensionality is the same
        as the dimensionality of the image, even if an axis has length 1.

        """
        return self._getdata(self._adjustBlc(blc),
                             self._adjustTrc(trc),
                             self._adjustInc(inc))

    # Negate the mask; in numpy True means invalid.
    def getmask(self, blc=(), trc=(), inc=()):
        """Get image mask.

        Using the arguments blc (bottom left corner), trc (top right corner),
        and inc (stride) it is possible to get a mask slice. Not all axes
        need to be specified. Missing values default to begin, end, and 1.

        The mask is returned as a numpy array. Its dimensionality is the same
        as the dimensionality of the image, even if an axis has length 1.
        Note that the casacore images use the convention that a mask value
        True means good and False means bad. However, numpy uses the opposite.
        Therefore the mask will be negated, so it can be used directly in
        numpy operations.

        If the image has no mask, an array will be returned with all values
        set to False.

        """
        return numpy.logical_not(self._getmask(self._adjustBlc(blc),
                                               self._adjustTrc(trc),
                                               self._adjustInc(inc)))

    # Get data and mask
    def get(self, blc=(), trc=(), inc=()):
        """Get image data and mask.

        Get the image data and mask (see ::func:`getdata` and :func:`getmask`)
        as a numpy masked array.

        """
        return nma.masked_array(self.getdata(blc, trc, inc),
                                self.getmask(blc, trc, inc))

    def putdata(self, value, blc=(), trc=(), inc=()):
        """Put image data.

        Using the arguments blc (bottom left corner), trc (top right corner),
        and inc (stride) it is possible to put a data slice. Not all axes
        need to be specified. Missing values default to begin, end, and 1.

        The data should be a numpy array. Its dimensionality must be the same
        as the dimensionality of the image.

        """
        return self._putdata(value, self._adjustBlc(blc),
                             self._adjustInc(inc))

    def putmask(self, value, blc=(), trc=(), inc=()):
        """Put image mask.

        Using the arguments blc (bottom left corner), trc (top right corner),
        and inc (stride) it is possible to put a data slice. Not all axes
        need to be specified. Missing values default to begin, end, and 1.

        The data should be a numpy array. Its dimensionality must be the same
        as the dimensionality of the image.
        Note that the casacore images use the convention that a mask value
        True means good and False means bad. However, numpy uses the opposite.
        Therefore the mask will be negated, so a numpy masked can be given
        directly.

        The mask is not written if the image has no mask and if it the entire
        mask is False. In that case the mask most likely comes from a getmask
        operation on an image without a mask.

        """
        # casa and numpy have opposite flags
        return self._putmask(~value, self._adjustBlc(blc),
                             self._adjustInc(inc))

    def put(self, value, blc=(), trc=(), inc=()):
        """Put image data and mask.

        Put the image data and optionally the mask (see ::func:`getdata`
        and :func:`getmask`).
        If the `value` argument is a numpy masked array, but data and mask will
        bw written. If it is a normal numpy array, only the data will be
        written.

        """
        if isinstance(value, nma.MaskedArray):
            self.putdata(value.data, blc, trc, inc)
            self.putmask(nma.getmaskarray(value), blc, trc, inc)
        else:
            self.putdata(value, blc, trc, inc)

    def haslock(self, write=False):
        """Test if the image holds a read or write lock.

        | See `func:`tables.table.haslock` for more information.
        | Locks are only used for images in casacore format. For other formats
          (un)locking is a no-op, so this method always returns True.

        """
        return self._haslock(write)

    def lock(self, write=False, nattempts=0):
        """Acquire a read or write lock on the image.

        | See `func:`tables.table.haslock` for more information.
        | Locks are only used for images in casacore format. For other formats
          (un)locking is a no-op, so this method always returns True.

        Only advanced users should use locking. In normal operations
        explicit locking and unlocking is not necessary.

        """
        return self._lock(write, nattempts)

    def unlock(self):
        """Release a lock on the image.

        | See `func:`tables.table.haslock` for more information.
        | Locks are only used for images in casacore format. For other formats
          (un)locking is a no-op, so this method always returns True.

        """
        return self._unlock()

    def subimage(self, blc=(), trc=(), inc=(), dropdegenerate=True):
        """Form a subimage.

        An image object containing a subset of an image is returned.
        The arguments blc (bottom left corner), trc (top right corner),
        and inc (stride) define the subset. Not all axes need to be specified.
        Missing values default to begin, end, and 1.

        By default axes with length 1 are left out.

        A subimage is a so-called virtual image. It is not stored, but only
        references the original image. It can be made persistent using the
        :func:`saveas` method.

        """
        return image(self._subimage(self._adjustBlc(blc),
                                    self._adjustTrc(trc),
                                    self._adjustInc(inc),
                                    dropdegenerate))

    def coordinates(self):
        """Get the :class:`coordinatesystem` of the image."""
        return coordinatesystem(self._coordinates())

    def toworld(self, pixel):
        """Convert the pixel coordinates of an image value to world coordinates.

        The coordinates must be given with the slowest varying axis first.
        Thus normally like frequency(,polarisation axis),Dec,Ra.

        """
        return self._toworld(pixel, True)

    def topixel(self, world):
        """Convert the world coordinates of an image value to pixel coordinates.

        The coordinates must be given with the slowest varying axis first.
        Thus normally like frequency(,polarisation axis),Dec,Ra.

        """
        return self._topixel(world, True)

    def imageinfo(self):
        """Get the standard image info."""
        return self._imageinfo()

    def miscinfo(self):
        """Get the auxiliary image info."""
        return self._miscinfo()

    def unit(self):
        """Get the pixel unit of the image."""
        return self._unit()

    def history(self):
        """Get the image processing history."""
        return self._history()

    def info(self):
        """Get coordinates, image info, and unit"."""
        return {'coordinates': self._coordinates(),
                'imageinfo': self._imageinfo(),
                'miscinfo': self._miscinfo(),
                'unit': self._unit()
                }

    def tofits(self, filename, overwrite=True, velocity=True,
               optical=True, bitpix=-32, minpix=1, maxpix=-1):
        """Write the image to a file in FITS format.

        `filename`
          FITS file name
        `overwrite`
          If False, an exception is raised if the new image file already exists.
          Default is True.
        `velocity`
          By default a velocity primary spectral axis is written if possible.
        `optical`
          If writing a velocity, use the optical definition
          (otherwise use radio).
        `bitpix`
          can be set to -32 (float) or 16 (short) only. When `bitpix` is
          16 it will write BSCALE and BZERO into the FITS file. If minPix
        `minpix` and `maxpix`
          are used to determine BSCALE and BZERO if `bitpix=16`.
          If `minpix` is greater than `maxpix` (which is the default),
          the minimum and maximum pixel values will be determined from the ddta.
          Oherwise the supplied values will be used and pixels outside that
          range will be clipped to the minimum and maximum pixel values.
          Note that this truncation does not occur for `bitpix=-32`.

        """
        return self._tofits(filename, overwrite, velocity, optical,
                            bitpix, minpix, maxpix)

    def saveas(self, filename, overwrite=True, hdf5=False,
               copymask=True, newmaskname="", newtileshape=()):
        """Write the image to disk.

        Note that the created disk file is a snapshot, so it is not updated
        for possible later changes in the image object.

        `overwrite`
          If False, an exception is raised if the new image file already exists.
          Default is True.
        `ashdf5`
          If True, the image is created in HDF5 format, otherwise in casacore
          format. Default is casacore format.
        `copymask`
          By default the mask is written as well if the image has a mask.
        'newmaskname`
          If the mask is written, the name is the same the original or
          `mask0` if the original mask has no name. Using this argument a
          different mask name can be given.
        `tileshape`
          Advanced users can give a new tile shape. See the :mod:`tables`
          module for more information about Tiled Storage Managers.

        """
        self._saveas(filename, overwrite, hdf5,
                     copymask, newmaskname,
                     newtileshape)

    def statistics(self, axes=(), minmaxvalues=(), exclude=False, robust=True):
        """Calculate statistics for the image.

        Statistics are returned in a dict for the given axes.
        E.g. if axes [0,1] is given in a 3-dim image, the statistics are
        calculated for each plane along the 3rd axis. By default statistics
        are calculated for the entire image.

        `minmaxvalues` can be given to include or exclude pixels
        with values in the given range. If only one value is given,
        min=-abs(val) and max=abs(val).

        By default robust statistics (Median, MedAbsDevMed, and Quartile) are
        calculated too.
        """
        return self._statistics(self._adaptAxes(axes), "",
                                minmaxvalues, exclude, robust)

    def regrid(self, axes, coordsys, outname="", overwrite=True,
               outshape=(), interpolation="linear",
               decimate=10, replicate=False,
               refchange=True, forceregrid=False):
        """Regrid the image to a new image object.

         Regrid the image on the given axes to the given coordinate system.
         The output is stored in the given file; it no file name is given a
         temporary image is made.
         If the output shape is empty, the old shape is used.
         `replicate=True` means replication rather than regridding.

        """
        return image(self._regrid(self._adaptAxes(axes),
                                  outname, overwrite,
                                  outshape, coordsys.dict(),
                                  interpolation, decimate, replicate,
                                  refchange, forceregrid))

    def view(self, tempname='/tmp/tempimage'):
        """Display the image using casaviewer.

        If the image is not persistent, a copy will be made that the user
        has to delete once viewing has finished. The name of the copy can be
        given in argument `tempname`. Default is '/tmp/tempimage'.

        """
        import os
        # Test if casaviewer can be found.
        # On OS-X 'which' always returns 0, so use test on top of it.
        if os.system('test -x `which casaviewer` > /dev/null 2>&1') == 0:
            six.print_("Starting casaviewer in the background ...")
            self.unlock()
            if self.ispersistent():
                os.system('casaviewer ' + self.name() + ' &')
            elif len(tempname) > 0:
                six.print_("  making a persistent copy in " + tempname)
                six.print_("  which should be deleted after the viewer has ended")
                self.saveas(tempname)
                os.system('casaviewer ' + tempname + ' &')
            else:
                six.print_("Cannot view because the image is in memory only.")
                six.print_("You can browse a persistent copy of the image like:")
                six.print_("   t.view('/tmp/tempimage')")
        else:
            six.print_("casaviewer cannot be found")

    def _adaptAxes(self, axes):
        # If axes is a single integer value, turn it into a list.
        if isinstance(axes, integer_types):
            axes = [axes]
        # ImageProxy expects Fortran-numbered axes.
        # So reverse the axes.
        n = self.ndim() - 1
        axout = []
        for i in range(len(axes), 0, -1):
            axout += [n - axes[i - 1]]
        return axout

    def _adjust(self, val, defval):
        retval = defval
        if isinstance(val, tuple) or isinstance(val, list):
            retval[0:len(val)] = val
        else:
            retval[0] = val
        return retval

    # Append blc with 0 if shorter than shape.
    def _adjustBlc(self, blc):
        shp = self._shape()
        return self._adjust(blc, [0 for x in shp])

    # Append trc with shape-1 if shorter than shape.
    def _adjustTrc(self, trc):
        shp = self._shape()
        return self._adjust(trc, [x - 1 for x in shp])

    # Append inc with 1 if shorter than shape.
    def _adjustInc(self, inc):
        shp = self._shape()
        return self._adjust(inc, [1 for x in shp])
