from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon
from collections import defaultdict
from math import pi as pi


def factorGaussian(q):
    """
    Find the conversion factor that is used to convert the given quantity q to and from CGS Gaussian units and SI units

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done

    Returns :
            **(dictionary)** : the conversion factor in terms of :math:`4\pi\epsilon_0`

    Example :
            >>> from unitconvert.gaussian import factorGaussian
            >>> from astropy import units as u
            >>> factorGaussian(1*u.A)
            {'4 pi eps0' : 0.5 }
    """
    dimdict = getdim(q.si)
    factorlist = {"4 pi eps0": dimdict[u.A] / 2}
    return factorlist


def toGaussian(q):
    """
    Convert the given astropy quantity `q` in SI units to Gaussian units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

    Returns :
            **(astropy quantity)** : the input quantity `q` in gaussian units

    Example :
            >>> from unitconvert.gaussian import toGaussian
            >>> from astropy import units as u
            >>> toGaussian(1*u.A)
            <Quantity 2.99792458e+09 Fr / s>
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
    factor = (4 * pi * acon.eps0) ** (d / 2)
    natqu = q / factor
    try:
        return (
            natqu.to(
                u.kg ** (a + d / 2)
                * u.m ** (b + 3 * d / 2)
                * u.s ** (c - 2 * d)
                * u.K**e
                * u.cd**f
                * u.mol**g
                * u.rad**h
            )
        ).cgs
    except:
        return "Cannot convert"


def fromGaussian(q, finalUnits):
    """
    Convert the given astropy quantity `q` in gaussian units to SI units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

            **finalUnits (astropy quantity)** : the base units to which quantity needs to be converted back.

    Returns :
            **(astropy quantity)** : the input quantity `q` in SI units

    Example :
            >>> from unitconvert.gaussian import fromGaussian
            >>> from astropy import units as u
            >>> fromGaussian(2.99792458e9 * u.Fr / u.s)
            <Quantity 1. A>
    """

    fac = factorGaussian(finalUnits)
    factor = (4 * pi * acon.eps0) ** fac["4 pi eps0"]
    try:
        return (q * factor).to(finalUnits)
    except:
        return "Cannot convert"

