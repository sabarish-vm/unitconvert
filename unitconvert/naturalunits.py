import astropy.units as u
import astropy.constants as acon
from collections import defaultdict

def getdim(q):
    q = q*1
    q = q.si.decompose()
    sb = q.unit.bases
    sp = q.unit.powers
    dictdim = defaultdict(lambda : 0)
    for i in range(len(sb)):
        dictdim[sb[i]] = sp[i]
    return dictdim

def Natfactor(q) :
    dimdict = getdim(1*q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factor = acon.hbar**(1/2*(2*b + 2*c - d)) * acon.c**(1/2*(-4*a + 2*b  +d)) * acon.k_B**(-e) * acon.eps0**(d/2)
    return factor

def toNaturalunits(q) :
    q = 1*q
    factor = Natfactor(q)
    natqu = q/factor
    massdim = getdim(natqu)[u.kg]
    return natqu.to(u.eV**massdim)

def fromNaturalunits(q,finalUnits) :
    factor = Natfactor(finalUnits)
    return (q*factor).to(finalUnits)
    

