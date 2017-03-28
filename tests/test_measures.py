from vsvbp.container import Item, Bin
from vsvbp.measures import *
import unittest


class MeasuresTestCase(unittest.TestCase):
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

    def testComputeRem(self):
        assert compute_item_req(self.items) == [14, 16, 19]
        assert compute_bin_res(self.bins) == [106, 10, 113]
        self.b1.add(self.i4)
        assert compute_bin_res(self.bins) == [106, 10, 113]
        self.b3.add(self.i3)
        assert compute_bin_res(self.bins) == [106, 9, 113]

    def testCMes(self):
        staticBinsOneOverC(self.items, self.bins, False)
        staticItemsOneOverC(self.items, self.bins, False)
        assert self.i1.size == 1
        assert self.i2.size == 2
        assert self.i3.size == 3
        assert self.i4.size == 0
        assert self.b1.size == 1
        assert self.b2.size == 2
        assert self.b3.size == 3

        staticBinsOneOverC(self.items, self.bins, True)
        staticItemsOneOverC(self.items, self.bins, True)
        assert abs(self.i1.size - (1. / 106 + 2. / 10 + 9. / 113)) < 10 ** -14
        assert abs(self.i2.size - (4. / 106 + 5. / 10 + 3. / 113)) < 10 ** -14
        assert abs(self.i3.size - (1. / 10)) < 10 ** -14
        assert abs(self.i4.size - (9. / 106 + 8. / 10 + 7. / 113)) < 10 ** -14
        assert abs(self.b1.size - (5. / 106 + 8. / 10 + 4. / 113)) < 10 ** -14
        assert abs(self.b2.size - (100. / 106 + 100. / 113)) < 10 ** -14
        assert abs(self.b3.size - (1. / 106 + 2. / 10 + 9. / 113)) < 10 ** -14

        self.bins.pop()
        dynamicBinsOneOverC(self.items, self.bins, True)
        dynamicItemsOneOverC(self.items, self.bins, True)
        assert abs(self.i1.size - (1. / 106 + 2. / 10 + 9. / 113)) < 10 ** -14
        assert abs(self.i2.size - (4. / 106 + 5. / 10 + 3. / 113)) < 10 ** -14
        assert abs(self.i3.size - (1. / 10)) < 10 ** -14
        assert abs(self.i4.size - (9. / 106 + 8. / 10 + 7. / 113)) < 10 ** -14
        assert abs(self.b1.size - (5. / 106 + 8. / 10 + 4. / 113)) < 10 ** -14
        assert abs(self.b2.size - (100. / 106 + 100. / 113)) < 10 ** -14
        assert abs(self.b3.size - (1. / 106 + 2. / 10 + 9. / 113)) < 10 ** -14

        dynamicBinsOneOverC(self.items, self.bins)
        dynamicItemsOneOverC(self.items, self.bins)
        assert abs(self.i1.size - (1. / 105 + 2. / 8 + 9. / 104)) < 10 ** -14
        assert abs(self.i2.size - (4. / 105 + 5. / 8 + 3. / 104)) < 10 ** -14
        assert abs(self.i3.size - (1. / 8)) < 10 ** -14
        assert abs(self.i4.size - (9. / 105 + 8. / 8 + 7. / 104)) < 10 ** -14
        assert abs(self.b1.size - (5. / 105 + 8. / 8 + 4. / 104)) < 10 ** -14
        assert abs(self.b2.size - (100. / 105 + 100. / 104)) < 10 ** -14
        assert abs(self.b3.size - (1. / 106 + 2. / 10 + 9. / 113)) < 10 ** -14

    def testRMes(self):
        staticBinsOneOverR(self.items, self.bins, False)
        staticItemsOneOverR(self.items, self.bins, False)
        assert self.i1.size == 1
        assert self.i2.size == 2
        assert self.i3.size == 3
        assert self.i4.size == 0
        assert self.b1.size == 1
        assert self.b2.size == 2
        assert self.b3.size == 3

        staticBinsOneOverR(self.items, self.bins, True)
        staticItemsOneOverR(self.items, self.bins, True)
        assert abs(self.i1.size - (1. / 14 + 2. / 16 + 9. / 19)) < 10 ** -14
        assert abs(self.i2.size - (4. / 14 + 5. / 16 + 3. / 19)) < 10 ** -14
        assert abs(self.i3.size - (1. / 16)) < 10 ** -14
        assert abs(self.i4.size - (9. / 14 + 8. / 16 + 7. / 19)) < 10 ** -14
        assert abs(self.b1.size - (5. / 14 + 8. / 16 + 4. / 19)) < 10 ** -14
        assert abs(self.b2.size - (100. / 14 + 100. / 19)) < 10 ** -14
        assert abs(self.b3.size - (1. / 14 + 2. / 16 + 9. / 19)) < 10 ** -14

        self.items.pop(0)
        dynamicBinsOneOverR(self.items, self.bins, True)
        dynamicItemsOneOverR(self.items, self.bins, True)
        assert abs(self.i1.size - (1. / 14 + 2. / 16 + 9. / 19)) < 10 ** -14
        assert abs(self.i2.size - (4. / 14 + 5. / 16 + 3. / 19)) < 10 ** -14
        assert abs(self.i3.size - (1. / 16)) < 10 ** -14
        assert abs(self.i4.size - (9. / 14 + 8. / 16 + 7. / 19)) < 10 ** -14
        assert abs(self.b1.size - (5. / 14 + 8. / 16 + 4. / 19)) < 10 ** -14
        assert abs(self.b2.size - (100. / 14 + 100. / 19)) < 10 ** -14
        assert abs(self.b3.size - (1. / 14 + 2. / 16 + 9. / 19)) < 10 ** -14

        dynamicBinsOneOverR(self.items, self.bins)
        dynamicItemsOneOverR(self.items, self.bins)
        assert abs(self.i1.size - (1. / 5 + 2. / 8 + 9. / 12)) < 10 ** -14
        assert abs(self.i2.size - (4. / 5 + 5. / 8 + 3. / 12)) < 10 ** -14
        assert abs(self.i3.size - (1. / 8)) < 10 ** -14
        assert abs(self.i4.size - (9. / 14 + 8. / 16 + 7. / 19)) < 10 ** -14
        assert abs(self.b1.size - (5. / 5 + 8. / 8 + 4. / 12)) < 10 ** -14
        assert abs(self.b2.size - (100. / 5 + 100. / 12)) < 10 ** -14
        assert abs(self.b3.size - (1. / 5 + 2. / 8 + 9. / 12)) < 10 ** -14

    def testRCMes(self):
        staticBinsROverC(self.items, self.bins, False)
        staticItemsROverC(self.items, self.bins, False)
        assert self.i1.size == 1
        assert self.i2.size == 2
        assert self.i3.size == 3
        assert self.i4.size == 0
        assert self.b1.size == 1
        assert self.b2.size == 2
        assert self.b3.size == 3

        staticBinsROverC(self.items, self.bins, True)
        staticItemsROverC(self.items, self.bins, True)
        assert abs(self.i1.size - (14. / 106. + 2. * 16. / 10. + 9. * 19. / 113.)) < 10 ** -14
        assert abs(self.i2.size - (4. * 14. / 106. + 5. * 16. / 10. + 3. * 19. / 113.)) < 10 ** -14
        assert abs(self.i3.size - (16. / 10.)) < 10 ** -14
        assert abs(self.i4.size - (9. * 14. / 106. + 8. * 16. / 10. + 7. * 19. / 113.)) < 10 ** -14
        assert abs(self.b1.size - (5. * 14. / 106. + 8. * 16. / 10. + 4. * 19. / 113.)) < 10 ** -14
        assert abs(self.b2.size - (100. * 14. / 106. + 100. * 19. / 113.)) < 10 ** -14
        assert abs(self.b3.size - (14. / 106. + 2. * 16. / 10. + 9. * 19. / 113.)) < 10 ** -14

        i = self.items.pop(2)
        assert self.b1.add(i)
        dynamicBinsROverC(self.items, self.bins, True)
        dynamicItemsROverC(self.items, self.bins, True)
        assert abs(self.i1.size - (14. / 106. + 2. * 16. / 10. + 9. * 19. / 113.)) < 10 ** -14
        assert abs(self.i2.size - (4. * 14. / 106. + 5. * 16. / 10. + 3. * 19. / 113.)) < 10 ** -14
        assert abs(self.i3.size - (16. / 10.)) < 10 ** -14
        assert abs(self.i4.size - (9. * 14. / 106. + 8. * 16. / 10. + 7. * 19. / 113.)) < 10 ** -14
        assert abs(self.b1.size - (5. * 14. / 106. + 8. * 16. / 10. + 4. * 19. / 113.)) < 10 ** -14
        assert abs(self.b2.size - (100. * 14. / 106. + 100. * 19. / 113.)) < 10 ** -14
        assert abs(self.b3.size - (14. / 106. + 2. * 16. / 10. + 9. * 19. / 113.)) < 10 ** -14

        dynamicBinsROverC(self.items, self.bins)
        dynamicItemsROverC(self.items, self.bins)
        assert abs(self.i1.size - (10. / 102. + 2. * 11. / 5. + 9. * 16. / 110.)) < 10 ** -14
        assert abs(self.i2.size - (4. * 14. / 106. + 5. * 16. / 10. + 3. * 19. / 113.)) < 10 ** -14
        assert abs(self.i3.size - (11. / 5.)) < 10 ** -14
        assert abs(self.i4.size - (9. * 10. / 102. + 8. * 11. / 5. + 7. * 16. / 110.)) < 10 ** -14
        assert abs(self.b1.size - (10. / 102. + 3. * 11. / 5. + 16. / 110.)) < 10 ** -14
        assert abs(self.b2.size - (100. * 10. / 102. + 100. * 16. / 110.)) < 10 ** -14
        assert abs(self.b3.size - (10. / 102. + 2. * 11. / 5. + 9. * 16. / 110.)) < 10 ** -14