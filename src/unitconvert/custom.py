import astropy.units as u
import astropy.constants as acon
from unitconvert.getdimensions import getdim
import numpy as np

def create_units(constants, units, name , save = 'global' ,overwrite = 'no', labels = []) :
    '''
    Creates a new unit system and saves them in current working directory or inside a global directory. This saved system can be accessed later. The target custom unit system has two parts. 
    1) List of constants or units that needs to be set to 1
    2) List of Remaining units

    Args :
            **constants (list)** : A list of astropy constants / astropy units that is a part of the custom unit that needs to be set to 1.

            **units (list)** : A list of astropy units corresponding to the remanining units.

            **name (str)** The name of the unit system
        
            **save (str)** :  `'local'` to save the unit system in the current working directory `'global'` to save it in a global directory in the home of the user

            **overwrite (str)** : `'yes'` to overwrite the existing unit system with a given name if it exists `'no'` to not to overwrite the existing unit system
    
            **labels (list)** : A list of strings corresponding to each physical constant that serves as a symbol for that constant. It is useful when one uses not the inbuilt astropy constants but defines ones own constants.  
    
    Returns :
            None         
    '''
    from sympy import symbols as symbols
    from collections import defaultdict
    from os.path import expanduser as userpath
    from os import getcwd,mkdir
    from os.path import join as joinpath
    from os.path import exists as isthere
    from sympy.solvers.solveset import linsolve

    ## Check for existence of directories for saving unitsystems
    if save == 'global' :
        path = joinpath(userpath('~'),'.unitconvert')
        if isthere(path) == False :
            mkdir(path)
    elif save == 'local' :
        path = getcwd()
    else :
        path = getcwd()
        print('saving to current working directory')

    ## Check for pre-existence of already saved unitsystems
    if overwrite != 'yes' and isthere(joinpath(path,'.unit_'+name+'.dat')) == True :
        print('Unit system system already exists ! \nPlease use a different name or set the overwrite option to yes. i.e. create_units(...., overwrite = \'yes\')')
        return 

    si = {0 : u.kg , 1:  u.m , 2: u.s, 3 :u.Kelvin, 4 : u.A,5 : u.mol, 6: u.cd, 7: u.rad}
    targetunits = constants + units
    unused = checksystem(targetunits,want_details=True)['SI-unrelated']
    units +=  unused
    targetunits += unused

    if len(targetunits) != 8 :
        print('There is an inconsistency in the given set of constants, and units.  Please check !')
    else :
        # This generates a dictionary that has the dimensions of the constants + units of the new unit system
        rhsdict = defaultdict(lambda: 0)
        for i in range(len(targetunits)):
            rhsdict[i] = getdim(targetunits[i])
            
        def findtotal(t) :
            total = 0
            for i in range(len(targetunits)) :
                total = total + eval('r'+str(i+1))* rhsdict[i][t]
            return total

        # Generating the variables r1, r2, r3... and e1,e2,e3... which are the exponents of the constants on RHS
        for i in range(len(targetunits)) :
            globals()['r'+str(i+1)] = symbols('r'+str(i+1))
            
        for j in range(len(si)) :
            globals()['e'+str(j+1)] = findtotal(si[j])

        # Generating the variables l1, l2, l3... which are the exponents of the constants on LHS
        for i in range(len(targetunits)) :
            globals()['l'+str(i+1)] = symbols('l'+str(i+1))

        equations = [e1 - l1 , e2 - l2 , e3 - l3 , e4 - l4 , e5 - l5 , e6 - l6 , e7 - l7 , e8 - l8]
        sol = linsolve(equations,(r1,r2,r3,r4,r5,r6,r7,r8))
        solns = eval(str(sol.args[0]))
        solncons = solns[0:(len(constants))]
        solnunits = solns[len(constants) :] 
        temp = []
        for i in constants :
            try :
                temp.append(i.abbrev)
            except AttributeError :
                temp.append((i.value,i.unit.to_string()))
        
        temp2 = []
        for i in units :
            try :
                temp2.append(i.abbrev)
            except AttributeError :
                temp2.append(i.to_string())

        if labels == [] :
            for i in constants :
                try :
                    labels.append(i.abbrev)
                except AttributeError :
                    labels.append(i.unit)


        with open(joinpath(path,'.unit_'+name+'.dat'),'w') as f :
            f.write('#constants \n')
            f.write(str(temp) + '\n')
            f.write('#units \n')
            f.write(str(temp2) + '\n')
            f.write('#solution for constants \n')
            f.write(str(solncons) + '\n')
            f.write('#solution for rest of units \n')
            f.write(str(solnunits) + '\n')
            f.write('#symbols for constants \n')
            f.write(str(labels))

