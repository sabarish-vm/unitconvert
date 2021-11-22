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

def Naturalunitsfactor(q):
    dimdict = getdim(1*q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {'hbar':1/2*(2*b + 2*c - d), 'c' : 1/2*(-4*a + 2*b  +d), 'k_B' : -e ,'eps0' : d/2  }
    factor = acon.hbar**(1/2*(2*b + 2*c - d)) * acon.c**(1/2*(-4*a + 2*b  +d)) * acon.k_B**(-e) * acon.eps0**(d/2)
    return factorlist

def getFactor(q) :
    fac = Naturalunitsfactor(q)
    factor = acon.hbar**(fac['hbar']) * acon.c**(fac['c']) * acon.k_B**(fac['k_B']) * acon.eps0**(fac['eps0'])
    return factor

def toNaturalunits(q) :
    q = 1*q
    factor = getFactor(q)
    natqu = q/factor
    massdim = getdim(natqu)[u.kg]
    try :
        return natqu.to(u.eV**massdim)
    except :
        return q

def fromNaturalunits(q,finalUnits) :
    factor = getFactor(finalUnits)
    return (q*factor).to(finalUnits)
    

