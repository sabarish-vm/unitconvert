# Units Convert Package

## Overview
 
The package contains modules which will convert the desired Physical units given as astropy.units.Quantity object to Natural units. Here, natural units refer to the unit system where ℏ = *k*<sub>*B*</sub> = *c* = *ϵ*<sub>0</sub> = 1. Hopefully in the future, this will be extended to include even custom unit systems.

## Key Modules

There are two key modules **toNaturalunits(q)** , and **fromNaturalunits(q,des_units)**.

### Example
	from unitconvert.naturalunits import *
	from astropy import units as au 
    
    height = 1*au.m  # In S.I. units
    height_natural = toNaturalunits(height) # In natural units 
    
We can revert back to S.I. units as follows,
    
    height_si = fromNaturalunits(height_natural,au.m) # We convert it back to SI
    height_cgs = fromNaturalunits(height_natural,au.cm) # We convert it to CGS
    
    