def load_units(name, save = 'global'):
    '''
    Loading saved unit system

    Args :
            **name (str)** : The name of the unit system that has to be loaded
            
            **save (str)** : `'local'` : to load the unit system saved in the current working directory `'global'` : to load the unit system saved in the global directory (home directory of the user)

    Returns :
        The function returns three functions with three functionalities

        **1)** function that converts from SI to the New unit system

        **2)** function that converts from the New unit system to SI

        **3)** function to returns the conversion factor
    '''
    from sympy import symbols as symbols
    from collections import defaultdict
    from os.path import expanduser as userpath
    from os import getcwd,mkdir
    from os.path import join as joinpath
    from os.path import exists as isthere

    if save == 'global' :
        path = joinpath(userpath('~'),'.unitconvert')
        if isthere(joinpath(path,'.unit_'+name+'.dat')) == False :
            print('Unit system not found in the global directory!')
            return 
    else :
        path = getcwd()
        if isthere(joinpath(path,'.unit_'+name+'.dat')) == False :
            print('Unit system not found in the current working directory!')
            return

        # Generating the variables l1, l2, l3... which are the exponents of the constants on LHS
    for i in range(8) :
        globals()['l'+str(i+1)] = symbols('l'+str(i+1))

    with open(joinpath(path,'.unit_'+name+'.dat'),'r') as f :
        lines = f.readlines()
        t_cons = eval(lines[1])
        #print(t_cons);print('\n')
        constants = [] 
        units = []
        for item in t_cons :
            if type(item) == str :
                constants.append(eval('acon.'+ item))
            elif type(item) != str :
                value = float(item[0])
                unit_temp = item[1]
                constants.append(u.Quantity(unit=unit_temp,value=value))
        t_units = eval(lines[3])
        for item in t_units :
            if type(item) == str :
                units.append(u.Quantity(value=1,unit=item))
            elif type(item) != str :
                value = float(item[0])
                unit_temp = item[1]
                units.append(u.Quantity(unit=unit_temp,value=value))

        solncons  = eval(lines[5]) 
        solnunits = eval(lines[7])
        labels = eval(lines[9])
    targetunits = constants + units
    # Generating the variables l1, l2, l3... which are the exponents of the constants on LHS
    for i in range(len(targetunits)) :
        globals()['l'+str(i+1)] = symbols('l'+str(i+1))       

    #return constants,units,solncons,solnunits
    def convfactor(q):
        dimdict = getdim(q.si)
        a1 = dimdict[u.kg]
        a2 = dimdict[u.m]
        a3 = dimdict[u.s]
        a4 = dimdict[u.K]
        a5 = dimdict[u.A]
        a6 = dimdict[u.mol]
        a7 = dimdict[u.cd]
        a8 = dimdict[u.rad]
        factor = 1
        returnunits = 1
        for i in range(len(constants)):
            factor = factor * constants[i]**float(solncons[i].subs(l1,a1).subs(l2,a2).subs(l3,a3).subs(l4,a4).subs(l5,a5).subs(l6,a6).subs(l7,a7).subs(l8,a8))
        for i in range(len(units)):
            returnunits = returnunits * units[i]**float(solnunits[i].subs(l1,a1).subs(l2,a2).subs(l3,a3).subs(l4,a4).subs(l5,a5).subs(l6,a6).subs(l7,a7).subs(l8,a8))
        return factor, returnunits
       
    def convert(q):
        '''
        SI to Whatever-Units system : Function that converts SI astropy quantities to new units

        Parameters :
        ------------

        q : astropy.quantitiy
            The instance of the class astropy quantity that needs to be converted 
        '''
        q = (q*u.dimensionless_unscaled).si
        f,r = convfactor(q)
        return (q/f).to(r)

    def convertback(q,finalunits):
        '''
        Whatever-Units to SI : Function that converts astropy quantities in new units back to SI

        Parameters :
        ------------

        q : astropy.quantitiy
            The instance of the class astropy quantity that needs to be converted 
        finalunits : astropy.quantity
                     The final units as astropy quantities to which we need to convert back to
        '''
        q = (q*u.dimensionless_unscaled).si
        f,r = convfactor(finalunits)
        return (q*f).to(finalunits)

    def getfactor(q):
        '''
        Get the conversion factor

        Parameters :
        ------------

        q : astropy.quantitiy
            The instance of the class astropy quantity for which the conversion factor to the new units is required
        '''

        dimdict = getdim(q.si)
        a1 = -dimdict[u.kg]
        a2 = -dimdict[u.m]
        a3 = -dimdict[u.s]
        a4 = -dimdict[u.K]
        a5 = -dimdict[u.A]
        a6 = -dimdict[u.mol]
        a7 = -dimdict[u.cd]
        a8 = -dimdict[u.rad]
        factor = 1
        returnunits = 1
        factorlist = dict()
        for i in range(len(constants)):
            factorlist[labels[i]] = float(solncons[i].subs(l1,a1).subs(l2,a2).subs(l3,a3).subs(l4,a4).subs(l5,a5).subs(l6,a6).subs(l7,a7).subs(l8,a8))
        return factorlist

    return convert,convertback,getfactor

