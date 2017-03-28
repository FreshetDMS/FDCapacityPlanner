import operator


def maxl(list):
    """ Return max using size attribute """
    return max(list, key=lambda x: x.size)


def minl(list):
    """ Return min using size attribute """
    return min(list, key=lambda x: x.size)


def sortl(list, dec=True):
    """ Sort list using size attribute.
    Items are sorted by decreasing order if rev = True,
    by increasing order otherwise """
    list.sort(key=lambda x: x.size, reverse=dec)
    return list


def vp_lower_bound(items, tbin):
    """ Return a lower bound on the minimum number of bins required
    assuming that all bins have the same capacities as tbin.
    This is a lower bound for the vector packing problem """
    if not items: return 0

    reqs = [0] * len(tbin.capacities)
    for i in items:
        reqs = map(operator.add, reqs, i.requirements)

    nbins = 0
    for w, c in zip(reqs, tbin.capacities):
        nb = w / c
        if w % c: nb += 1
        nbins = max(nbins, nb)

    return nbins
