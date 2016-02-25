===============================
Module :mod:`casacore.measures`
===============================

.. module:: casacore.measures

Introduction
============

This is a python binding to
`casacore measures <../../casacore/doc/html/group__Measures__module.html>`_

A measure is a quantity with a specified reference frame (e.g. *UTC*, *J2000*,
*mars*). The measures module provides an interface to the handling of
measures. The basic functionality provided is:

    * Conversion of measures, especially between different frames
      (e.g. *UTC* to *LAST*)
    * Calculation of e.g. a rest frequency from a velocity and a
      frequency.

To access the measures do the following. We will use `dm` as the measures
instance through all examples::

   >>> from casacore.measures import measures
   >>> dm = measures()

Measures
--------

Measures are e.g. an epoch or coordinates which have in addition to values -
:class:`casacore.quanta.Quantity` - also a reference specification and possibly
an offset. They are represented as records with fields describing the various
entities embodied in the measure. These entities can be obtained by the access
methods:

* :meth:`~casacore.measures.measures.get_type`
* :meth:`~casacore.measures.measures.get_ref`
* :meth:`~casacore.measures.measures.get_offset`
* :meth:`~casacore.measures.measures.get_value`.

Each measure has its own list of reference codes (see the individual methods
for creating them, like :meth:`~casacore.measures.measures.direction`). If an
empty or no code reference code is  given, the default code for that type of
measure will be used (e.g. it is *J2000* for a
:meth:`~casacore.measures.measures.direction`). If an unknown code is given,
this default is also returned, but with a warning message.

The values of a measure (like the right-ascension for a
:meth:`~casacore.measures.measures.direction`) are given as
:func:`casacore.quanta.quantity`. Each of them can be either a scalar quantity
with a scalar or vector for its actual value (see the following example)::

    >>> from casacore.quanta import quantity
    >>> dm.epoch('utc','today')	# note that your value will be different
    {'m0': {'unit': 'd', 'value': 55147.912709756973},
     'refer': 'UTC',
     'type': 'epoch'}
    >>> dm.direction('j2000','5h20m','-30.2deg')
    {'m0': {'unit': 'rad', 'value': 1.3962634015954634},
     'm1': {'unit': 'rad', 'value': -0.52708943410228748},
     'refer': 'J2000',
     'type': 'direction'}
    >>> a = dm.direction('j2000','5h20m','-30.2deg')
    >>> print a['type']
    direction
    >>> dm.get_offset(a)
    None
    >>> dm.getref(a)
    J2000
    >>> dm.get_value(a)
    [1.3962634016 rad, -0.527089434102 rad]
    >>> dm.get_value(a)[0]
    1.3962634016 rad
    >>> dm.get_value(a)[1]
    -0.527089434102 rad
    >>> # try as a scalar quantity with multiple values
    >>> a = dm.direction('j2000', quantity([10,20],'deg'),
                     quantity([30,40], 'deg'))
    >>> dm.get_value(a)[0]
    [0.17453292519943295, 0.3490658503988659] rad
    >>> dm.get_value(a)[0].get_value()[1]
    0.3490658503988659
    >>> print a
    {'m0': {'unit': 'rad', 'value': array([ 0.17453293,  0.34906585])},
     'm1': {'unit': 'rad', 'value': array([ 0.52359878,  0.6981317 ])},
     'refer': 'J2000',
     'type': 'direction'}

Known measures are:

    * :meth:`~casacore.measures.measures.epoch`: an instance in time (internally
      expressed as MJD or MGSD)
    * :meth:`~casacore.measures.measures.direction`: a direction towards an
      astronomical object (including planets, sun, moon)
    * :meth:`~casacore.measures.measures.position`: a position on Earth
    * :meth:`~casacore.measures.measures.frequency`: electromagnetic wave energy
    * :meth:`~casacore.measures.measures.radialvelocity`: radial velocity of
      astronomical object
    * :meth:`~casacore.measures.measures.doppler`: doppler shift (i.e. radial
      velocity in non-velocity units like *Optical*, *Radio*.
    * :meth:`~casacore.measures.measures.baseline`: interferometer baseline
    * :meth:`~casacore.measures.measures.uvw`: UVW coordinates
    * :meth:`~casacore.measures.measures.earthmagnetic`: Earth' magnetic field

In addition to the reference code (like *J2000*), a measure needs sometimes
more information to be convertable to another reference code (e.g. a time
and position to convert it to an azimuth/elevation). This additional
information is called the reference frame, and can specify one or more of
'where am i', 'when is it', 'what direction", 'how fast'.

The frame values can be set using the method :meth:`measures.do_frame`.

Since you would normally work from a fixed position, the position frame
element ('where you are'), can be specified in your .aipsrc if its name is in
the Observatory list (obslist) tool function. You can set your preferred
position by adding to your *.casarc* file::

    measures.default.observatory:	atca

API
---

.. autofunction:: casacore.measures.is_measure

.. autoclass:: casacore.measures.measures
   :members:
   :exclude-members: asbaseline, doframe, framenow, getvalue, todop, todoppler,
                     torestfrequency, torest, touvw, tofrequency,
		     toradialvelocity
