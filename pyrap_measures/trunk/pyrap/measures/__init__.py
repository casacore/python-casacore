# __init__.py: Top level .py file for python measures interface
# Copyright (C) 2006
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
# $Id: __init__.py,v 1.2 2006/12/04 04:01:03 mmarquar Exp $
__all__ = ['is_measure', 'measures']

import os
import pyrap.quanta as dq
from  _measures import measures as _measures

if os.environ.has_key("MEASURESDATA"):
    if not os.environ.has_key("AIPSPATH"):
        os.environ["AIPSPATH"] = "%s dummy dummy" %  os.environ["MEASURESDATA"]

def is_measure(v):
    """
    Return if this is a true measures dictionary

    :param v: The object to check
    """
    if isinstance(v, dict) and v.has_key("type") and  v.has_key("m0"):
        return True
    return False

def _check_valid_offset(self, mtype):
    if not off['type'] == mtype:
        raise TypeError('Illegal offset type specified.')        
    

class measures(_measures):
    """The measures server object. This should be used to set frame 
    information and create the various measures and do conversion on them.

    The measures types are:
    
    * :func:`measures.direction`
    
    * :func:`measures.position`
    
    * :func:`measures.epoch`

    * :func:`measures.frequency`

    * :func:`measures.doppler`

    * :func:`measures.baseline`    

    Typical usage::
        from pyrap.measures import measures
        dm = measures() # create measures server instance
        dirmeas = dm.direction()
      
    """
    def __init__(self):
        _measures.__init__(self)
        self._framestack = {}

    def set_data_path(self, pth):
        """Set the location of the measures data 

        :param pth: The absolute path to the data directory.
        """
        if os.path.exists(pth):
            os.environ["AIPSPATH"] = "%s dummy dummy" % pth

    def measure(self, v, rf, off=None):
        """Create/convert a measure using the frame state set on the measures 
        server instance.
        
        :param v: The measure to convert

        :param rf: The frame reference to convert to
        
        :param off: The optional offset for the measure

        """
        if off is None: off = {}
        keys = ["m0", "m1", "m2"]
        for key in keys:
            if key in v:
                if dq.is_quantity(v[key]):
                    v[key] = v[key].to_dict()
        return _measures.measure(self, v, rf, off)

    def direction(self, rf='', v0='0..', v1='90..', off=None):
        loc = { 'type': 'direction' , 'refer':  rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        if is_measure(off):
            if not off['type'] == "direction":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)
        
    def position(self, rf='', v0='0..', v1='90..', v2='0m', off=None):
        loc = { 'type': 'position' , 'refer':  rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "position":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def epoch(self, rf='', v0='0.0d', off=None):
        loc = { 'type': 'epoch' , 'refer':  rf}
        loc['m0'] = dq.quantity(v0)
        if is_measure(off):
            if not off['type'] == "epoch":
                raise TypeError('Illegal offset type specified.')        
            loc["offset"] = off
        return self.measure(loc, rf)

    def frequency(self, rf='', v0='0Hz', off=None):
        loc = { 'type': "frequency",
                'refer': rf,
                'm0': dq.quantity(v0) }
        if is_measure(off):
            if not off['type'] == "frequency":
                raise TypeError('Illegal offset type specified.')        
            loc["offset"] = off
        return self.measure(loc, rf)

    def doppler(self, rf='', v0='0', off=None):
        loc = { 'type': "doppler",
                'refer': rf,
                'm0': dq.quantity(v0) }
        if is_measure(off):
            if not off['type'] == "doppler":
                raise TypeError('Illegal offset type specified.')        
            loc["offset"] = off
        return self.measure(loc, rf)

    def radialvelocity(self, rf='', v0='0m/s', off=None):
        loc = { 'type': "radialvelocity",
                'refer': rf,
                'm0': dq.quantity(v0) }
        if is_measure(off):
            if not off['type'] == "radialvelocity":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def baseline(self, rf='', v0='0..', v1='', v2='', off=None):
        
        loc = { 'type': "baseline", 'refer': rf }
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "doppler":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def uvw(self, rf='', v0='0..', v1='', v2='', off=None):
        loc = { 'type': "uvw", 'refer': rf }
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "uvw":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)
       
    def earthmagnetic(self, rf='', v0='0G', v1='0..', v2='90..', off=None):
        loc = { 'type': "earthmagnetic", 'refer': rf }
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "earthmagnetic":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)
       

    def tofrequency(self, rf, v0, rfq):
        if is_measure(rfq) and rfq['type'] == 'frequency':
            rfq = dq.quantity(rfq['m0'])
        if is_measure(v0) and  v0['type'] == 'doppler' \
               and  dq.is_quantity(rfq) \
               and  rfq.conforms(dq.quantity('Hz')):
            return self.doptofreq(v0, rf, rfq.to_dict())
        else:
            raise TypeError('Illegal Doppler or rest frequency specified')

    def torestfrequency(self, v0, d0):
        if is_measure(v0) and  v0['type'] == 'frequency' \
               and is_measure(d0) and d0['type'] == 'doppler':
            return self.torest(v0, d0)
        else:
            raise TypeError('Illegal Doppler or rest frequency specified')
    to_restfrequency = torestfrequency

    def todoppler(self, rf, v0, rfq=False):
        if is_measure(rfq) and rfq['type'] == 'frequency':
            rfq = dq.quantity(rfq['m0'])
        if is_measure(v0):
            if v0['type'] == 'radialvelocity':
                return self.todop(v0, dq.quantity(1.,'Hz'))
            elif v0['type'] == 'frequency' and  dq.is_quantity(rfq) \
                    and rfq.conforms(dq.quantity('Hz')):
                return self.todop(v0, rfq)
            else:
                raise TypeError('Illegal Doppler or rest frequency specified')
        else:
            raise TypeError('Illegal Frequency specified')
    to_doppler = todoppler
   
    def toradialvelocity(self, rf, v0):
        if is_measure(v0) and v0['type'] == 'doppler':
            return self.doptorv(rf, v0)
        else:
            raise TypeError('Illegal Doppler specified')
    to_radialvelocity = toradialvelocity

    def touvw(self, v):
        if is_measure(v) and v['type'] == 'baseline':
           return _measures.uvw(self, v)
        else:
            raise TypeError('Illegal Baseline specified')
    to_uvm = touvw
        
    def expand(self, v):
        """Calculates the differences between a series of given measure values:
        it calculates baseline values from position values. 

        :params v: a measure (of type 'baseline', 'position' or 'uvw')
        :returns: a tuple with the first element being a measure
                  and the second a quantity containing the differences.
        
        Example::
            
            >>> from pyrap.quanta import quantity
            >>> x = quantity([10,50],'m')
            >>> y = quantity([20,100],'m')
            >>> z = quantity([30,150],'m')
            >>> sb = dm.baseline('itrf', x, y, z)
            >>> (sbex, xyz) = dm.expand(sb)
            >>> print xyz
            [40.000000000000014, 80.0, 120.0] m

        """ 
        if not is_measure(v) or v['type'] not in ['baseline', 
                                                  'position', 'uvw']:
            raise TypeError("Can only expand baselines, positions, or uvw")
        vw = v.copy()
        vw['type'] = "uvw"
        vw['refer'] = "J2000"
        out = _measures.expand(self, vw)
        xyz = None
        if 'xyz' in out:
            xyz = dq.quantity(out.pop('xyz'))
        outm = out.pop('r0')        
        outm['type'] = v['type']
        outm['refer'] = v['refer']
        return (outm, xyz)

    def asbaseline(self, pos):
        """Convert a position measure into a baseline measure. No actual 
        baseline is calculated, since operations can be done on positions, 
        with subtractions to obtain baselines at a later stage.
        
        :param pos: a position measure
        :returns: a baseline measure

        """
        if not is_measure(pos) or pos['type'] not in ['position', 'baseline']:
            raise TypeError('Argument is not a position/baseline measure')
        if pos['type'] == 'position':
            loc = self.measure(pos, 'itrf')
            loc['type'] = 'baseline'
            return self.measure(loc, 'j2000')
        return pos
    as_baseline = asbaseline
                
    def getvalue(self, v):
        """
        Return a list of quantities making up the measures' value.
        
        :param v: a measure
        """
        if  not is_measure(v):
            raise TypeError('Incorrect input type for getvalue()')
        import re
        rx = re.compile("m\d+")
        out = []
        keys = v.keys()[:]
        keys.sort()
        for key in keys:
            if re.match(rx, key):
                out.append(dq.quantity(v.get(key)))
        return out
    get_value = getvalue

    def get_type(self, m):
        """Get the type of the measure.

        :param m: a measure (dictionary)
        :rtype: string
        """
        if is_measure(m):
            return m["type"]
        else:
            raise TypeError("Argument is not a measure")

    def get_ref(self, m):
        """Get the reference frame of the measure.

        :param m: a measure (dictionary)
        :rtype: string
        """

        if is_measure(m):
            return m["refer"]
        else:
            raise TypeError("Argument is not a measure")

    def get_offset(self, m):
        """Get the offset measure.

        :param m: a measure (dictionary)
        :rtype: a measure
        """

        if is_measure(m):
            return m.get("offset", None)
        else:
            raise TypeError("Argument is not a measure")

    def doframe(self, v):
        """This method will set the measure specified as part of a frame. 

        If conversion from one type to another is necessary (with the measure
        function), the following frames should be set if one of the reference
        types involved in the conversion is as in the following lists:

        **Epoch**

         * UTC		
         * TAI
         * LAST	- position
         * LMST - position
         * GMST1 
         * GAST 
         * UT1 
         * UT2 
         * TDT 
         * TCG 
         * TDB 
         * TCD

        **Direction**

         * J2000
         * JMEAN - epoch 
         * JTRUE - epoch
         * APP - epoch
         * B1950 
         * BMEAN - epoch
         * BTRUE - epoch
         * GALACTIC 	
         * HADEC - epoch, position
         * AZEL	- epoch, position
         * SUPERGALACTIC
         * ECLIPTIC
         * MECLIPTIC - epoch
         * TECLIPTIC - epoch
         * PLANET - epoch, [position]

        **Position**

         * WGS84
         * ITRF

        **Radial Velocity**

         * LSRK - direction
         * LSRD - direction
         * BARY - direction
         * GEO - direction, epoch
         * TOPO - direction, epoch, position
         * GALACTO - direction
         * 

        **Doppler**

         * RADIO 
         * OPTICAL 
         * Z 
         * RATIO 
         * RELATIVISTIC 
         * BETA 
         * GAMMA
         * 

        **Frequency**

         * REST - direction, radialvelocity
         * LSRK - direction
         * LSRD - direction
         * BARY - direction
         * GEO - direction, epoch
         * TOPO	- direction, epoch, position
         * GALACTO

        """
        if not is_measure(v):
            raise TypeError('Argument is not a measure')
        if (v["type"] == "frequency" and v["refer"].lower() == "rest") \
               or _measures.doframe(self, v):
            self._framestack[v["type"]] = v
            return True
        return False
    do_frame = doframe
    
    def _fillnow(self):
        if not "epoch" in self._framestack \
               or not is_measure(self._framestack["epoch"]):
            self.frame_now()
            
    def _getwhere(self):
        if not self._framestack.has_key("position") \
               or not is_measure(self._framestack["position"]):
            raise RuntimeError("Can't find position frame")
        return self._framestack["position"]
    
    def framenow(self):
        """Set the time (epoch) frame to the current time and day."""
        self.do_frame(self.epoch("UTC", "today"))
    frame_now = framenow
    
    def rise(self, crd, ev='5deg'):
        """This method will give the rise/set hour-angles of a source. It 
        needs the position in the frame, and a time. If the latter is not 
        set, the current time will be used. 

        :param crd: a direction measure
        :param ev: the elevation limit as a quantity or string
        :returns: `dict` with rise and set sidereal time quantities or a 2
                   strings "below" or "above" 
        """
        if not is_measure(crd):
            raise TypeError('No rise/set coordinates specified')
        ps = self._getwhere()
        self._fillnow()
        hd = self.measure(crd, "hadec")
        c = self.measure(crd, "app")
        evq = dq.quantity(ev)
        hdm1 = dq.quantity(hd["m1"])
        psm1 = dq.quantity(ps["m1"])
        ct = (dq.sin(dq.quantity(ev)) - (dq.sin(hdm1) * dq.sin(psm1)))\
              / (dq.cos(hdm1) * dq.cos(psm1))

        if ct.get_value() >= 1:
            return {'rise': 'below', 'set': 'below'}
        if ct.get_value() <= -1:
            return {'rise': 'above', 'set': 'above'}
        a = dq.acos(ct)
        return dict(rise=dq.quantity(c["m0"]).norm(0) - a,
                    set=dq.quantity(c["m0"]).norm(0) + a)
    
    def riseset(self, crd, ev="5deg"):
        """This will give the rise/set times of a source. It needs the 
        position in the frame, and a time. If the latter is not set, the 
        current time will be used. 
        
        :param crd: a direction measure
        :param ev: the elevation limit as a quantity or string
        :returns: The returned value is a `dict` with a 

        'solved' key, which is `False` if the source is always below or above 
        the horizon. In that case the rise and set fields will all have a 
        string value. The `dict` also returns a rise and set `dict`, with 
        'last'  and 'utc' keys showing the rise and set times as epochs.
        """

        a = self.rise(crd, ev)
        if isinstance(a['rise'], str):
            return { "rise": { "last": a[0], "utc": a[0] },
                     "set" : { "last": a[1], "utc": a[1] },
                     "solved": False }
        ofe = self.measure(self._framestack["epoch"], "utc")
        if not is_measure(ofe):
            ofe = self.epoch('utc', 'today')
        x = a.copy()
        for k in x:
            x[k] = self.measure(
                      self.epoch("last", 
                                 a[k].totime(),
                                 off=self.epoch("r_utc",
                                                (dq.quantity(ofe["m0"]) 
                                                 + dq.quantity("0.5d")
                                                 ))
                                 ),
                      "utc")
        return { "rise": { "last": self.epoch("last",
                                              a["rise"].totime()),
                           "utc": x["rise"] },
                 
                 "set": { "last": self.epoch("last",
                                             a["set"].totime()),
                           "utc": x["set"] },
                 "solved" : True
                 }

    def observatory(self, name):
        """Get a (position) measure for the given obervatory
        
        :param name: the name of the observatory
        :returns: a position measure
        """
        return _measures.observatory(self, name.upper())

    def get_observatories(self):
        """Return a list of known observatory names, whci can be used as input
        for :meth:`~pyrap.measures.measures.observatory`
    
        :rtype: list of strings
        """
        return self.obslist()

    #alias
    def list_codes(self, m):
        """Get the known reference codes for a specified measure type. It 
        will return a `dict` with two keys. The first is a string list 
        of all normal codes; the second a string list (maybe empty) with all 
        extra codes (like planets).
        
        :param m: the measures with the type to get codes for
        """
        return _measures.alltyp(self, m)

    
    def posangle(self, m0, m1):
        """
        This method will give the position angle from a direction to another
        i.e. the angle in a direction between the direction to the North
        pole and the other direction.

        :param m0: a measure 
        :param m1: another measure

        Example::

            >>> a = dm.direction('j2000','0deg','70deg')
            >>> b = dm.direction('j2000','0deg','80deg') 
            >>> print dm.posangle(a,b)
            -0.0 deg 
        """
        return _measures.posangle(self, m0, m1)

    def separation(self, m0, m1):
        """
        This method will give the separation of a direction from another as 
        an angle. 
 
        :param m0: a measure 
        :param m1: another measure

        Example::

            >>> a = dm.direction('j2000','0deg','70deg')
            >>> b = dm.direction('j2000','0deg','80deg') 
            >>> print dm.separation(a,b)
            10.0 deg
       """
        return _measures.separation(self, m0, m1)


##     def show(v, refcode=True):
##         z = ""
##         if is_measure(v):
##             x = dm.gettype(v)
##             y = dm.getvalue(v)
##             if x.startswith("epo"):
##                 z = dq.form.dtime(y[0])
##             else:
##                 return ""
##             if refcode:
##                 return [z, dm.getref(v)]
##         return z

    
