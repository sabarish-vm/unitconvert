import astropy.units as u
import astropy.constants as acon
from collections import defaultdict
import getdimensions *

def geometrizedfactor(q):
    dimdict = getdim(1*q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {'c' : 2*a - c , 'G' : -a }
    factor = acon.c**(2*a - c) * acon.G**(-a)
    return factor,factorlist

def toGeometrized(q) :
    q = 1*q
    factor = geometrizedfactor(q)[0]
    natqu = q/factor
    lendim = getdim(natqu)[u.m]
    return natqu.to(u.m**lendim)

def fromGeometrized(q,finalUnits) :
    factor = geometrizedfactor(finalUnits)[0]
    return (q*factor).to(finalUnits)

print(toGeometrized(u.solMass))