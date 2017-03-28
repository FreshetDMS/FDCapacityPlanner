from vsvbp.container import Item, Bin, Instance
from vsvbp.solver import is_feasible, optimize
import unittest


class OptimizationTestCase(unittest.TestCase):
    def setUp(self):
        self.items = [Item([0,4,3]), Item([1,1,3]), Item([5,2,1]), Item([3,1,7])]
        self.bins = [Bin([5,5,8]), Bin([8,5,9]), Bin([3,3,5])]

    def testFeasible(self):
        bins = [Bin(self.bins[0].capacities) for i in xrange(5)]
        inst = Instance(self.items[:], bins)
        assert is_feasible(inst, True)

        bins = [Bin(self.bins[0].capacities) for i in xrange(2)]
        inst = Instance(self.items[:], bins)
        assert not is_feasible(inst, True)

        # Warning: this test may fail if the heuristics perform poorly
        bins = [Bin(self.bins[1].capacities) for i in xrange(3)]
        inst = Instance(self.items[:], bins)
        assert is_feasible(inst, True)

        bins = [Bin(self.bins[2].capacities) for i in xrange(15)]
        inst = Instance(self.items[:], bins)
        assert not is_feasible(inst, True)

    def testOptimize(self):
        # Warning: these tests may fail if the heuristics perform poorly
        assert len(optimize(self.items, self.bins[0], True).bins) == 3
        assert len(optimize(self.items, self.bins[1], True).bins) == 2
        assert optimize(self.items, self.bins[2], True) is None
