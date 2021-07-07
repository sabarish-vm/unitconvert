# Units Convert Package

## Installtion

You can pip install it as, 
	pip install -i https://test.pypi.org/simple/ unitconvert-pkg

## Overview
 
The package contains modules which will convert the desired Physical units given as astropy.units.Quantity object to Natural units. Here, natural units refer to the unit system where ℏ = *k*<sub>*B*</sub> = *c* = *ϵ*<sub>0</sub> = 1. Hopefully in the future, this will be extended to include even custom unit systems.

## Key Modules

There are two key modules **toNaturalunits(q)** ,  **fromNaturalunits(q,des_units)**, and **Naturalunitsfactor(quantity)**

### Example
	from unitconvert.naturalunits import *
	from astropy import units as au 
    
    height = 1*au.m  # In S.I. units
    height_natural = toNaturalunits(height) # In natural units 
    
We can revert back to S.I. units as follows,
    
    height_si = fromNaturalunits(height_natural,au.m) # We convert it back to SI
    height_cgs = fromNaturalunits(height_natural,au.cm) # We convert it to CGS
    
We can use the function Naturalunitsfactor(quantity) to restore the constants in the equation which have been set equal to 1. For example in the equation *E* = *mc*<sup>2</sup>, in natural units will be just *E* = *m*. To restore the constants, just use the function as follows,

	Naturalunitsfactor(u.kg)
	
This returns the output,

	 {'hbar': 0.0, 'c': -2.0, 'k_B': 0, 'eps0': 0.0}
Which says that your quantity *m* has to be divided by *c* <sup>-2</sup>. 
    
    


