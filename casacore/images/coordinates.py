# coordinates.py: Python coordinate system wrapper
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

import six


class coordinatesystem(object):
    """
    A thin wrapper for casacore coordinate systems. It dissects the
    coordinatesystem record returned from casacore images.
    This only handles one instance of each coordinate type.
    The possible types are ''direction'', ''spectral'', ''stokes'',
    ''linear'' and ''tabular''.
     The first, second, trird and fourth axis are respectively,
     'Right Ascension','Declination','Stokes' and 'Frequency'.
     To make a coordinate object, these things should be taken care
     of.Like to make a spectral coordinate, a 4D image should be used
     as the 4th axis is 'Frequency' and so on.

    It uses reference semantics for the individual coordinates,
    e.g. the following will work::

      cs = im.coordinates()
      cs["direction"].set_referencepixel([0.0,0.0])
      # or equivalent
      cs.get_coordinates("direction").set_referencepixel([0.0,0.0])

    """

    def __init__(self, rec):
        self._csys = rec
        self._names = []
        self._get_coordinatenames()

    def __str__(self):
        out = ""
        for coord in self:
            out += str(coord)
        return out

    def dict(self):
        return self._csys

    def summary(self):
        six.print_(str(self))

    def _get_coordinatenames(self):
        """Create ordered list of coordinate names
        """
        validnames = ("direction", "spectral", "linear", "stokes", "tabular")
        self._names = [""] * len(validnames)
        n = 0
        for key in self._csys.keys():
            for name in validnames:
                if key.startswith(name):
                    idx = int(key[len(name):])
                    self._names[idx] = name
                    n += 1
        # reverse as we are c order in python
        self._names = self._names[:n][::-1]

        if len(self._names) == 0:
            raise LookupError("Coordinate record doesn't contain valid coordinates")

    def get_names(self):
        """Get the coordinate names
        """
        return self._names

    def __getitem__(self, name):
        # reverse index back to fortran order as the record is using this
        i = self._names[::-1].index(name)
        return eval("%scoordinate(self._csys['%s'])" % (name, name + str(i)))

    # alias
    get_coordinate = __getitem__

    def __setitem__(self, name, val):
        # reverse index back to fortran order as the record is using this
        i = self._names[::-1].index(name)
        assert isinstance(val, eval("%scoordinate" % name))
        self._csys[name + str(i)] = val._coord

    # alias
    set_coordinate = __setitem__

    def __iter__(self):
        for name in self._names:
            yield self.get_coordinate(name)

    def get_obsdate(self):
        return self._csys.get("obsdate", None)

    def get_observer(self):
        return self._csys.get("observer", None)

    def get_telescope(self):
        return self._csys.get("telescope", None)

    def get_referencepixel(self):
        return [coord.get_referencepixel() for coord in self]

    def set_referencepixel(self, values):
        for i, coord in enumerate(self):
            coord.set_referencepixel(values[i])

    def get_referencevalue(self):
        return [coord.get_referencevalue() for coord in self]

    def set_referencevalue(self, values):
        for i, coord in enumerate(self):
            coord.set_referencevalue(values[i])

    def get_increment(self):
        return [coord.get_increment() for coord in self]

    def set_increment(self, values):
        for i, coord in enumerate(self):
            coord.set_increment(values[i])

    def get_unit(self):
        return [coord.get_unit() for coord in self]

    def get_axes(self):
        return [coord.get_axes() for coord in self]


