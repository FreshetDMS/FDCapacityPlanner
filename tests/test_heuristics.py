from vsvbp.container import Item, Bin
from vsvbp.heuristics import *
from vsvbp.measures import do_nothing
import unittest


class HeuristicsTestCase(unittest.TestCase):
    def setUp(self):
        self.i1 = Item([1, 2, 9])
        self.i2 = Item([4, 5, 3])
        self.i3 = Item([0, 1, 0])
        self.i4 = Item([9, 8, 7])
        self.i1.size = 1
        self.i2.size = 2
        self.i3.size = 3
        self.i4.size = 0
        self.items = [self.i4, self.i3, self.i2, self.i1]
        self.b1 = Bin([5, 8, 4])
        self.b2 = Bin([100, 0, 100])
        self.b3 = Bin([1, 2, 9])
        self.b1.size = 1
        self.b2.size = 2
        self.b3.size = 3
        self.bins = [self.b1, self.b2, self.b3]

    def testItemCentricSuccess(self):
        ret = bfd_item_centric(self.items[1:], self.bins, do_nothing, do_nothing)
        assert ret == []

    def testItemCentricFailure(self):
        ret = bfd_item_centric(self.items, self.bins, do_nothing, do_nothing)
        assert self.b3.items == [self.i1]
        assert self.b2.items == []
        assert self.b1.items == [self.i3, self.i2]
        assert ret == [(3, self.i4)]

    def testBinCentricSuccess(self):
        ret = bfd_bin_centric(self.items[1:], self.bins, do_nothing, do_nothing)
        assert ret == []

    def testBinCentricFailure(self):
        ret = bfd_bin_centric(self.items, self.bins, do_nothing, do_nothing)
        assert self.b3.items == [self.i1]
        assert self.b2.items == []
        assert self.b1.items == [self.i3, self.i2]
        assert ret == [(3, self.i4)]

    def testFailure(self):
        self.i4.size = 10
        ret = bfd_item_centric(self.items, self.bins, do_nothing, do_nothing)
        assert self.b3.items == [self.i1]
        assert self.b2.items == []
        assert self.b1.items == [self.i3, self.i2]
        assert ret == [(0, self.i4)]
        self.setUp()
        self.i4.size = 10
        ret = bfd_bin_centric(self.items, self.bins, do_nothing, do_nothing)
        assert self.b3.items == [self.i1]
        assert self.b2.items == []
        assert self.b1.items == [self.i3, self.i2]
        assert ret == [(3, self.i4)]

    def testOriginalBinBalancing(self):
        self.i2.requirements = [1, 1, 1]
        ret = bin_balancing(self.items, self.bins, do_nothing, do_nothing, False)
        assert self.b1.items == [self.i3]
        assert self.b2.items == []
        assert self.b3.items == [self.i2]
        assert ret == [(2, self.i1), (3, self.i4)]

    def testSingleBinBalancing(self):
        self.i2.requirements = [1, 1, 1]
        ret = bin_balancing(self.items, self.bins, do_nothing, do_nothing, True)
        assert self.b1.items == [self.i3]
        assert self.b2.items == []
        assert self.b3.items == [self.i2]
        assert ret == [(2, self.i1), (3, self.i4)]
