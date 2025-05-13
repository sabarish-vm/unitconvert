from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon
from collections import defaultdict


def factorNatural(q):
    """
    Find the conversion factor that is used to convert the given quantity q to and from Natural units and SI units

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done

    Returns :
            **(dictionary)** : the conversion factor in terms of :math:`c, \hbar, \epsilon_0, k_B`

    Example :
            >>> from unitconvert.natural import factorNatural
            >>> from astropy import units as u
            >>> factorNatural(1*u.m)
            {'hbar': 1.0, 'c': 1.0, 'k_B': 0, 'eps0': 0.0}
    """
    dimdict = getdim(q.si)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {
        "hbar": 1 / 2 * (2 * b + 2 * c - d),
        "c": 1 / 2 * (-4 * a + 2 * b + d),
        "k_B": -e,
        "eps0": d / 2,
    }
    return factorlist


def toNatural(q):
    """
    Convert the given astropy quantity `q` in SI units to Natural units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

    Returns :
            **(astropy quantity)** : the input quantity `q` in natural units

    Example :
            >>> from unitconvert.natural import toNatural
            >>> from astropy import units as u
            >>> toNatural(1*u.m)
            <Quantity 5067730.7161564 1 / eV>
    """
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
    factor = (
        acon.hbar ** (1 / 2 * (2 * b + 2 * c - d))
        * acon.c ** (1 / 2 * (-4 * a + 2 * b + d))
        * acon.k_B ** (-e)
        * acon.eps0 ** (d / 2)
    )
    natqu = q / factor
    massdim = getdim(natqu)[u.kg]
    try:
        return natqu.to(u.eV**massdim * u.cd**f * u.mol**g * u.rad**h)
    except:
        return q


def fromNatural(q, finalUnits):
    """
    Convert the given astropy quantity `q` in natural units to SI units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

            **finalUnits (astropy quantity)** : the base units to which quantity needs to be converted back.

            For instance both `meters` and `seconds` have the same units `eV` in Natural units. Therefore we need to specify the SI unit to which we need to convert it back to.

    Returns :
            **(astropy quantity)** : the input quantity `q` in SI units

    Example :
            >>> from unitconvert.natural import fromNatural
            >>> from astropy import units as u
            >>> fromNatural(5067730.7161564/u.eV,u.m)
            <Quantity 1. m>
    """
    fac = factorNatural(finalUnits)
    factor = (
        acon.hbar ** (fac["hbar"])
        * acon.c ** (fac["c"])
        * acon.k_B ** (fac["k_B"])
        * acon.eps0 ** (fac["eps0"])
    )
    try:
        return (q * factor).to(finalUnits)
    except:
        return "Cannot convert"
