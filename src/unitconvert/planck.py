from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon
from collections import defaultdict

def factorPlanck(q):
    """ 
    Find the conversion factor that is used to convert the given quantity q to and from Planck units and SI units 

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done
    
    Returns :
            **(dictionary)** : the conversion factor in terms of :math:`c, \hbar, \epsilon_0, k_B,G`

    Example :
            >>> from unitconvert.planck import factorPlanck
            >>> from astropy import units as u
            >>> factorPlanck(1*u.m)
            {'c': -1.5, 'hbar': 0.5, 'k_B': 0, 'eps0': 0.0, 'G': 0.5}
    """
    dimdict = getdim(q.si)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {'c':1/2*(a-3*b -5*c + 5*e - 6*d), 'hbar' : 1/2*(a + b +c +e ), 'k_B' : -e ,'eps0' : d/2 , 'G' : 1/2*(-a+b+c-e-d)  }
    return factorlist

def toPlanck(q) :
    """ 
    Convert the given astropy quantity `q` in SI units to Planck units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted
    
    Returns :
            **(astropy quantity)** : the input quantity `q` in Planck units

    Example :
            >>> from unitconvert.planck import toPlanck
            >>> from astropy import units as u
            >>> toPlanck(1*u.m)
            <Quantity 6.18714241e+34>
    """
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
    """ 
    Convert the given astropy quantity `q` in Planck units to SI units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

            **finalUnits (astropy quantity)** : the base units to which quantity needs to be converted back.

            All fundamental quantities are unit less in Planck units. Therefore we need to specify the SI unit to which we need to convert it back to.
    
    Returns :
            **(astropy quantity)** : the input quantity `q` in SI units

    Example :
            >>> from unitconvert.planck import fromPlanck
            >>> from astropy import units as u
            >>> fromPlanck(6.18714241e+34,u.m)
            <Quantity 1. m>
    """
    fac = factorPlanck(finalUnits)
    factor = acon.hbar**(fac['hbar']) * acon.c**(fac['c']) * acon.k_B**(fac['k_B']) * acon.eps0**(fac['eps0']) * acon.G**(fac['G'])
    try :
        return (q*factor).to(finalUnits)
    except :
        return 'Cannot convert'
    

