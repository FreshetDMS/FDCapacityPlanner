import unittest
import itertools
import operator


################## Utility functions ####################



################## Instance ####################

class Instance:
    """ An instance """

    def __init__(self, items, bins):
        self.items = items[:]
        self.bins = bins[:]

    def __repr__(self):
        return "Items:\n" + str(self.items) + "\nBins:\n" + str(self.bins)

    def empty(self):
        for i in self.items: i.size = 0
        for b in self.bins: b.empty()


################## Items ####################

class Item(object):
    """ An item """

    def __init__(self, requirements):
        self.requirements = requirements[:]
        self.size = 0

    def __repr__(self):
        return str(self.requirements)


class ConstrainedItem(Item):
    def __init__(self, requirements):
        super(ConstrainedItem, self).__init__(requirements)

    def is_constraint_satisfied(self, bin):
        return True

################## Bins ####################

class Bin:
    """ A bin """

    def __init__(self, capacities):
        self.capacities = capacities[:]
        self.remaining = capacities[:]
        self.items = []
        self.size = 0

    def __repr__(self):
        return str([self.capacities, self.remaining])

    def feasible(self, item):
        """ 
        Return True iff item can be packed in this bin 
            - Item cannot be packed in this bin if item constraints are not satisfied
            - Or if there is not enough space left in the bin
        """
        if isinstance(item, ConstrainedItem):
            if not item.is_constraint_satisfied(self):
                return False

        for req, rem in itertools.izip_longest(item.requirements, self.remaining):
            if (req > rem):
                return False
        return True

    def insert(self, item):
        """
            Adds item to the bin
            Requires: the assignment is feasible
        """
        for i, req in enumerate(item.requirements):
            self.remaining[i] -= req
        self.items.append(item)

    def add(self, item):
        """
            Test feasibility and add item to the bin
            Return True if the item has been added, False o.w.
        """
        if self.feasible(item):
            self.insert(item)
            return True
        return False

    def empty(self):
        """ Empty the bin """
        self.items = []
        self.remaining = self.capacities[:]


################## Unit tests ####################



if __name__ == "__main__":
    unittest.main()
