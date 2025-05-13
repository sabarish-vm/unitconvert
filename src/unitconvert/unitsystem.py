from unitconvert.getdimensions import getdim
import astropy.units as u


def toSystem(q, target):
    """
    Convert any quantity to any standard set of units.
    Standard refers to set of units whose individual dimensions are similar to that of SI.

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done
            **system (list)** : a list of astropy quantities that serve as the target unit system

    Returns :
            **(astropy quantity)** : the input quantity `q` in target units

    Example :
            >>> from unitconvert.unitsystem import toSystem
            >>> from astropy import units as u
            >>> toSystem(1*u.pc*u.A,[u.kpc,u.solMass,u.yr])
            <Quantity 0.001 A kpc>
    """
    q = 1 * q

    q = 1.0 * q
    qSI = {(1 * uniT).si.unit: uniT for uniT in q.unit.bases}
    targetSI = {(1 * uniT).si.unit: uniT for uniT in target}

    q = q.si
    dimdict = getdim(q)
    m = dimdict[u.kg]
    l = dimdict[u.m]
    t = dimdict[u.s]
    i = dimdict[u.A]
    theta = dimdict[u.K]
    j = dimdict[u.cd]
    n = dimdict[u.mol]
    ang = dimdict[u.rad]

    uM = targetSI.get(u.kg, qSI.get(u.kg, u.kg))
    uL = targetSI.get(u.m, qSI.get(u.m, u.m))
    uT = targetSI.get(u.s, qSI.get(u.s, u.s))
    uI = targetSI.get(u.A, qSI.get(u.A, u.A))
    uTheta = targetSI.get(u.K, qSI.get(u.K, u.K))
    uN = targetSI.get(u.mol, qSI.get(u.mol, u.mol))
    uJ = targetSI.get(u.cd, qSI.get(u.cd, u.cd))
    uAng = targetSI.get(u.rad, qSI.get(u.rad, u.rad))

    returnUnits = (
        uM**m * uL**l * uT**t * uI**i * uTheta**theta * uJ**j * uN**n * uAng**ang
    )

    return q.to(returnUnits)
