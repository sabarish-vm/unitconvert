![CI](https://github.com/sabarish-vm/unitconvert/actions/workflows/test.yml/badge.svg)
# Installation instructions

## Latest version : (Recommended)
``` Shell
pip install git+https://github.com/sabarish-vm/unitconvert.git 
```
## Old version v=x.y.z : 
After cloning or downloading the desired verion `x.y.z` do the following,  
``` Shell
pip install numpy astropy
```
``` Shell
git checkout old_versions
cd v0.x.y
pip install -e .
```

# Units Convert Package
The package contains modules which will convert the desired units given as astropy.units. Quantity object to physical units like natural units, geometrized units, and cgs gaussian units. Here, natural units refer to the unit system where ℏ = *c* = *k*<sub>*B*</sub> = *ϵ*<sub>0</sub> = 1, geometrized units refer to *c* = *G* = 1, cgs gaussian refers to 4*π*ϵ<sub>0</sub> = 1

## What's new in 1.0.0 ?


# Overview
## Example
### Key Modules in unitconvert.natural 
There are three key modules **toNaturalunits(q)** ,  **fromNaturalunits(q,required_units)**, and **factorNatural(q)**.

	from unitconvert.natural import *
	from astropy import units as au 
    
    height = 1*au.m  # In S.I. units
    height_natural = toNatural(height) # In natural units 
    
We can revert back to S.I. units as follows,
    
    height_si = fromNatural(height_natural,au.m) # We convert it back to SI
    height_cgs = fromNatural(height_natural,au.cm) # We convert it to CGS

We can also find the factor that will the restore the constants which were set to 1 in a given analytic expression. This is illustrated with the example below,

Consider the equation *E* = *m* *c*<sup>-2</sup>, in natural units it becomes *E* = *m*, now to restore the units using the package follow the given recipe, find the factor of each variable in the equation using the function factorNatural(quantity), and divide the same variable with output. i.e. in our example we have for the rhs the quantity mass which has the units kg,

    In : factorNatural(u.kg)
    Out : {'hbar': 0.0, 'c': -2.0, 'k_B': 0, 'eps0': 0.0}

Thus you will divide *m* by *c* <sup>-2</sup>, to get *m* *c* <sup>2</sup>. Similarly for LHS we get,

    In : factorNatural(u.eV)
    Out : {'hbar': 0.0, 'c': 0.0, 'k_B': 0, 'eps0': 0.0}

Here there factor is just 1, thus we get the equation with restored constants as *E* = *m* *c*<sup>2</sup>

## Geometrized, CGS Gaussian, and Planck unit systems 

These unit systems are defined inside unitconvert.geometrized, unitconvert.gaussian, unitconvert.planck and they have similar named modules to that of unitconvert.natural, that is they contain toGeometrized, toGaussian, toPlanck, factorGeometrized, factorGaussian,factorPlanck, fromGeometrized, fromGaussian, fromPlanck. They can be imported as follows, 

    from unitconvert.geometrized import *
    from unitconvert.gaussian import *
    from unitconvert.planck import *

## Custom unit systems support from verision>1.0.0
