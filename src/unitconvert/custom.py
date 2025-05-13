import astropy.units as u
import astropy.constants as acon
from unitconvert.getdimensions import getdim
import numpy as np
import math
from unitconvert.defaults import si


def create_units(constants, units, name, save="global", overwrite="no", labels=[]):
    """
    Creates a new unit system and saves them in current working directory or inside a global directory.
    This saved system can be accessed later. The target custom unit system has two parts.
    1) List of constants or units that needs to be set to 1
    2) List of Remaining units

    Args :
            **constants (list)** : A list of astropy constants / astropy units that is a part of the custom unit that needs to be set to 1.

            **units (list)** : A list of astropy units corresponding to the remanining units.

            **name (str)** The name of the unit system

            **save (str)** :  `'local'` to save the unit system in the current working directory `'global'` to save it in a global directory in the home of the user

            **overwrite (str)** : `'yes'` to overwrite the existing unit system with a given name if it exists `'no'` to not to overwrite the existing unit system

            **labels (list)** : A list of strings corresponding to each physical constant that serves as
            a symbol for that constant. It is useful when one uses not the inbuilt astropy constants but
            defines ones own constants.

    Returns :
            None
    """
    from os.path import expanduser as userpath
    from os import getcwd, mkdir
    from os.path import join as joinpath
    from os.path import exists as isthere

    ## Check for existence of directories for saving unitsystems
    if save == "global":
        path = joinpath(userpath("~"), ".unitconvert")
        if isthere(path) is False:
            mkdir(path)
    elif save == "local":
        path = getcwd()
    else:
        path = getcwd()
        print("saving to current working directory")

    ## Check for pre-existence of already saved unitsystems
    if overwrite != "yes" and isthere(joinpath(path, ".unit_" + name + ".dat")) is True:
        print(
            "Unit system system already exists ! \nPlease use a different name or set the overwrite option to yes. i.e. create_units(...., overwrite = 'yes')"
        )
        return

    targetunits = constants + units
    unitsysdetails = checksystem(targetunits)
    unused = unitsysdetails["SI-unrelated"]
    units_all = units + unused
    targetunits += unused
    si_basis = unitsysdetails["SI-related"] + unitsysdetails["SI-unrelated"]

    if len(targetunits) != 8:
        print(
            "There is an inconsistency in the given set of constants, and units.  Please check !"
        )

    else:
        temp = []
        for i in constants:
            try:  # inbuilt abbrev for the constant
                temp.append(i.abbrev)
            except AttributeError:  # random composite quantity
                try:
                    temp.append((i.value, i.unit.to_string()))
                except AttributeError:  # astropy def.quantity
                    temp.append(((1 * i).si.value, (1 * i).si.unit.to_string()))

        temp2 = []
        for i in units_all:
            try:
                temp2.append(i.to_string())
            except AttributeError:
                temp2.append(i.to_string())
        temp3 = []
        for i in si_basis:
            try:
                temp3.append(i.abbrev)
            except AttributeError:
                temp3.append(i.to_string())

        if labels == []:
            for i in constants:
                try:
                    labels.append(i.abbrev)
                except AttributeError:
                    labels.append(i.to_string())

        with open(joinpath(path, ".unit_" + name + ".dat"), "w") as f:
            f.write("#constants \n")
            f.write(str(temp) + "\n")
            f.write("#units \n")
            f.write(str(temp2) + "\n")
            f.write("#symbols for constants \n")
            f.write(str(labels) + "\n")
            f.write("#si-basis \n")
            f.write(str(temp3) + "\n")

        np.savetxt(
            joinpath(path, ".unit" + name + ".mat"), unitsysdetails["Matrix-U_SI"]
        )


