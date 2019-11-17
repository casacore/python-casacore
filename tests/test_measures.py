import unittest
from casacore import measures

class TestMeasures(unittest.TestCase):
    def test_epoch(self):
        dm = measures.measures()
        epoch = dm.epoch(rf='utc', v0='2009-09-09T09:09')
        epoch_d = dm.get_value(epoch)
