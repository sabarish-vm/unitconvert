from unitconvert.custom import create_units, load_units
from astropy import constants as ac
from astropy import units as u
import numpy as np


def test1_2C_1U():
    soc = u.def_unit("soc", ac.c)
    constants = [soc, ac.hbar]
    units = [u.eV]
    name = "test1_2C_0U"
    create_units(
        constants=constants, units=units, name=name, save="local", overwrite="yes"
    )

    to, fr, fac, mat = load_units(name=name, save="local")
    assert np.isclose(to(u.m * u.cd), 5067730.7 * u.cd / u.eV)


def test_0C_2U():
    cc = u.def_unit("_c", ac.c)
    hbar = u.def_unit("_hbar", ac.hbar)
    u.add_enabled_units([cc, hbar])
    constants = []
    units = [cc, hbar, u.eV]
    name = "test_0C_2U"
    create_units(
        constants=constants, units=units, name=name, save="local", overwrite="yes"
    )
    to, fr, fac, mat = load_units(name=name, save="local")
    assert np.isclose(to(u.m * u.K), 5067730.7 * cc * hbar * u.K / u.eV)


def test_1C_1U():
    cc = u.def_unit("_c", ac.c)
    hbar = u.def_unit("_hbar", ac.hbar)
    u.add_enabled_units([cc, hbar])
    constants = [cc]
    units = [hbar, u.eV]
    name = "test_0C_2U"
    create_units(
        constants=constants, units=units, name=name, save="local", overwrite="yes"
    )
    to, fr, fac, mat = load_units(name=name, save="local")
    assert np.isclose(to(u.m * u.A), 5067730.7 * hbar * u.A / u.eV)
