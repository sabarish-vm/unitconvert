from unitconvert.getdimensions import getdim
import astropy.units as u

gM = u.def_unit('gM',1.989e43*u.g)
gL = u.def_unit('gL',3.085678e21*u.cm)
gV = u.def_unit('gV',1e5*u.cm/u.s)
gT = u.def_unit('gT',3.085678e16*u.s)

def toGadget(q):
    """ 
    Find the conversion factor that is used to convert the given quantity q to and from units used in the :math:`N`-body code ``GAGDGET-2`` and SI units 

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done
    
    Returns :
            **(astropy quantity)** : the input quantity `q` in gadget units             

    Example :
            >>> from unitconvert.natural import toGadget
            >>> from astropy import units as u
            >>> toGadget(1*u.pc)
            <Quantity 0.001 gL>
    """
    q=1*q
    dimdict=getdim(q=q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    f = dimdict[u.cd]
    g = dimdict[u.mol]
    h = dimdict[u.rad]
    return q.to(gM**a * gL**b * gT**c * u.A**d * u.K**e * u.cd**f * u.mol**g * u.rad**h)

def fromGadget(q,finalUnits=None):
    """ 
    Find the conversion factor that is used to convert the given quantity q given in units of :math:`N`-body code ``GAGDGET-2`` to SI units 

    Args :
            **q (astropy quantity)** : the quantity for which unit conversion must be done
            **finalUnits** : optional argument to specify the units to which `q` must be converted. Defaults to standard astronomical units [kpc, solMass, Gyr] if not specified.
    
    Returns :
            **(astropy quantity)** : the input quantity `q` in astronomical units or specified units.             

    Example :
            >>> from unitconvert.natural import toGadget
            >>> from astropy import units as u
            >>> toGadget(0.001*gL)
            <Quantity 0.001 kpc>
    """
    q=1*q
    dimdict=getdim(q=q)
    a = dimdict[u.kg]
    b = dimdict[u.m]
    c = dimdict[u.s]
    d = dimdict[u.A]
    e = dimdict[u.K]
    f = dimdict[u.cd]
    g = dimdict[u.mol]
    h = dimdict[u.rad]
    if finalUnits is None :
        return q.to(u.solMass**a * u.kpc**b * u.Gyr**c * u.A**d * u.K**e * u.cd**f * u.mol**g * u.rad**h )
    elif finalUnits is not None :
        return q.to(finalUnits)