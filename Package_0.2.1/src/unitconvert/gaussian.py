from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon
from collections import defaultdict
from math import pi as pi

def factorGaussian(q):
    dimdict = getdim(1*q)
    factorlist = {'4 pi eps0': dimdict[u.A]/2  }
    return factorlist

def toGaussian(q) :
    dimdict = getdim(1*q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    f = dimdict[u.cd]
    g = dimdict[u.mol]
    h = dimdict[u.rad]
    factor = (4*pi*acon.eps0)**(d/2)
    natqu = q/factor
    try :
        return (natqu.to(u.kg**(a+d/2) * u.m**(b+3*d/2) * u.s**(c-2*d) * u.K**e * u.cd**f *u.mol**g * u.rad**h)).cgs
    except :
        return 'Cannot convert'

def fromGaussian(q,finalUnits) :
    fac = factorGaussian(finalUnits)
    factor = (4*pi*acon.eps0)**fac['4 pi eps0']
    try :
        return (q*factor).to(finalUnits)
    except :
        return 'Cannot convert'