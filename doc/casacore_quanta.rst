=============================
Module :mod:`casacore.quanta`
=============================

.. module:: casacore.quanta

Python bindings for
`casacore Quantum objects <../../casacore/doc/html/classcasa_1_1Quantum.html>`_
It transparently handles Quantity and Quantum<Vector<Double> >.

Introduction
============

A quantity is a value with a unit. For example, '5km/s', or '20Jy/pc2'. This
module enables you to create and manipulate such quantities. The types of
functionality provided are:

    * Conversion of quantities to different units
    * Calculations with quantities

Constants, time and angle formatting
------------------------------------

If you would like to see all the possible constants known to quanta you can
execute the function :func:`casacore.quanta.constants.keys()`. You can get the
value of any constant in that dictionary with a command such as::

    >>> from casacore import quanta
    >>> boltzmann = quanta.constants['k']
    >>> print 'Boltzmann constant is ', boltzmann
    Boltzmann constant is 1.3806578e-23 J/K

There are some extra handy ways you can manipulate strings when you are
dealing with times or angles. The following list shows special strings and
string formats which you can input to the quantity function. Something in
square brackets is optional. There are examples after the list.

    * time: [+-]hh:mm:ss.t... - This is the preferred time format (trailing
                                fields can be omitted)
    * time: [+-]hhHmmMss.t..[S] - This is an alternative time format (HMS case
                                  insensitive, trailing second fields can be
                                  omitted)
    * angle: [+-]dd.mm.ss.t.. - This is the preferred angle format (trailing
                                fields after second priod can be omitted; dd..
                                is valid)
    * angle: [+-]ddDmmMss.t...[S] - This is an alternative angle format (DMS
                                    case insensitive, trailing fields can be
                                    omitted after M)
    * today - The special string "today" gives the UTC time at the instant
              the command was issued.
    * today/time - The special string "today" plus the specified time
                   string gives the UTC time at the specified instant
    * yyyy/mm/dd[/time] - gives the UTC time at the specified instant
    * yyyy-mm-dd[Ttime[+-hh[:mm]]] - gives the UTC time from ISO 8601 format
                                     with timezone offset
    * dd[-]mmm[-][cc]yy[/time] - gives the UTC time at the specified instant
                                 in calendar style notation (23-jun-1999)

All possible units are visible in the dict `casacore.quanta.constants.units`,
and all possible prefixes (all SI prefixes) are in the dict 
`casacore.quanta.constants.prefixes`.

Note that the standard unit for degrees is 'deg', and for days 'd'. Formatting
is done in such a way that it interprets a 'd' as degrees if preceded by a
value without a period and if any value following it is terminated with an 'm'.
In other cases 'days' are assumed. Here are some examples::

    >>> from casacore.quanta import quantity
    >>> print quantity('today')
    50611.2108 d
    >>> print quantity('5jul1998')
    50999 unit=d
    print quantity('5jul1998/12:')
    50999.5 d
    >>> print quantity('-30.12.2')
    30.2005556 deg
    >>> print quantity('2:2:10')
    30.5416667 deg
    >>> print quantity('23h3m2.2s')
    345.759167 deg

Python :mod:`datetime` to quantity::

    >>> import datetime
    >>> utcnow = datetime.datetime.utcnow()
    >>> q = quantity(utcnow.isoformat())

The (string) output of quantities can be controlled in different ways:

Standard output:

    >>> q = quantity('23h3m2.2s')
    >>> print q
    345.75917 deg

Angle/time quantity formatting:

    >>> print q.formatted("ANGLE")
    +345.45.33

Precision formatting:

    >>> print q.to_string("%0.2f")
    345.76 deg

API
===

.. function:: is_quantity(q)

    :param q: the object to check.

.. function:: quantity(*args)

   A Factory function to create a :class:`casacore.quanta.Quantity` instance.
   This can be from a scalar or vector and a unit.

   :param args:
   	  * A string will be parsed into a :class:`casacore.quanta.Quantity`
	  * A `dict` with the keys `value` and `unit`
	  * two arguments representing `value` and `unit`

    Examples::

      q1 = quantity(1.0, "km/s")
      q2 = quantity("1km/s")
      q3 = quantity([1.0,2.0], "km/s")


.. class:: Quantity

    A unit-value based physical quantity.

    .. method:: set_value(val)

        Set the value of the quantity

        :param val: The new value to change to (in current units)

    .. method:: get(unit=None)

        Return the quantity as another (conformant) one.

        :param unit: an optional conformant unit to convert the quantity to.
                     If the unit isn't specified the canonical unit is used.
	:rtype: :class:`casacore.quanta.Quantity`

        Example::

            >>> q = quantity('1km/s')
	    >>> print q.get('m/s')
	    1000.0 m/s

    .. method:: get_value(unit)

        Get the value of the quantity suing the optiona unit

        :param unit: a conformant unit to convert the quantity to.
	:rtype: `float` ot `list` of `float`

        Example::

            >>> q = quantity('1km/s')
	    >>> print q.get_value()
	    1.0

    .. method:: get_unit()

        Retrieve the unit

	:rtype: string

    .. method:: conforms(other)

	Check if another :class:`casacore.quanta.Quantity` conforms to self.

        :param other: an :class:`casacore.quanta.Quantity` object to compare to

    .. method:: convert(other=None)

        Convert the quantity using the given :class:`Quantity` or unit string.

        :param other: an optional conformant :class:`Quantity` to convert to.
                      If other isn't specified the canonical unit is used.

        Example::

            >>> q = quantity('1km/s')
	    >>> q.convert()
	    >>> print q
	    1000.0 m/s

    .. method:: to_dict()

        Return self as a python :class:`dict` with `value` and `unit` keys.

	:rtype: :class:`dict`

    .. method:: to_angle()

        Convert to an angle Quantity.
	This will only work if it conforms to angle

	:rtype: :class:`casacore.quanta.Quantity`

    .. method:: to_time()

        Convert to a time Quantity (e.g. hour angle).
	This will only work if it conforms to time

	:rtype: :class:`casacore.quanta.Quantity`

    .. method:: to_unix_time()

        Convert to a unix time value (in seconds).
	This can be used to create python :class:`datetime.datetime` objects

	:rtype: float

    .. method:: to_string(fmt="%0.5f")
       
       Return a string with the Quantity values' precision formatted with `fmt`.

       :param fmt: the printf type formatting string.
       :rtype: string

    .. method:: formatted(fmt)

       Return a formatted string representation of the Quantity.
       
       :param fmt: the format code for angle or time formatting as per
       	      	   `casacore angle format <../../casacore/doc/html/classcasa_1_1MVAngle.html#ef9ddd9c3fe111aef61b066b2745ced4>`_ and `casacore time format <../../casacore/doc/html/classcasa_1_1MVTime.html#906c0740cdae7a50ef933d6c3e2ac5ab>`_
       :rtype: string

On top of the listed method, it also supports all mathematical operators and
functions like:

    * \*, \*=, +, +=, -, -=, /, /=
    * <, <=, >, >=, ==, !=
    * abs, pow, root, srqt, cels, floor, sin, cos, asin, acos, atan, atan2
      log, log10, exp
    * near and nearabs

Examples::

    >>> q = quantity("1km/s")
    >>> print q*2
    2.0 km/s
    >>> print 2*q
    2.0 km/s
    >>> q /= 2
    >>> print q
    0.5 km/s
    >>> q2 = quantity("0rad")
    >>> print dq.cos(q)
    1.0
