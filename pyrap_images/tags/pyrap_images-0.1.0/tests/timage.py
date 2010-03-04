#!/usr/bin/env python

from pyrap.images import *
import numpy

# Create an image
im = image("", shape=[4,3])
print im.ndim(), im.shape(), len(im), im.size(), im.ispersistent(), im.datatype(), im.name()
# Write data into it
im.put (numpy.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]]))
print im.getdata()
print im.getdata((0,0),(2,1))
print im.getdata(0,2,2)          # blc,trc,inc get adjusted
# Create an expression from it
imex = image('$im + $im')
print imex.getdata()
# Create a subset and update it.
im1 = im.subimage(0,2,2)
print im1.getdata()
im1.putdata (im1.getdata() + 1)
print im.getdata()
print im.getmask()
# Create a concatenated image.
imc1 = image((im,imex))
print imc1.shape()
print imc1.getdata()
imc1.saveas ('timage.py_tmp.img1')
imc2 = image('timage.py_tmp.img1')
print imc2.getdata()
# Create a float image expression with a mask
imex = image('float(timage.py_tmp.img1[timage.py_tmp.img1 > 3])')
print imex.getdata()
print imex.getmask()
imex.saveas ('timage.py_tmp.img2', copymask=True)
imex2 = image('timage.py_tmp.img2', mask='mask0')
print imex2.getmask()
imex2.put (imex2.getdata() + 10)
print imex2.getdata()
print imex2.statistics()     # takes mask into account!
imex2.tofits('timage.py_tmp.fits')
imex3 = image('timage.py_tmp.fits')
print imex3.getdata()
