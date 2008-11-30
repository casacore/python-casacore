#!/usr/bin/env python

from pyrap.util import substitute

a=1
b=2
p = "$((a+b)*(a+b))"
s = substitute(p)
print "a=%d, b=%d, %s => %s" % (a, b, p, s) 
