==========================
Module :mod:`pyrap.quanta`
==========================

.. module:: pyrap.quanta
   
Python bindings for casacore's casa::Quantum value-unit objects.
It transparently handles Quantity and Quantum<Vector<Double> >.

On top of the listed method, it also supports all mathematical operators like:

    * \*, \*=, +, +=, -, -=, /, /=
    * abs, pow, root, srqt, cels, floor, sin, cos, asin, acos, atan, atan2
      log, log10, exp
    * near and nearabs

Examples::

    q = quantity('1km/s')	
    print q*2
    >>> 2.0 km/s
    print 2*q
    >>> 2.0 km/s
    q /= 2
    print q
    >>> 0.5 km/s
    q2 = quantity('0rad') 
    print dq.cos(q)
    >>> 1.0

.. function:: pyrap.quanta.is_quantity(q)

    :param q: the object to check.

.. function:: pyrap.quanta.quantity(*args)

   A Factory function to create a :class:`pyrap.quanta.Quantity` instance.
   This can be from a scalar or vector and a unit.

   :param args: 
   	  * A string will be parsed into a :class:`pyrap.quanta.Quantity`
	  * A `dict` with the keys `value` and `unit`
	  * two arguments representing `value` and `unit`
	  
    Examples::
      
      q1 = quantity(1.0, "km/s")
      q2 = quantity("1km/s")
      q3 = quantity([1.0,2.0], "km/s")
	  

.. class:: pyrap.quanta.Quantity

    A unit-value based physical quantity.

    .. method:: get(unit=None)

        Return the quantity as another (conformant) one.

        :param unit: an optional conformant unit to convert the quantity to.
                     If the unit isn't specified the canonical unit is used.

        Example::

            q = quantity('1km/s')
	    print q.get('m/s')
	    >>> 1000.0 m/s

    .. method:: get_value(unit)

        Get the value of the quantity suing the optiona unit

        :param unit: a conformant unit to convert the quantity to.

        Example::

            q = quantity('1km/s')
	    print q.get_value()
	    >>> 1.0

    .. method:: get_unit()

        Retrieve the unit
	
	:rtype: string

    .. method:: conforms(other)
        
	Check if another :class:`pyrap.quanta.Quantity` conforms to self.

        :param other: an :class:`pyrap.quanta.Quantity` object to compare to

   .. method:: convert(other=None)

        Convert the quantity using the given `Quantity` or unit string.

        :param other: an optional conformant `Quantity` to convert to.
                      If other isn't specified the canonical unit is used.

        Example::

            q = quantity('1km/s')
	    q.convert()
	    print q
	    >>> 1000.0 m/s
