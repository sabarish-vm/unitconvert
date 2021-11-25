from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon
from collections import defaultdict

def factorPlanck(q):
    # [acon.c, acon.hbar, acon.k_B, acon.eps0, acon.G]
    dimdict = getdim(q.si)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {'c':1/2*(a-3*b -5*c + 5*e - 6*d), 'hbar' : 1/2*(a + b +c +e ), 'k_B' : -e ,'eps0' : d/2 , 'G' : 1/2*(-a+b+c-e-d)  }
    return factorlist

def toPlanck(q) :
    q = q.si
    dimdict = getdim(q.si)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    f = dimdict[u.cd]
    g = dimdict[u.mol]
    h = dimdict[u.rad]
    factorlist = {'c':1/2*(a-3*b -5*c + 5*e + 6*d), 'hbar' : 1/2*(a + b +c +e ), 'k_B' : -e ,'eps0' : d/2 , 'G' : 1/2*(-a+b+c-e-d)  }
    factor =  acon.c**(1/2*(a-3*b -5*c + 5*e + 6*d)) * acon.hbar**(1/2*(a + b +c +e )) * acon.k_B**(-e) * acon.eps0**(d/2) * acon.G**(1/2*(-a+b+c-e-d))
    natqu = q/factor
    try :
        return natqu.to(u.cd**f * u.mol**g * u.rad**h)
    except :
        return 'Cannot Convert'

def fromPlanck(q,finalUnits) :
    fac = factorNatural(finalUnits)
    factor = acon.hbar**(fac['hbar']) * acon.c**(fac['c']) * acon.k_B**(fac['k_B']) * acon.eps0**(fac['eps0']) * acon.G**(fac['G'])
    try :
        return (q*factor).to(finalUnits)
    except :
        return 'Cannot convert'
    

