from unitconvert.getdimensions import *
import astropy.units as u
import astropy.constants as acon


def factorGeometrized(q):
    """
    Find the conversion factor that is used to convert the given quantity q to and from Geometrized units and SI units

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done

    Returns :
            **(dictionary)** : the conversion factor in terms of :math:`c, G`

    Example :
            >>> from unitconvert.geometrized import factorGeometrized
            >>> from astropy import units as u
            >>> factorGeometrized(1*u.kg)
            {'c': 2, 'G': -1 }
    """
    dimdict = getdim(q.si)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    factorlist = {"c": 2 * a - c, "G": -a}
    return factorlist


def toGeometrized(q):
    """
    Convert the given astropy quantity `q` in SI units to Geometrized units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

    Returns :
            **(astropy quantity)** : the input quantity `q` in geometrized units

    Example :
            >>> from unitconvert.geometrized import toGeometrized
            >>> from astropy import units as u
            >>> toGeometrized(1*u.kg)
            <Quantity 7.42616027e-28 m>
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
    factor = factor = acon.c ** (2 * a - c) * acon.G ** (-a)
    natqu = q / factor
    lendim = getdim(natqu)[u.m]
    try:
        return natqu.to(u.m**lendim * u.A**d * u.K**e * u.cd**f * u.mol**g * u.rad**h)
    except:
        return "Cannot Convert"


def fromGeometrized(q, finalUnits):
    """
    Convert the given astropy quantity `q` in geometrized units to SI units

    Args :
            **q (astropy quantity)** : the quantity which needs to be converted

            **finalUnits (astropy quantity)** : the base units to which quantity needs to be converted back.

            For instance both `meters` and `seconds` have the same units `eV` in Geometrized units. Therefore we need to specify the SI unit to which we need to convert it back to.

    Returns :
            **(astropy quantity)** : the input quantity `q` in SI units

    Example :
            >>> from unitconvert.geometrized import fromGeometrized
            >>> from astropy import units as u
            >>> fromGeometrized(7.42616027e-28*u.m,u.kg)
            <Quantity 1. kg>
    """
    fac = factorGeometrized(finalUnits)
    factor = acon.c ** (fac["c"]) * acon.G ** (fac["G"])
    try:
        return (q * factor).to(finalUnits)
    except:
        return "Cannot convert"
