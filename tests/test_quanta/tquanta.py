#!/usr/bin/env python

from pyrap.quanta import *

q0 = quantity('1deg')
print is_quantity(q0)
q1 = quantity(1.0, 'deg')
print is_quantity(q1)
print q1 == q0
q2 = quantity([180.0, 0.0], 'deg')
print is_quantity(q2)
print q1 != q2
print q0+q1
print q0-q1
print q0*q1
print q0/q1
print q0+1
print q2+[1,1]
print sin(q0)
print sin(q2)
print q0.get()
print q0.get('h')
print q0.canonical()
print q0.get_value()
print q0.get_value('arcsec')
print q0.get_unit()
q3 = quantity('12h10m5s')
print q3.to_time()
print q3.to_unix_time()
print q3.to_angle()
print q3.formatted("ANGLE")
print q3.to_string("%0.3f")

