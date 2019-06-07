"""Tests casacore.images module."""
import unittest
from casacore.images import *
import numpy
import tempfile
import os
try:
    import numpy.ma as nma
except ImportError:
    import numpy.core.ma as nma


class TestImage(unittest.TestCase):
    """Unittesting Class."""

    tempdir = tempfile.gettempdir()
    os.chdir(tempdir)

    def test_image(self):
        """Create an image."""
        im = image("testimg", shape=[4, 3])
        im1 = image("", shape=[4, 3])
        self.assertEqual(im.ndim(), 2)
        self.assertEqual(im.shape(), [4, 3])
        self.assertEqual(len(im), 12)
        self.assertEqual(im.size(), 12)
        self.assertTrue(im.ispersistent())
        self.assertEqual(im.datatype(), 'float')
        self.assertEqual(im.imagetype(), 'PagedImage')

        self.assertEqual(im1.name(), 'Temporary_Image')
        self.assertEqual(im1.imagetype(), 'TempImage')

    def test_write_data(self):
        """Write data into it."""
        im = image("testimg", shape=[4, 3])
        im.put(numpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]))
        numpy.testing.assert_equal(im.getdata(),
                                   numpy.array([[1,  2,  3],
                                                [4,  5,  6],
                                                [7,  8,  9],
                                                [10, 11, 12]]))
        numpy.testing.assert_equal(im.getdata((0, 0), (2, 1)),
                                   numpy.array([[1, 2],
                                                [4, 5],
                                                [7, 8]]))
        # blc,trc,inc get adjusted
        numpy.testing.assert_equal(im.getdata(0, 2, 2),
                                   numpy.array([[1, 2, 3],
                                                [7, 8, 9]]))

    def test_image_mask(self):
        """Test image mask."""
        im1 = image("testimg", shape=[2, 3])
        marr = nma.masked_array(numpy.array([[1, 2, 3], [4, 5, 6]]),
                mask=[[False, True, False], [False, False, True]])
        im1.put(marr)
        numpy.testing.assert_equal(im1.getdata(), marr.data)
        numpy.testing.assert_equal(im1.getmask(), marr.mask)
        im1.putmask(numpy.array([[True, False, True],
                                [False, False, False]]), (0, 0), (0, 1))
        numpy.testing.assert_equal(im1.getmask(),
                                   numpy.array([[True, False,  True],
                                               [False, False, False]]))
        numpy.testing.assert_equal(im1.getdata(),
                                   numpy.array([[1, 2, 3], [4, 5, 6]]))
        im1.putdata(numpy.array([0, 1, 0]), (0, 0), (0, 1))
        numpy.testing.assert_equal(im1.getdata(),
                                   numpy.array([[0, 1, 0], [4, 5, 6]]))

    def test_image_mask2(self):
        """Test image mask."""
        marr = nma.masked_array(numpy.array([[1., 2, 3], [4, 5, 6]]),
                mask=[[False, True, False], [False, False, True]])
        im1 = image("testimg", values=marr)
        numpy.testing.assert_equal(im1.getdata(), marr.data)
        numpy.testing.assert_equal(im1.getmask(), marr.mask)

    def test_lock(self):
        """Test lock."""
        im = image("testimg", shape=[2, 3])
        im.saveas('timage.img1')
        im1 = image('timage.img1')
        self.assertTrue(im1.haslock())
        im1.unlock()
        self.assertFalse(im1.haslock())
        im1.lock()
        self.assertTrue(im1.haslock())

    def test_expr(self):
        """Create an expression from the image."""
        im = image("testimg", shape=[2, 3])
        im.put(numpy.array([[1, 2, 3], [4, 5, 6]]))
        imex = image('$im + $im')
        numpy.testing.assert_equal(imex.getdata(),
                                   numpy.array([[2.,   4.,   6.],
                                                [8.,  10.,  12.]]))

    def test_subset(self):
        """Create a subset and update it."""
        im = image("testimg", shape=[2, 3])
        im.put(numpy.array([[1, 2, 3], [4, 5, 6]]))
        im1 = im.subimage(0, 1, 2)
        numpy.testing.assert_equal(im1.getdata(),
                                   numpy.array([1, 2, 3]))
        im1.putdata(im1.getdata() + 1)
        numpy.testing.assert_equal(im1.getdata(),
                                   numpy.array([2, 3, 4]))
        numpy.testing.assert_equal(im.getmask(),
                                   numpy.array([[False, False, False],
                                                [False, False, False]]))

    def test_concimg(self):
        """Create a concatenated image."""
        im = image("testimg", shape=[2, 3])
        im.put(numpy.array([[1, 2, 3], [4, 5, 6]]))
        imc1 = image((im, im))
        self.assertEqual(imc1.shape(), [2, 6])
        numpy.testing.assert_equal(imc1.getdata(),
                                   numpy.array([[1, 2, 3, 1, 2, 3],
                                                [4, 5, 6, 4, 5, 6]]))
        imc1.saveas('timage.py_tmp.img1')
        imc2 = image('timage.py_tmp.img1')
        numpy.testing.assert_equal(imc2.getdata(),
                                   numpy.array([[1, 2, 3, 1, 2, 3],
                                                [4, 5, 6, 4, 5, 6]]))

    def test_float(self):
        """Create a float image expression with a mask."""
        im = image("testimg", shape=[2, 3])
        im.put(numpy.array([[1, 2, 3], [4, 5, 6]]))
        im.saveas('timage.py_tmp.img1')
        imex = image('float(timage.py_tmp.img1[timage.py_tmp.img1 > 3])')
        numpy.testing.assert_equal(imex.getdata(),
                                   numpy.array([[1, 2, 3],
                                                [4, 5, 6]]))
        numpy.testing.assert_equal(imex.getmask(),
                                   numpy.array([[True,  True,  True],
                                                [False, False, False]]))
        imex.saveas('timage.py_tmp.img2', copymask=True)
        imex2 = image('timage.py_tmp.img2', mask='mask0')
        numpy.testing.assert_equal(imex2.getmask(),
                                   numpy.array([[True,  True,  True],
                                                [False, False, False]]))
        imex2.put(imex2.getdata() + 10)
        numpy.testing.assert_equal(imex2.getdata(),
                                   numpy.array([[11, 12, 13],
                                                [14, 15, 16]]))
        print(imex2.statistics())
        imex2.tofits('timage.py_tmp.fits')
        imex3 = image('timage.py_tmp.fits')
        print(imex3.getdata())

    def test_image_coordinate(self):
        """Get some info on a coordinate system and change it."""
        im = image("testimg", shape=[2, 2, 2, 2])
        im.put(numpy.array([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
                            [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]]))
        imcor = im.coordinates()
        print(im.info())
        imcor.set_referencepixel([3, numpy.array([2]), numpy.array([1, 1])])
        numpy.testing.assert_equal(imcor.get_referencepixel(),
                                   [3, numpy.array([2]), numpy.array([1, 1])])
        self.assertIn('direction', imcor.get_names())
        self.assertAlmostEqual(imcor.get_obsdate()['m0']['value'],
                               51544.00000000116)
        self.assertEqual(imcor.get_observer(), 'Karl Jansky')
        self.assertEqual(imcor.get_telescope(), 'ALMA')
        imcor.set_referencevalue([1, numpy.array([2]), numpy.array([3, 4])])
        numpy.testing.assert_equal(imcor.get_referencevalue(),
                                   [1, numpy.array([2]), numpy.array([3, 4])])
        imcor.set_increment([4, numpy.array([3]), numpy.array([2, 1])])
        numpy.testing.assert_equal(imcor.get_increment(),
                                   [4, numpy.array([3]), numpy.array([2, 1])])
        numpy.testing.assert_equal(imcor.get_axes(),
                                   ['Frequency', ['Stokes'],
                                   ['Declination', 'Right Ascension']])
        print(imcor)
        self.assertEqual(imcor.get_unit(), ['Hz', [], ["'", "'"]])

    def test_direction_coordinate(self):
        """Tests direction coordinates."""
        im = image("testimg", shape=[2, 2, 2, 2])
        imcor = im.coordinates()
        dircor = imcor.get_coordinate('direction')
        print(dircor)
        self.assertEqual(dircor.get_axis_size(), 2)
        self.assertEqual(dircor.get_image_axis(), 2)
        dircor.set_referencepixel([3.0, 0.0])
        self.assertEqual(dircor.get_referencepixel(), [3.0, 0.0])
        self.assertEqual(dircor.get_projection(), 'SIN')
        dircor.set_projection('TAN')
        self.assertEqual(dircor.get_projection(), 'TAN')
        self.assertEqual(dircor.get_frame(), 'J2000')
        dircor.set_frame('B1950')
        self.assertEqual(dircor.get_frame(), 'B1950')

    def test_spectral_coordinate(self):
        """Tests spectral coordinates."""
        im = image("testimg", shape=[2, 2, 2, 2])
        imcor = im.coordinates()
        spcor = imcor.get_coordinate('spectral')
        print (spcor)
        self.assertEqual(spcor.get_axis_size(), 2)
        self.assertEqual(spcor.get_image_axis(), 0)
        self.assertEqual(spcor.get_unit(), 'Hz')
        spcor.set_referencepixel(2)
        self.assertEqual(spcor.get_referencepixel(), 2)
        spcor.set_referencevalue(2)
        self.assertEqual(spcor.get_referencevalue(), 2)
        spcor.set_increment(3)
        self.assertEqual(spcor.get_increment(), 3)
        self.assertEqual(spcor.get_axes(), 'Frequency')
        spcor.set_restfrequency(1200)
        self.assertEqual(spcor.get_restfrequency(), 1200)
        self.assertEqual(spcor.get_frame(), 'LSRK')
        spcor.set_frame('BARY')
        self.assertEqual(spcor.get_frame(), 'BARY')
        self.assertEqual(spcor.get_conversion()['direction']['m1']['unit'],
                         'rad')

    def tests_stokes_coordinate(self):
        """Tests stokes coordinates."""
        im = image("testimg", shape=[2, 2, 2, 2])
        imcor = im.coordinates()
        stkco = imcor.get_coordinate('stokes')
        self.assertEqual(stkco.get_axis_size(), 2)
        self.assertEqual(stkco.get_image_axis(), 1)
        self.assertEqual(stkco.get_stokes(), ['I', 'Q'])

        # TODO
        # Test AttrGroup
