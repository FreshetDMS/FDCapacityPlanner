"""
    Provides a basic framework for optimization for vector packing problems using the heuristics

    This is not exact and neither run-time optimized
"""

from .container import *
from .heuristics import *
from .generator import *
from .measures import *
from fdcp.aws import InstanceBin
import random
import logging

logger = logging.getLogger("vsvbp-solver")


# Create a list of heuristics with valid combinations of measures
class HeuristicList(object):
    pass


__hlist = HeuristicList()

# Static bfd ic/bc heuristics
__hlist.static = [
    (do_nothing, do_nothing),
    (shuffleItemsOnce, shuffleBinsOnce),
    (staticItemsOneOverC, staticBinsOneOverC),
    (staticItemsOneOverR, staticBinsOneOverR),
    (staticItemsROverC, staticBinsROverC)
]

# Dynamic heuristics
__hlist.dynamic = [
    (shuffleItems, shuffleBins),
    (dynamicItemsOneOverC, dynamicBinsOneOverC),
    (dynamicItemsOneOverR, dynamicBinsOneOverR),
    (dynamicItemsROverC, dynamicBinsROverC)
]

# Bin balancing heuristics
__hlist.balance = [
    (do_nothing, do_nothing),
    (shuffleItemsOnce, shuffleBinsOnce),
    (shuffleItems, shuffleBins),
    (staticItemsOneOverC, staticBinsOneOverC),
    (dynamicItemsOneOverC, dynamicBinsOneOverC),
    (staticItemsOneOverR, staticBinsOneOverR),
    (dynamicItemsOneOverR, dynamicBinsOneOverR),
    (staticItemsROverC, staticBinsROverC),
    (dynamicItemsROverC, dynamicBinsROverC)
]

# Dot Product heuristics
__hlist.dotprod = [
    (dp_nonorm, do_nothing),
    (dp_normC, do_nothing),
    (dp_normR, do_nothing)
]


def is_feasible(instance, use_dp=False):
    """ Run all heuristics and return True iff a heuristic finds
    a feasible solution. Return False otherwise.

    We emphasize that this code is NOT optimized at all. We could
    make each much faster by starting with the heuristics which have
    the best success chances."""

    logger.debug("Running is_feasible with bins: " + str(len(instance.bins)))

    # Run static heuristics
    logger.debug("Running static heuristics")
    for m1, m2 in __hlist.static:
        instance.empty()
        ret = bfd_item_centric(instance.items[:], instance.bins[:], m1, m2)
        if not ret:
            return True

    # Run item centric dynamic heuristics
    logger.debug("Running dynamic heuristics")
    for m1, m2 in __hlist.dynamic:
        instance.empty()
        ret = bfd_item_centric(instance.items[:], instance.bins[:], m1, m2)
        if not ret:
            return True

    # Run bin centric dynamic heuristics
    logger.debug("Running bin centric dynamic heuristics")
    for m1, m2 in __hlist.dynamic:
        instance.empty()
        ret = bfd_bin_centric(instance.items[:], instance.bins[:], m1, m2)
        if not ret:
            return True

    # Run bin balancing heuristics
    logger.debug("Running bin balancing heuristics")
    for m1, m2 in __hlist.balance:
        instance.empty()
        ret = bin_balancing(instance.items[:], instance.bins[:], m1, m2)
        if not ret:
            return True

    # Run single bin balancing heuristics
    logger.debug("Running single bin balancing heuristics")
    for m1, m2 in __hlist.balance:
        instance.empty()
        ret = bin_balancing(instance.items[:], instance.bins[:], m1, m2, single=True)
        if not ret:
            return True

    # Run Dot Product heuristics
    if not use_dp:
        return False

    logger.debug("Running dot product heuristics")
    for m1, m2 in __hlist.dotprod:
        instance.empty()
        ret = bfd_item_centric(instance.items[:], instance.bins[:], m1, m2)
        if not ret:
            return True

    # No solution found
    return False


def optimize(items, tbin, use_dp=False, seed=None, aws=False):
    """ Performs a binary search and returns the best solution
        found for the vector bin packing problem.

    Keyword arguments:
        items -- a list of items (Item) to pack
        tbin -- a typical Bin: all bins have the same capacities as tbin

    Return the best solution found. len(ret.bins) is the best number of bins found.
    """
    # replace by the following line to return lower bounds
    # return Instance([], [tbin]*vp_lower_bound(items, tbin))

    if seed is not None:
        random.seed(seed)

    lb = int(math.ceil(vp_lower_bound(items, tbin)))
    ub = len(items)
    best = None
    while lb <= ub:
        mid = (lb + ub) / 2
        if not aws:
            bins = [Bin(tbin.capacities) for i in xrange(mid)]
        else:
            bins = [InstanceBin(tbin.instance_type, tbin.storage_type, tbin.io_op_size_kb) for i in xrange(mid)]
        inst = Instance(items[:], bins)
        if is_feasible(inst, use_dp):
            best = inst
            ub = mid - 1
        else:
            lb = mid + 1

    return best
