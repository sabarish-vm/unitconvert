from getdimensions import *
import astropy.units as u
import astropy.constants as acon
from collections import defaultdict

def factorNatural(q):
    dimdict = getdim(1*q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {'hbar':1/2*(2*b + 2*c - d), 'c' : 1/2*(-4*a + 2*b  +d), 'k_B' : -e ,'eps0' : d/2  }
    factor = acon.hbar**(1/2*(2*b + 2*c - d)) * acon.c**(1/2*(-4*a + 2*b  +d)) * acon.k_B**(-e) * acon.eps0**(d/2)
    return factorlist

def toNatural(q) :
    dimdict = getdim(1*q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    f = dimdict[u.cd]
    g = dimdict[u.mol]
    h = dimdict[u.rad]
    factor = acon.hbar**(1/2*(2*b + 2*c - d)) * acon.c**(1/2*(-4*a + 2*b  +d)) * acon.k_B**(-e) * acon.eps0**(d/2)
    natqu = q/factor
    massdim = getdim(natqu)[u.kg]
    try :
        return natqu.to(u.eV**massdim * u.cd**f * u.mol**g * u.rad**h)
    except :
        return q

def fromNatural(q,finalUnits) :
    fac = factorNatural(finalUnits)
    factor = acon.hbar**(fac['hbar']) * acon.c**(fac['c']) * acon.k_B**(fac['k_B']) * acon.eps0**(fac['eps0'])
    try :
        return (q*factor).to(finalUnits)
    except :
        return 'Cannot convert'
    

