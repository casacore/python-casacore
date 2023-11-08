# __init__.py: Top level .py file for python measures interface
# Copyright (C) 2006
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
# $Id: __init__.py,v 1.2 2006/12/04 04:01:03 mmarquar Exp $
__all__ = ['is_measure', 'measures']

from ._measures import measures as _measures

import casacore.quanta as dq
import os

if 'MEASURESDATA' in os.environ.keys():
    if 'AIPSPATH' not in os.environ.keys():
        os.environ['AIPSPATH'] = '%s dummy dummy' % os.environ['MEASURESDATA']


def is_measure(v):
    """
    Return if this is a true measures dictionary

    :param v: The object to check
    """
    if isinstance(v, dict) and "type" in v and "m0" in v:
        return True
    return False


def _check_valid_offset(self, mtype):
    if not off['type'] == mtype:
        raise TypeError('Illegal offset type specified.')


class measures(_measures):
    """The measures server object. This should be used to set frame
    information and create the various measures and do conversion on them.

    The measures types are:

    * :meth:`direction`

    * :meth:`position`

    * :meth:`epoch`

    * :meth:`frequency`

    * :meth:`doppler`

    * :meth:`baseline`

    * :meth:`radialvelocity`

    * :meth:`uvw`

    * :meth:`earthmagnetic`

    Typical usage::

        from casacore.measures import measures
        dm = measures() # create measures server instance
        dirmeas = dm.direction()

    """

    def __init__(self):
        _measures.__init__(self)
        self._framestack = {}

    def set_data_path(self, pth):
        """Set the location of the measures data directory.

        :param pth: The absolute path to the measures data directory.
        """
        if os.path.exists(pth):
            if not os.path.exists(os.path.join(pth, 'data', 'geodetic')):
                raise IOError("The given path doesn't contain a 'data' "
                              "subdirectory")
            os.environ["AIPSPATH"] = "%s dummy dummy" % pth

    def measure(self, v, rf, off=None):
        """Create/convert a measure using the frame state set on the measures
        server instance (via :meth:`do_frame`)

        :param v: The measure to convert

        :param rf: The frame reference to convert to

        :param off: The optional offset for the measure

        """
        if off is None:
            off = {}
        keys = ["m0", "m1", "m2"]
        for key in keys:
            if key in v:
                if dq.is_quantity(v[key]):
                    v[key] = v[key].to_dict()
        return _measures.measure(self, v, rf, off)

    def direction(self, rf='', v0='0..', v1='90..', off=None):
        """Defines a direction measure. It has to specify a reference code,
        direction quantity values (see introduction for the action on a
        scalar quantity with either a vector or scalar value, and when a
        vector of quantities is given), and optionally it can specify an
        offset, which in itself has to be a direction.

        :param rf: reference code string; allowable reference codes are:
                   J2000 JMEAN  JTRUE APP B1950 BMEAN BTRUE GALACTIC HADEC
                   AZEL SUPERGAL ECLIPTIC MECLIPTIC TECLIPTIC MERCURY VENUS
                   MARS JUPITER SATURN URANUS NEPTUNE PLUTO MOON SUN COMET.
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.direction())

        :param v0, v1: Direction quantity values should be
                       longitude (angle) and latitude (angle) or strings
                       parsable by :func:`~casacore.quanta.quantity`.
                       None are needed for planets: the frame epoch defines
                       coordinates. See :func:`~casacore.quanta.quantity` for
                       possible angle formats.
        :param off: an optional offset measure of same type

        Example::

            >>> dm.direction('j2000','30deg','40deg')
            >>> dm.direction('mars')

        """
        loc = {'type': 'direction', 'refer': rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        if is_measure(off):
            if not off['type'] == "direction":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def position(self, rf='', v0='0..', v1='90..', v2='0m', off=None):
        """Defines a position measure. It has to specify a reference code,
        position quantity values (see introduction for the action on a
        scalar quantity with either a vector or scalar value, and when a
        vector of quantities is given), and optionally it can specify an
        offset, which in itself has to be a position.
        Note that additional ones may become available. Check with::

            dm.list_codes(dm.position())

        The position quantity values should be either longitude (angle),
        latitude(angle) and height(length); or x,y,z (length). See
        :func:`~casacore.quanta.quantity` for possible angle formats.

        :param rf: reference code string; Allowable reference
                   codes are: *WGS84* *ITRF* (World Geodetic System and
                   International Terrestrial Reference Frame)
        :param v0: longitude or x as quantity or string
        :param v1: latitude or y as quantity or string
        :param v2: height or z as quantity or string
        :param off: an optional offset measure of same type

        Example::

            dm.position('wgs84','30deg','40deg','10m')
            dm.observatory('ATCA')

        """
        loc = {'type': 'position', 'refer': rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "position":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def epoch(self, rf='', v0='0.0d', off=None):
        """
        Defines an epoch measure. It has to specify a reference code, an epoch
        quantity value (see introduction for the action on a scalar quantity
        with either a vector or scalar value, and when a vector of quantities
        is given), and optionally it can specify an offset, which in itself
        has to be an epoch.

        :param rf: reference code string; Allowable reference
                   codes are: *UTC TAI LAST LMST GMST1 GAST UT1 UT2 TDT TCG
                   TDB TCB*
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.position())

        :param v0: time as quantity or string
        :param off: an optional offset measure of same type

        """
        loc = {'type': 'epoch', 'refer': rf}
        loc['m0'] = dq.quantity(v0)
        if is_measure(off):
            if not off['type'] == "epoch":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def frequency(self, rf='', v0='0Hz', off=None):
        """Defines a frequency measure. It has to specify a reference code,
        frequency quantity value (see introduction for the action on a scalar
        quantity with either a vector or scalar value, and when a vector of
        quantities is given), and optionally it can specify an offset, which
        in itself has to be a frequency.

        :param rf: reference code string; Allowable reference
                   codes are: *REST LSRK LSRD BARY GEO TOPO GALACTO*
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.frequency())

        :param v0: frequency value as quantity or string. The frequency
                   quantity values should be in one of the recognised units
                   (examples all give same frequency):

                   * value with time units: a period (0.5s)
                   * value as frequency: 2Hz
                   * value in angular frequency: 720deg/s
                   * value as length: 149896km
                   * value as wave number: 4.19169e-8m-1
                   * value as enery (h.nu): 8.27134e-9ueV
                   * value as momentum: 4.42044e-42kg.m

        :param off: an optional offset measure of same type

        """
        loc = {'type': "frequency",
               'refer': rf,
               'm0': dq.quantity(v0)}
        if is_measure(off):
            if not off['type'] == "frequency":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def doppler(self, rf='', v0=0.0, off=None):
        """Defines a doppler measure. It has to specify a reference code,
        doppler quantity value (see introduction for the action on a scalar
        quantity with either a vector or scalar value, and when a vector of
        quantities is given), and optionally it can specify an offset, which
        in itself has to be a doppler.

        :param rf: reference code string; Allowable reference
                   codes are: *RADIO OPTICAL Z RATIO RELATIVISTIC BETA GAMMA*.
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.doppler())

        :param v0: doppler ratio as quantity, string or float value. It
                   should be either non-dimensioned to specify a ratio of
                   the light velocity, or in velocity. (examples all give
                   same doppler):
        :param off: an optional offset measure of same type

        Example::

            >>> from casacore import quanta
            >>> dm.doppler('radio', 0.4)
            >>> dm.doppler('radio', '0.4')
            >>> dm.doppler('RADIO', quanta.constants['c']*0.4))

        """
        if isinstance(v0, float):
            v0 = str(v0)
        loc = {'type': "doppler",
               'refer': rf,
               'm0': dq.quantity(v0)}
        if is_measure(off):
            if not off['type'] == "doppler":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def radialvelocity(self, rf='', v0='0m/s', off=None):
        """Defines a radialvelocity measure. It has to specify a reference
        code, radialvelocity quantity value (see introduction for the action
        on a scalar quantity with either a vector or scalar value, and when
        a vector of quantities is given), and optionally it can specify an
        offset, which in itself has to be a radialvelocity.


        :param rf: reference code string; Allowable reference
                   codes are: *LSRK LSRD BARY GEO TOPO GALACTO*
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.radialvelocity())

        :param v0: longitude or x as quantity or string
        :param off: an optional offset measure of same type

        """
        loc = {'type': "radialvelocity",
               'refer': rf,
               'm0': dq.quantity(v0)}
        if is_measure(off):
            if not off['type'] == "radialvelocity":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def baseline(self, rf='', v0='0..', v1='', v2='', off=None):
        """Defines a baselin measure. It has to specify a reference code, uvw
        quantity values (see introduction for the action on a scalar quantity
        with either a vector or scalar value, and when a vector of quantities
        is given), and optionally it can specify an offset, which in itself
        has to be a baseline.

        :param rf: reference code string; Allowable reference
                   codes are: *ITRF* and :meth:`direction` codes
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.baseline())


        :param v0: longitude or x as quantity or string
        :param v1: latitude or y as quantity or string
        :param v2: height or z as quantity or string
        :param off: an optional offset measure of same type
        """
        loc = {'type': "baseline", 'refer': rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "doppler":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def uvw(self, rf='', v0='0..', v1='', v2='', off=None):
        """Defines a uvw measure. It has to specify a reference code, uvw
        quantity values (see introduction for the action on a scalar quantity
        with either a vector or scalar value, and when a vector of quantities
        is given), and optionally it can specify an offset, which in itself
        has to be a uvw.

        :param rf: reference code string; Allowable reference
                   codes are: *ITRF* and :meth:`direction` codes
                   Note that additional ones may become available. Check with::

                       dm.list_codes(dm.uvw())


        :param v0: longitude or x as quantity or string
        :param v1: latitude or y as quantity or string
        :param v2: height or z as quantity or string
        :param off: an optional offset measure of same type

        """
        loc = {'type': "uvw", 'refer': rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "uvw":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def earthmagnetic(self, rf='', v0='0G', v1='0..', v2='90..', off=None):
        """Defines an earthmagnetic measure. It needs a reference code,
        earthmagnetic quantity values (see introduction for the action on a
        scalar quantity with either a vector or scalar value, and when a
        vector of quantities is given) if the reference code is not for a
        model, and optionally it can specify an offset, which in itself has
        to be a earthmagnetic. In general you specify a model (*IGRF* is the
        default and the only one known) and convert it to an explicit field.
        (See http://fdd.gsfc.nasa.gov/IGRF.html for information on the
        International Geomagnetic Reference Field). The earthmagnetic quantity
        values should be either longitude (angle), latitude(angle) and
        length(field strength); or x,y,z (field).
        See :func:`~casacore.quanta.quantity` for possible angle formats.

        :param rf: reference code string; Allowable reference
                   codes are: *IGRF*
        :param v0: longitude or x as quantity or string
        :param v1: latitude or y as quantity or string
        :param v2: height or z as quantity or string
        :param off: an optional offset measure of same type

        """
        loc = {'type': "earthmagnetic", 'refer': rf}
        loc['m0'] = dq.quantity(v0)
        loc['m1'] = dq.quantity(v1)
        loc['m2'] = dq.quantity(v2)
        if is_measure(off):
            if not off['type'] == "earthmagnetic":
                raise TypeError('Illegal offset type specified.')
            loc["offset"] = off
        return self.measure(loc, rf)

    def tofrequency(self, rf, v0, rfq):
        """Convert a Doppler type value (e.g. in radio mode) to a
        frequency. The type of frequency (e.g. LSRK) and a rest frequency
        (either as a frequency quantity (e.g. ``dm.constants('HI'))`` or
        a frequency measure (e.g. ``dm.frequency('rest','5100MHz'))`` should
        be specified.

        :param rf: frequency reference code (see :meth:`frequency`)
        :param v0: a doppler measure
        :param rfq: frequency measure or quantity

        Example::

            dop = dm.doppler('radio',0.4)
            freq = dm.tofrequency('lsrk', dop, dm.constants('HI'))

        """
        if is_measure(rfq) and rfq['type'] == 'frequency':
            rfq = dq.quantity(rfq['m0'])
        elif isinstance(rfq, string_types):
            rfq = dq.quantity(rfq)
        if is_measure(v0) and v0['type'] == 'doppler' \
                and dq.is_quantity(rfq) \
                and rfq.conforms(dq.quantity('Hz')):
            return self.doptofreq(v0, rf, rfq)
        else:
            raise TypeError('Illegal Doppler or rest frequency specified')

    to_frequency = tofrequency

    def torestfrequency(self, f0, d0):
        """Convert a frequency measure and a doppler measure (e.g.
        obtained from another spectral line with a known rest frequency) to
        a rest frequency.

        :param f0: frequency reference code (see :meth:`frequency`)
        :param v0: a doppler measure

        Example::

            dp = dm.doppler('radio', '2196.24984km/s')  # a measured doppler speed
            f = dm.frequency('lsrk','1410MHz')    # a measured frequency
            dm.torestfrequency(f, dp)        # the corresponding rest frequency

        """
        if is_measure(f0) and f0['type'] == 'frequency' \
                and is_measure(d0) and d0['type'] == 'doppler':
            return self.torest(f0, d0)
        else:
            raise TypeError('Illegal Doppler or rest frequency specified')

    to_restfrequency = torestfrequency

    def todoppler(self, rf, v0, rfq):
        """Convert a radialvelocity measure or a frequency measure to a
        doppler measure. In the case of a frequency, a rest frequency has
        to be specified. The type of doppler wanted (e.g. *RADIO*) has to be
        specified.

        :param rf: doppler reference code (see :meth:`doppler`)
        :param v0: a radialvelocity or frequency measure
        :param rfq: frequency measure or quantity

        Example::

            f = dm.frequency('lsrk','1410MHz')     # specify a frequency
            dm.todoppler('radio', f, dm.constants('HI')) # give doppler, using HI rest

        """
        if is_measure(rfq) and rfq['type'] == 'frequency':
            rfq = dq.quantity(rfq['m0'])
        elif isinstance(rfq, string_types):
            rfq = dq.quantity(rfq)
        if is_measure(v0):
            if v0['type'] == 'radialvelocity':
                return self.todop(v0, dq.quantity(1., 'Hz'))
            elif v0['type'] == 'frequency' and dq.is_quantity(rfq) \
                    and rfq.conforms(dq.quantity('Hz')):
                return self.todop(v0, rfq)
            else:
                raise TypeError('Illegal Doppler or rest frequency specified')
        else:
            raise TypeError('Illegal Frequency specified')

    to_doppler = todoppler

    def toradialvelocity(self, rf, v0):
        """Convert a Doppler type value (e.g. in radio mode) to a real
        radialvelocity. The type of velocity (e.g. *LSRK*) should be specified

        :param rf: radialvelocity reference code (see :meth:`radialvelocity`)
        :param v0: a doppler measure

        Example::

            a = dm.doppler('radio',0.4)
            dm.toradialvelocity('topo',a)

        """
        if is_measure(v0) and v0['type'] == 'doppler':
            return self.doptorv(rf, v0)
        else:
            raise TypeError('Illegal Doppler specified')

    to_radialvelocity = toradialvelocity

    def touvw(self, v):
        """Calculates a uvw measure from a baseline. The baseline can consist
        of a vector of actual baseline positions. Note that the baseline does
        not have to be a proper baseline, but can be a series of positions
        (to  call positions baselines see :meth:`asbaseline` ) for speed
        reasons: operations are linear and can be done on positions, which
        are converted to baseline values at the end (with :meth:`expand` ).

        Whatever the reference code of the baseline, the returned uvw will be
        given in J2000. If the dot argument is given, that variable will be
        filled with a quantity array consisting of the time derivative of the
        uvw (note that only the sidereal rate is taken into account; not
        precession, earth tides and similar variations, which are much
        smaller). If the xyz variable is given, it will be filled with the
        quantity values of the uvw measure.

        The values of the input baselines can be given as a quantity
        vector per x, y or z value.

        uvw coordinates are calculated for a certain direction in the sky
        hence the frame has to contain the direction for the calculation to
        work. Since the baseline and the sky rotate with respect of each
        other, the time should be specified as well.

        Example::

            >>> dm.do_frame(dm.observatory('atca'))
            >>> dm.do_frame(dm.source('1934-638'))
            >>> dm.do_frame(dm.epoch('utc', 'today'))
            >>> b = dm.baseline('itrf', '10m', '20m', '30m')

        """
        if is_measure(v) and v['type'] == 'baseline':
            m = _measures.uvw(self, v)
            m['xyz'] = dq.quantity(m['xyz'])
            m['dot'] = dq.quantity(m['dot'])
            return m
        else:
            raise TypeError('Illegal Baseline specified')

    to_uvw = touvw

    def expand(self, v):
        """Calculates the differences between a series of given measure values:
        it calculates baseline values from position values.

        :params v: a measure (of type 'baseline', 'position' or 'uvw')
        :returns: a `dict` with the value for key `measures` being a measure
                  and the value for key `xyz` a quantity containing the
                  differences.

        Example::

            >>> from casacore.quanta import quantity
            >>> x = quantity([10,50],'m')
            >>> y = quantity([20,100],'m')
            >>> z = quantity([30,150],'m')
            >>> sb = dm.baseline('itrf', x, y, z)
            >>> out = dm.expand(sb)
            >>> print out['xyz']
            [40.000000000000014, 80.0, 120.0] m

        """
        if not is_measure(v) or v['type'] not in ['baseline',
                                                  'position', 'uvw']:
            raise TypeError("Can only expand baselines, positions, or uvw")
        vw = v.copy()
        vw['type'] = "uvw"
        vw['refer'] = "J2000"
        outm = _measures.expand(self, vw)
        outm['xyz'] = dq.quantity(outm['xyz'])
        outm['measure']['type'] = v['type']
        outm['measure']['refer'] = v['refer']
        return outm

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
        if not is_measure(v):
            raise TypeError('Incorrect input type for getvalue()')
        import re
        rx = re.compile(r"m\d+")
        out = []
        keys = list(v.keys())
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
        if "epoch" not in self._framestack \
                or not is_measure(self._framestack["epoch"]):
            self.frame_now()

    def _getwhere(self):
        if "position" not in self._framestack \
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
        ct = (dq.sin(dq.quantity(ev)) - (dq.sin(hdm1) * dq.sin(psm1))) \
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
                  'solved' key, which is `False` if the source is always
                  below or above the horizon. In that case the rise and set
                  fields will all have a string value. The `dict` also returns
                  a rise and set `dict`, with  'last'  and 'utc' keys showing
                  the rise and set times as epochs.

        """

        a = self.rise(crd, ev)
        if isinstance(a['rise'], string_types):
            return {"rise": {"last": a[0], "utc": a[0]},
                    "set": {"last": a[1], "utc": a[1]},
                    "solved": False}
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
        return {"rise": {"last": self.epoch("last",
                                            a["rise"].totime()),
                         "utc": x["rise"]},

                "set": {"last": self.epoch("last",
                                           a["set"].totime()),
                        "utc": x["set"]},
                "solved": True
                }

    def observatory(self, name):
        """Get a (position) measure for the given obervatory.

        :param name: the name of the observatory. At the time of
                     writing the following observatories are recognised (but
                     check :meth:`get_observatories`): *ALMA ATCA BIMA CLRO
                     DRAO DWL GB JCMT MOPRA NRAO12M PKS VLA WSRT*
        :returns: a position measure
        """
        return _measures.observatory(self, name.upper())

    def get_observatories(self):
        """Return a list of known observatory names, which can be used as input
        to :meth:`observatory`.

        :rtype: list of strings
        """
        return self.obslist()

    def line(self, name):
        """Get a (frequency) measure for the given spectral line name.

        :param name: the name of the spectral line. Minimum match applies.
                     At the time of writing the following are recognised (but
                     check :meth:`get_lines`): *C109A CI CII166A DI H107A
                     H110A H138B H166A H240A H272A H2CO HE110A HE138B HI
                     OH1612 OH1665 OH1667 OH1720 CO115271 H2O22235 SiO86847
                     CO230538*
        :returns: a frequency measure
        """
        return _measures.line(self, name)

    def get_lines(self):
        """Return a list of known spectral line names, which can be used as
        input to :meth:`line`.

        :rtype: list of strings
        """
        return self.linelist()

    def source(self, name):
        """Get a (direction) measure for the given atsronomical source.

        :param name: the name of the source. Minimum match applies.
                     Check :meth:`get_sources` for the list of known sources
        :returns: a frequency measure

        Example::

            >>> print dm.source('1936-6')
            {'m0': {'unit': 'rad', 'value': -1.1285176426372401},
             'm1': {'unit': 'rad', 'value': -1.0854059868642842},
             'refer': 'ICRS',
             'type': 'direction'}

        """
        return _measures.source(self, name)

    def get_sources(self):
        """Return a list of known sources names, which can be used as
        input to :meth:`source`.

        :rtype: list of strings
        """
        return self.srclist()

    # alias
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

#     def show(v, refcode=True):
#         z = ""
#         if is_measure(v):
#             x = dm.gettype(v)
#             y = dm.getvalue(v)
#             if x.startswith("epo"):
#                 z = dq.form.dtime(y[0])
#             else:
#                 return ""
#             if refcode:
#                 return [z, dm.getref(v)]
#         return z
