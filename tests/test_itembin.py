import unittest
from vsvbp.container import Bin, Item
from vsvbp.utils import *


class ItemBinTestCase(unittest.TestCase):
    def dummy_item_size(self, list):
        for i in list:
            i.size = i.requirements[1]

    def setUp(self):
        l = [1, 5, 9]
        self.b0 = Bin(l)
        l[0] = 10;
        l[1] = 1;
        l[2] = 7
        self.b1 = Bin(l)
        self.totalCap = [sum(v) for v in zip(self.b0.capacities, self.b1.capacities)]
        self.i1 = Item([0, 4, 3])
        self.i2 = Item([1, 1, 3])

    def testItem(self):
        assert self.i1.requirements == [0, 4, 3]
        assert self.i2.requirements != [0, 4, 3]

    def testBin(self):
        assert self.b0.capacities == [1, 5, 9]
        assert not self.b1.add(self.i1)
        assert self.b1.add(self.i2)
        assert self.b1.capacities == [10, 1, 7]
        assert self.b1.remaining == [9, 0, 4]
        assert not self.b1.add(self.i2)
        self.b1.empty()
        assert self.b1.remaining == self.b1.capacities

    def testItemUnchanged(self):
        assert not self.b1.add(self.i1)
        assert self.i1.requirements == [0, 4, 3]
        assert self.b0.add(self.i1)
        assert self.i1.requirements == [0, 4, 3]

    def testMaxAndSort(self):
        i3 = Item([.5, 2, 1])
        l = [self.i1, self.i2, i3]
        self.dummy_item_size(l)
        assert maxl(l) == self.i1
        assert minl(l) == self.i2
        sortl(l)
        assert l == [self.i1, i3, self.i2]
        sortl(l, False)
        assert l == [self.i2, i3, self.i1]
        assert maxl(l) == self.i1
        assert minl(l) == self.i2

    def testLB(self):
        assert vp_lower_bound([], None) == 0
        items = [self.i1, self.i2]
        assert vp_lower_bound(items, Bin([1, 1, 1])) == 6
        assert vp_lower_bound(items, Bin([8, 8, 8])) == 1
        assert vp_lower_bound(items, Bin([2, 4, 6])) == 2
        assert vp_lower_bound(items, Bin([2, 5, 2])) == 3
