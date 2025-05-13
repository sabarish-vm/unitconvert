import astropy.units as u
import unitconvert.natural as nat
import unitconvert.planck as pl
import unitconvert.gaussian as gau
import unitconvert.geometrized as geo
import astropy.constants as c
import numpy as np


def test_nat():
    res = nat.toNatural(c.e)
    assert np.isclose(0.30282212, res, rtol=1e-6)
    res = nat.toNatural(u.m * u.cd)
    assert np.isclose(5067730.71615 * u.cd / u.eV, res, rtol=1e-6)


def test_geo():
    res = geo.toGeometrized(u.solMass)
    assert np.isclose(1476.62503805 * u.m, res, rtol=1e-6)
    res = geo.toGeometrized(1 * u.m * u.cd)
    assert np.isclose(1.0 * u.m * u.cd, res, rtol=1e-6)


def test_gau():
    assert np.isclose(gau.toGaussian(2.99792458e2 * u.V), 1 * u.erg / u.statC)
    res = geo.toGeometrized(1.0 * u.m * u.cd)
    assert np.isclose(1.0 * u.m * u.cd, res, rtol=1e-6)


def test_planck():
    assert np.isclose(pl.toPlanck(u.m) ** -1, 1.616255e-35, rtol=1e-6)
