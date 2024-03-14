# Installation instructions

## Latest version : Pip install from git
It is the easiest method to get it installed.
``` Shell
pip install git+https://github.com/sabarish-vm/unitconvert.git 
```
## Old version v=x.y.z : Pip install from pypi

``` Shell
pip install numpy astropy
pip install -i https://test.pypi.org/simple/ unitconvert-pkg==x.y.z
```

## Old version v=x.y.z : Pip install from git
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

## What's new in 0.2.4 ?
Transform units to any standard unit like cgs, si, astronomical. The desired target set must be specified as a list.

Example :

    >>> from unitconvert.unitsystem import toSystem
    >>> from astropy import units as u
    >>> toSystem(1 * u.pc *u.A,[u.kpc,u.solMass,u.yr])
    <Quantity 0.001 A kpc>

## What's new in 0.2.3 ?
Included units used in the $N$-body code `GADGET-2`.

## Changes from 0.2.2 to 0.2.3

Support for custom unit systems ! The user can specify the set basis units, and conversions from and to this system can be done using the functions `create_units`, and `load_units`

## Changes from 0.2.1 to 0.2.2
Included planck units ! 

## Overview
 
The package contains modules which will convert the desired units given as astropy.units.Quantity object to physical units like natural units, geometrized units, and cgs gaussian units. Here, natural units refer to the unit system where ℏ = *c* = *k*<sub>*B*</sub> = *ϵ*<sub>0</sub> = 1, geometrized units refer to *c* = *G* = 1, cgs gaussian refers to 4*π*ϵ<sub>0</sub> = 1


## Key Modules in unitconvert.natural 

There are three key modules **toNaturalunits(q)** ,  **fromNaturalunits(q,required_units)**, and **factorNatural(q)**.

### Example
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

## Geometrized, CGS Gaussian, and Planck  unit systems 

These unit systems are defined inside unitconvert.geometrized, unitconvert.gaussian, unitconvert.planck and they have similar named modules to that of unitconvert.natural, that is they contain toGeometrized, toGaussian, toPlanck, factorGeometrized, factorGaussian,factorPlanck, fromGeometrized, fromGaussian, fromPlanck. They can be imported as follows, 

    from unitconvert.geometrized import *
    from unitconvert.gaussian import *
    from unitconvert.planck import *

# README for the version 0.2.x 

For README of earlier versions please check the corresponding Package_0.x.y directory

## Changes from 0.1.x to 0.2.x

The previous versions are obselete, and does not have enough functionality and a lot of bugs are fixed in this release. In the near future another major revision to 1.0.0 will be made which will have the option to work with custom unit systems. 

## Changes from 0.2.0 to 0.2.1 

Fixed a small inconsistency with astropy, which led to errors while getting the dimensions of the charge of an electron.

