"""
Various size functions (measures)
They are all defined by :
    measure(items, bins, init=False)
A first run, with init = True is supposed to be run. During this run,
all structures are initialized.
In the following runs, sizes are updated.

These mesures alter attributes sizes from bins and items

Note that most measures perform some unnecessary redundant computations
"""

import random
import itertools
import math


################## Measures ####################

########## Random measures ##########

def do_nothing(items, bins, init=False):
    """ Stub measure - do not alter any of the sizes """
    return


def shuffleBins(items, bins, init=False):
    """ Assign random sizes to the bins if init is set to False """
    if init: return
    for b in bins:
        b.size = random.random()


def shuffleBinsOnce(items, bins, init=False):
    """ Assign random sizes to the bins on the first invocation
    after a call with init = True """
    if init:
        shuffleBins.go = True
    elif shuffleBins.go:
        random.shuffle(bins)
        shuffleBins.go = False


def shuffleItems(items, bins, init=False):
    """ Assign random sizes to the items if init is set to False """
    if init: return
    for i in items:
        i.size = random.random()


def shuffleItemsOnce(items, bins, init=False):
    """ Assign random sizes to the items on the first invocation
    after a call with init = True """
    if init:
        shuffleItems.go = True
    elif shuffleItems.go:
        random.shuffle(items)
        shuffleItems.go = False


########## Some useful functions ##########     

def compute_item_req(items):
    """ Computes total requirements """
    if not items:
        return 0
    s = len(items[0].requirements)
    req = [0] * s
    for i in items:
        for j in xrange(s):
            req[j] += i.requirements[j]
    return req


def compute_bin_res(bins):
    """ Computes total remaining bin resources """
    if not bins:
        return 0
    s = len(bins[0].remaining)
    rem = [0] * s
    for b in bins:
        for j in xrange(s):
            rem[j] += b.remaining[j]
    return rem


########## Normalize by 1/C ##########

def staticBinsOneOverC(items, bins, init=False):
    """ Static measure : bins sizes are updated once.
    alpha = beta = 1/C(r) """
    if init:
        dynamicBinsOneOverC(items, bins)


def staticItemsOneOverC(items, bins, init=False):
    """ Static measure : items sizes are updated once.
    alpha = beta = 1/C(r) """
    if init:
        dynamicItemsOneOverC(items, bins)


def dynamicBinsOneOverC(items, bins, init=False):
    """ Dynamic measure : bins sizes are always recomputed.
    alpha = beta = 1/C(r) """
    if init: return
    res = compute_bin_res(bins)
    if res == 0: return
    res = [1 / float(i) if i != 0 else 0 for i in res]
    for i in bins:
        i.size = 0
        for j, r in enumerate(i.remaining):
            i.size += res[j] * r


def dynamicItemsOneOverC(items, bins, init=False):
    """ Dynamic measure : items sizes are always recomputed.
    alpha = beta = 1/C(r) """
    if init: return
    res = compute_bin_res(bins)
    if res == 0: return
    res = [1 / float(i) if i != 0 else 0 for i in res]
    for i in items:
        i.size = 0
        for j, r in enumerate(i.requirements):
            i.size += res[j] * r


########## Normalize by 1/R ##########

def staticBinsOneOverR(items, bins, init=False):
    """ Static measure : bins sizes are updated once.
    alpha = beta = 1/R(r) """
    if init:
        dynamicBinsOneOverR(items, bins)


def staticItemsOneOverR(items, bins, init=False):
    """ Static measure : items sizes are updated once.
    alpha = beta = 1/R(r) """
    if init:
        dynamicItemsOneOverR(items, bins)


def dynamicBinsOneOverR(items, bins, init=False):
    """ Dynamic measure : bins sizes are always recomputed.
    alpha = beta = 1/R(r) """
    if init: return
    res = compute_item_req(items)
    if res == 0: return
    res = [1 / float(i) if i != 0 else 0 for i in res]
    for i in bins:
        i.size = 0
        for j, r in enumerate(i.remaining):
            i.size += res[j] * r


def dynamicItemsOneOverR(items, bins, init=False):
    """ Dynamic measure : items sizes are always recomputed.
    alpha = beta = 1/R(r) """
    if init: return
    res = compute_item_req(items)
    if res == 0: return
    res = [1 / float(i) if i != 0 else 0 for i in res]
    for i in items:
        i.size = 0
        for j, r in enumerate(i.requirements):
            i.size += res[j] * r