def checksystem(ls,want_details=False):
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

    si = [u.s, u.m, u.kg, u.A, u.K, u.cd, u.mol, u.rad]

    userUnits = ls
    userUnits = [1*i for i in userUnits]

    u2si = {i: getdim(i) for i in userUnits}

    uDep = {j for i in userUnits for j in getdim(i).keys()}
    uDep = [i for i in si if i in uDep]

    unUsedSubSpace = [i for i in si if i not in uDep]


    assert len(uDep) == len(userUnits), f'\nTo replace standard units \
with the ones given,the dimensions should match. That is, n units from the \
custom-unit system can replace exactly n replaceable-units from the standard \
unit system.\nNumber[Custom-units]={len(userUnits)}, \
\nNumber[replaceable-units]={len(uDep)},\
\nCustom-units = {userUnits}, \nReplaceable-units = {uDep}\nThe easiest \
solution is to add one of the replaceable units to the custom-units.\n'
    dimSpace2 = len(unUsedSubSpace)
    dimSpace1 = len(uDep)
    mat1 = np.matrix([[u2si[j][i]*1.0 for j in userUnits] for i in uDep])
    mat2 = np.matrix(np.identity(len(unUsedSubSpace)))
    mat = np.block([
        [mat1, np.zeros((dimSpace1, dimSpace2))],
        [np.zeros((dimSpace2, dimSpace1)), mat2]
    ])

    try:
        mat.I
        print("Custom-unit system looks good ! :) ")
    except np.linalg.LinAlgError:
        raise Exception("The unit system transformation matrix is singular \
=> Degenerate units are given in custom-units ")
    if want_details :
        return {'Custom-units':userUnits,'SI-related':uDep,
        'SI-unrelated':unUsedSubSpace}