class coordinate(object):
    """Overwrite as neccessary
    """

    def __init__(self, rec):
        self._coord = rec
        self._template = " %-16s: %s\n"

    def __str__(self):
        lname = self.__class__.__name__.capitalize()
        out = "%s Coordinate:\n" % lname[:-10]
        out += self._template % ("Reference Pixel",
                                 str(self.get_referencepixel()))
        out += self._template % ("Reference Value",
                                 str(self.get_referencevalue()) \
                                 + " " + str(self.get_unit()))
        out += self._template % ("Increment",
                                 str(self.get_increment()) \
                                 + " " + str(self.get_unit()))
        return out

    def dict(self):
        """Get the coordinate info as a dict"""
        return self._coord

    def get_axis_size(self, axis=0):
        """Get the length of the given axis in this coordinate

        -1 is returned if unknown.
        """
        try:
            return self._coord["_axes_sizes"][axis]
        except:
            return -1

    def get_image_axis(self, axis=0):
        """Get the image axis number of the given axis in this coordinate

        -1 is returned if unknown.
        """
        try:
            return self._coord["_image_axes"][axis]
        except:
            return -1

    # ALL list/array values have to be reversed as the coordsys dict holds

    # everything in fortran order.

    def get_referencepixel(self):
        """Get the reference pixel of the given axis in this coordinate."""
        return self._coord.get("crpix", [])[::-1]

    def set_referencepixel(self, pix):
        """Set the reference pixel of the given axis in this coordinate."""
        assert len(pix) == len(self._coord["crpix"])
        self._coord["crpix"] = pix[::-1]

    def get_referencevalue(self):
        """Get the reference value of the given axis in this coordinate."""
        return self._coord.get("crval", [])[::-1]

    def set_referencevalue(self, val):
        """Set the reference pixel of the given axis in this coordinate."""
        assert len(val) == len(self._coord["crval"])
        self._coord["crval"] = val[::-1]

    def get_increment(self):
        """Get the increment of the given axis in this coordinate."""
        return self._coord.get("cdelt", [])[::-1]

    def set_increment(self, inc):
        """Set the increment of the given axis in this coordinate."""
        self._coord["cdelt"] = inc[::-1]

    def get_unit(self):
        """Get the unit of the given axis in this coordinate."""
        return self._coord.get("units", [])[::-1]

    def get_axes(self):
        """Get the axes in this coordinate."""
        return self._coord.get("axes", [])[::-1]


class directioncoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

    def __str__(self):
        out = coordinate.__str__(self)
        out += self._template % ("Frame", str(self.get_frame()))
        out += self._template % ("Projection", str(self.get_projection()))
        return out

    def get_projection(self):
        """Get the projection of the given axis in this coordinate."""
        return self._coord.get("projection", None)

    def set_projection(self, val):
        """Set the projection of the given axis in this coordinate.

        The known projections are SIN, ZEA, TAN, NCP, AIT, ZEA
        """
        knownproj = ["SIN", "ZEA", "TAN", "NCP", "AIT", "ZEA"]  # etc
        assert val.upper() in knownproj
        self._coord["projection"] = val.upper()

    def get_frame(self):
        return self._coord.get("system", None)

    def set_frame(self, val):
        # maybe uses measures here
        # dm = measures();knonwframes = dm.list_codes(dm.direction())["normal"]
        knownframes = ["GALACTIC", "J2000", "B1950", "SUPERGAL"]  # etc
        assert val.upper() in knownframes
        self._coord["system"] = val.upper()


class spectralcoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

    def __str__(self):
        out = coordinate.__str__(self)
        out += self._template % ("Frame", str(self.get_frame()))
        out += self._template % ("Rest Frequency",
                                 str(self.get_restfrequency()) + " Hz")
        return out

    def get_unit(self):
        return self._coord.get("unit", None)

    def get_referencepixel(self):
        return self._coord["wcs"].get("crpix", None)

    def set_referencepixel(self, pix):
        self._coord["wcs"]["crpix"] = pix

    def get_referencevalue(self):
        return self._coord["wcs"].get("crval", None)

    def set_referencevalue(self, val):
        self._coord["wcs"]["crval"] = val

    def get_increment(self):
        return self._coord["wcs"].get("cdelt", None)

    def set_increment(self, inc):
        self._coord["wcs"]["cdelt"] = inc

    def get_axes(self):
        return self._coord.get("name", None)

    def get_restfrequency(self):
        return self._coord.get("restfreq", None)

    def set_restfrequency(self, val):
        self._coord["restfreq"] = val

    def get_frame(self):
        return self._coord.get("system", None)

    def set_frame(self, val):
        # maybe uses measures here
        # dm = measures();knonwframes = dm.list_codes(dm.frequency())["normal"]
        knownframes = ["BARY", "LSRK", "TOPO"]
        assert val.upper() in knownframes
        self._coord["system"] = val.upper()

    def get_conversion(self):
        return self._coord.get("conversion", None)

    def set_conversion(self, key, val):
        assert key in self._coord
        self._coord["conversion"][key] = val


class linearcoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)


class stokescoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

    def get_stokes(self):
        return self._coord["stokes"]


class tabularcoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

    def get_pixelvalues(self):
        return self._coord["pixelvalues"]

    def set_pixelvalues(self, val):
        assert len(val) == len(self._coord["pixelvalues"])
        self._coord["pixelvalues"] = val

    def get_worldvalues(self):
        return self._coord["worldvalues"]

    def set_worldvalues(self, val):
        assert len(val) == len(self._coord["worldvalues"])
        self._coord["worldvalues"] = val