########## Normalize by R/C ##########

def staticBinsROverC(items, bins, init=False):
    """ Static measure : bins sizes are updated once.
    alpha = beta = R(r)/C(r) """
    if init:
        dynamicBinsROverC(items, bins)


def staticItemsROverC(items, bins, init=False):
    """ Static measure : items sizes are updated once.
    alpha = beta = R(r)/C(r) """
    if init:
        dynamicItemsROverC(items, bins)


def dynamicBinsROverC(items, bins, init=False):
    """ Dynamic measure : bins sizes are always recomputed.
    alpha = beta = R(r)/C(r) """
    if init: return
    req = compute_item_req(items)
    if req == 0: return
    res = compute_bin_res(bins)
    if res == 0: return
    for i, v in enumerate(res):
        if v == 0:
            req[i] = 0
        else:
            req[i] /= float(v)

    for i in bins:
        i.size = 0
        for j, r in enumerate(i.remaining):
            i.size += req[j] * r


def dynamicItemsROverC(items, bins, init=False):
    """ Dynamic measure : items sizes are always recomputed.
    alpha = beta = R(r)/C(r) """
    if init: return
    req = compute_item_req(items)
    if req == 0: return
    res = compute_bin_res(bins)
    if res == 0: return
    for i, v in enumerate(res):
        if v == 0:
            req[i] = 0
        else:
            req[i] /= float(v)

    for i in items:
        i.size = 0
        for j, r in enumerate(i.requirements):
            i.size += req[j] * r

            ########## Norm based ##########


def norm(item, bin):
    # x is the coefficient minimizing sum_{p,m}((x*R(p,r)-C(m,r))^2)
    # in other word : x is the projection of C over normalized R
    x = 0
    div = 0
    for i, b in itertools.izip(item.requirements, bin.remaining):
        if i > b: return float('inf')
        x += i * b
        div += i * i
    x /= float(div)
    s = 0
    for i, b in itertools.izip(item.requirements, bin.remaining):
        s += (x * i - b) ** 2
    return s


def similarity(items, bins, init=False):
    """ Finds bins and items which are the most similar """
    if init: return
    best = float('inf')
    # without initialization, will crash if no item can be packed
    best_item = items[0]
    best_bin = bins[0]
    for i in items:
        for b in bins:
            n = norm(i, b)
            if n < best:
                best = n
                best_bin = b
                best_item = i

    for b in bins:
        if b == best_bin:
            b.size = 0
        else:
            b.size = 1
    for i in items:
        if i == best_item:
            i.size = 2
        else:
            i.size = 1


def dp(item, bin, normC, normR):
    """ dot product, if normR, normalize requirements by ||R|| and capacities by ||C||
    if normC, normalize requirements and capacities by ||C||
    Very unefficient : if we memorize previous results, dp on one bin only need
    to be computed on a given iteration """
    scal = 0
    normI = 0
    normB = 0
    for i, b in itertools.izip(item.requirements, bin.remaining):
        if i > b: return -1  # i cannot be packed into b
        scal += i * b
        normI += i * i
        normB += b * b
    if not normC and not normR:
        return scal
    if normR:
        return scal / (math.sqrt(normI) * math.sqrt(normB))
    return scal / float(normB)


def dot_product(items, bins, init=False, normC=False, normR=False):
    """ Finds bins and items which are the most similar, using dot product """
    if init: return  # more efficient approach would use this step to initialize sizes
    best = -1
    # without initialization, will crash if no item can be packed
    best_item = items[0]
    best_bin = bins[0]
    for i in items:
        for b in bins:
            n = dp(i, b, normC, normR)
            if n > best:
                best = n
                best_bin = b
                best_item = i

    for b in bins:
        if b == best_bin:
            b.size = 0
        else:
            b.size = 1
    for i in items:
        if i == best_item:
            i.size = 2
        else:
            i.size = 1


def dp_nonorm(items, bins, init=False):
    dot_product(items, bins, init=False, normC=False, normR=False)


def dp_normC(items, bins, init=False):
    dot_product(items, bins, init=False, normC=True, normR=False)


def dp_normR(items, bins, init=False):
    dot_product(items, bins, init=False, normR=True)
