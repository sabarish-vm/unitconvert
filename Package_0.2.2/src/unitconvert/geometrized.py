from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon


def factorGeometrized(q):
    dimdict = getdim(q.si)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = { 'c' : 2*a - c , 'G' : -a }
    return factorlist

def toGeometrized(q) :
    q = q.si
    dimdict = getdim(q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    f = dimdict[u.cd]
    g = dimdict[u.mol]
    h = dimdict[u.rad]
    factor = factor = acon.c**(2*a - c) * acon.G**(-a)
    natqu = q/factor
    lendim = getdim(natqu)[u.m]
    try :
        return natqu.to(u.m**lendim * u.A**d * u.K**e * u.cd**f * u.mol**g * u.rad**h )
    except :
        return 'Cannot Convert'

def fromGeometrized(q,finalUnits) :
    fac = factorGeometrized(finalUnits)
    factor = acon.c**(fac['c']) * acon.G**(fac['G'])
    try :
        return (q*factor).to(finalUnits)
    except :
        return 'Cannot convert'