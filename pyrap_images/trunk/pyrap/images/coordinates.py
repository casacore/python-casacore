# image.py: Python coordinate system wrapper
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
# $Id: $

import string
import numpy

class coordinatesystem(object):
    """
    A thin wrapper for casacore coordinate systems. It disects the 
    coordinatesystem record return from casacore images.
    This only handles one instance of each coordinate type.
    It uses reference semantics for the individual coordinates,
    e.g. following will work:
    
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
        for coord in self._names:
            out += str(self.get_coordinate(coord))
        return out

    def summary(self):
        print str(self)

    def _get_coordinatenames(self):
        """Create order list of coordinate names
        """
        validnames = ("direction", "spectral", "linear", "stokes", "tabular")
        self._names = [""] * len(validnames)
        n = 0
        for key in self._csys.keys():
            for name in validnames:
                if key.startswith(name):
                    idx = int(key[len(name):])
                    self._names[idx] = name
                    n +=1
        self._names = self._names[:n]
        if len(self._names) == 0:
            raise LookupError("Coordinate record doesn't contain valid coordinates")

    def __getitem__(self, name):
        i = self._names.index(name)
        return eval("%scoordinate(self._csys['%s'])" % (name, name+str(i)))

    # alias
    get_coordinate = __getitem__

    def __setitem__(self, name, val):
        i = self._names.index(name)
        assert isinstance(val, eval("%scoordinate" % name))
        self._csys[key+str(i)] = val._coord

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
        out = []
        for name in self._names:
            out.append(self.get_coordinate(name).get_referencepixel())
        return out

    def set_referencepixel(self, values):
        for i,name in enumerate(self._names):
            self.get_coordinate(name).set_referencepixel(values[i])

    def get_referencevalue(self):
        out = []
        for name in self._names:
            out.append(self.get_coordinate(name).get_referencevalue())
        return out

    def set_referencevalue(self, values):
        for i,name in enumerate(self._names):
            self.get_coordinate(name).set_referencevalue(values[i])

    def get_increment(self):
        out = []
        for name in self._names:
            out.append(self.get_coordinate(name).get_increment())
        return out

    def set_increment(self, values):
        for i,name in enumerate(self._names):
            self.get_coordinate(name).set_increment(values[i])

    def get_unit(self):
        out = []
        for name in self._names:
            out.append(self.get_coordinate(name).get_unit())
        return out

    def get_axes(self):
        out = []
        for name in self._names:
            out.append(self.get_coordinate(name).get_axes())
        return out


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

    def get_referencepixel(self):
        return self._coord.get("crpix", None)

    def set_referencepixel(self, pix):
        assert len(pix) == len(self._coord["crpix"])
        self._coord["crpix"] = pix[:]

    def get_referencevalue(self):
        return self._coord.get("crval", None)

    def set_referencevalue(self, val):
        assert len(val) == len(self._coord["crval"])
        self._coord["crval"] = val[:]

    def get_increment(self):
        return self._coord.get("cdelt", None)

    def set_increment(self, inc):
        self._coord["cdelt"] = inc
    
    def get_unit(self):
        return self._coord.get("units", None)

    def get_axes(self):
        return self._coord.get("axes", None)


class directioncoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

    def __str__(self):
        out = coordinate.__str__(self)
        out += self._template % ("Frame", str(self.get_frame()))
        out += self._template % ("Projection", str(self.get_projection()))
        return out
        
    def get_projection(self):
        return self._coord.get("projection", None)

    def get_frame(self):
       return self._coord.get("system", None)

    def set_frame(self, val):
        # maybe uses measures here
        #dm = measures();knonwframes = dm.listcodes(dm.direction())["normal"]
        knownframes = ["GALACTIC", "J2000"] # etc
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

    def get_frame(self):
       return self._coord.get("system", None)

    def set_frame(self, val):
        # maybe uses measures here
        #dm = measures();knonwframes = dm.listcodes(dm.frequency())["normal"]
        knownframes = ["BARY", "LSRK"] 
        assert val.upper() in knownframes
        self._coord["system"] = val.upper()

    def get_conversion(self):
        return self._coord.get("conversion", None)

    def set_conversion(self, key, val):
        assert self._coord.has_key(key)
        self._coord["conversion"][key] = val

class linearcoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

class stokescoordinate(coordinate):
    def __init__(self, rec):
        coordinate.__init__(self, rec)

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

