import unittest
from vsvbp.container import Item, Bin, Instance
from vsvbp.generator import generator


class ItemBinTestCase(unittest.TestCase):
    def setUp(self):
        self.i1 = Item([1,2,9]); self.i2 = Item([4,5,3])
        self.i3 = Item([0,1,0]); self.i4 = Item([9,8,7])
        self.i1.size = 1; self.i2.size = 2; self.i3.size = 3; self.i4.size = 0;
        self.items = [self.i4, self.i3, self.i2, self.i1]
        self.b1=Bin([5,8,4]); self.b2=Bin([100,0,100]); self.b3=Bin([1,2,9]);
        self.b1.size=1; self.b2.size=2; self.b3.size=3;
        self.bins = [self.b1,self.b2,self.b3]
        self.ins = Instance(self.items, self.bins)

    def testInstance(self):
        assert str(self.ins)=="Items:\n"+str(self.items)+"\nBins:\n"+str(self.bins)

    def testGenerator(self):
        iss=generator(2,2,.5,seed=0)
        assert iss.items[1].requirements==[356, 197]
        assert iss.bins[1].capacities == [516,411]