def load_units(name, save="global"):
    """
    Loading saved unit system

    Args :
            **name (str)** : The name of the unit system that has to be loaded

            **save (str)** : `'local'` : to load the unit system saved in the current working directory `'global'` : to load the unit system saved in the global directory (home directory of the user)

    Returns :
        The function returns three functions with three functionalities

        **1)** function that converts from SI to the New unit system

        **2)** function that converts from the New unit system to SI

        **3)** function to returns the conversion factor
    """
    from os.path import expanduser as userpath
    from os import getcwd
    from os.path import join as joinpath
    from os.path import exists as isthere

    if save == "global":
        path = joinpath(userpath("~"), ".unitconvert")
        if isthere(joinpath(path, ".unit_" + name + ".dat")) is False:
            print("Unit system not found in the global directory!")
            return
    else:
        path = getcwd()
        if isthere(joinpath(path, ".unit_" + name + ".dat")) is False:
            print("Unit system not found in the current working directory!")
            return

    with open(joinpath(path, ".unit_" + name + ".dat"), "r") as f:
        lines = f.readlines()
        t_cons = eval(lines[1])
        constants = []
        units = []
        si_basis = []
        for item in t_cons:
            if type(item) is str:
                constants.append(eval("acon." + item))
            elif type(item) is not str:
                value = float(item[0])
                unit_temp = item[1]
                constants.append(u.Quantity(unit=unit_temp, value=value))
        t_units = eval(lines[3])
        for item in t_units:
            if type(item) is str:
                units.append(u.Quantity(value=1, unit=item))
            elif type(item) is not str:
                value = float(item[0])
                unit_temp = item[1]
                units.append(u.Quantity(unit=unit_temp, value=value))
        t_units = eval(lines[7])
        for item in t_units:
            if type(item) is str:
                si_basis.append(u.Unit(item))
            elif type(item) is not str:
                value = float(item[0])
                unit_temp = item[1]
                si_basis.append(u.Quantity(unit=unit_temp, value=value))
    mat_u_si = np.genfromtxt(joinpath(path, ".unit" + name + ".mat"))

    targetunits = constants + units

    # return constants,units,solncons,solnunits
    def convfactor(q):
        dimdict = getdim(q)
        si_powers = np.array([dimdict[i] for i in si_basis])
        cu_powers = np.einsum("ij,j->i", mat_u_si, si_powers)
        lc = len(constants)
        con_powers = cu_powers[:lc]
        unit_powers = cu_powers[lc:]
        _tC = math.prod([j ** (con_powers[i]) for i, j in enumerate(constants)])
        _tU = math.prod([j ** (unit_powers[i]) for i, j in enumerate(units)])
        factor = (_tC * _tU).si
        returnunits = _tU
        return factor, returnunits, si_powers, cu_powers

    def convert(q):
        """
        SI to Whatever-Units system : Function that converts SI astropy quantities to new units

        Parameters :
        ------------

        q : astropy.quantitiy
            The instance of the class astropy quantity that needs to be converted
        """
        q = (1 * q * u.dimensionless_unscaled).si
        f, r, _, _ = convfactor(q)
        return (q / f) * r

    def convertback(q, finalunits):
        """
        Whatever-Units to SI : Function that converts astropy quantities in new units back to SI

        Parameters :
        ------------

        q : astropy.quantitiy
            The instance of the class astropy quantity that needs to be converted
        finalunits : astropy.quantity
                     The final units as astropy quantities to which we need to convert back to
        """
        q = (q * u.dimensionless_unscaled).si
        f, r, _, _ = convfactor(finalunits)
        return (q * f / r).to(finalunits)

    def getfactor(q):
        """
        Get the conversion factor

        Parameters :
        ------------

        q : astropy.quantitiy
            The instance of the class astropy quantity for which the conversion factor to the new units is required
        """

        factor = 1
        returnunits = 1
        _, _, sip, cup = convfactor(q)
        factorlist = {
            targetunits[id].unit.to_string(): cup[id] for id in range(len(targetunits))
        }
        return factorlist

    return convert, convertback, getfactor, mat_u_si


def checksystem(ls):
    """
    Check if the user defined unit system can be transformed to and from SI units.

    Args :
        **ls (list)** : a list of astropy quantities belonging to the custom unit system

        **want_details (boolean)** : if `True` returns details about the passed custom-unit system

    Returns :
        None : default
        details (dictionary) : if `want_details` is set to `True`, inferred details about the passed custom-unit system


    Example :
        >>> from unitconvert.unitsystem import checksystem
        >>> from astropy import units as u
        >>> from astropy import constants as c
        >>> checksystem([c.c]) # c.c = speed of light
        <Error message>
        >>> checksystem([c.c,u.m])
        Custom-unit system looks good ! :)
    """

    userUnits = ls
    userUnits = [1 * i for i in userUnits]

    u2si = {i: getdim(i) for i in userUnits}

    uDep0 = {j for i in userUnits for j in getdim(i).keys()}
    uDep = [i for i in si if i in uDep0]

    unUsedSubSpace = [i for i in si if i not in uDep]

    assert len(uDep) == len(userUnits), (
        f"\nTo replace standard units \
with the ones given,the dimensions should match. That is, n units from the \
custom-unit system can replace exactly n replaceable-units from the standard \
unit system.\nNumber[Custom-units]={len(userUnits)}, \
\nNumber[replaceable-units]={len(uDep)},\
\nCustom-units = {userUnits}, \nReplaceable-units = {uDep}\nThe easiest \
solution is to add one of the replaceable units to the custom-units.\n"
    )
    dimSpace2 = len(unUsedSubSpace)
    dimSpace1 = len(uDep)
    mat1 = np.array([[u2si[j][i] * 1.0 for j in userUnits] for i in uDep])
    mat2 = np.array(np.identity(len(unUsedSubSpace)))
    mat = np.block(
        [
            [mat1, np.zeros((dimSpace1, dimSpace2))],
            [np.zeros((dimSpace2, dimSpace1)), mat2],
        ]
    )

    try:
        matInv = np.linalg.inv(mat)
        print("Custom-unit system looks good ! :) ")
    except np.linalg.LinAlgError:
        raise Exception(
            "The unit system transformation matrix is singular \
=> Degenerate units are given in custom-units "
        )
    return {
        "Matrix-SI_U": mat,
        "Matrix-U_SI": matInv,
        "Custom-units": userUnits,
        "SI-related": uDep,
        "SI-unrelated": unUsedSubSpace,
    }
