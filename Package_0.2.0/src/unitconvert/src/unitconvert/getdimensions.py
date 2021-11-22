import astropy.units as u
import astropy.constants as acon

def getdim(q):
    q = q*1
    q = q.si.decompose()
    sb = q.unit.bases
    sp = q.unit.powers
    dictdim = defaultdict(lambda : 0)
    for i in range(len(sb)):
        dictdim[sb[i]] = sp[i]
    return dictdim