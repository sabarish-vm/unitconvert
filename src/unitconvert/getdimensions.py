from collections import defaultdict


def getdim(q):
    q = q.si.decompose()
    q = q * 1
    sb = q.unit.bases
    sp = q.unit.powers
    dictdim = defaultdict(lambda: 0)
    for i in range(len(sb)):
        dictdim[sb[i]] = sp[i]
    return dictdim
