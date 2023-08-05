import numpy as np

from arpes.provenance import update_provenance
from arpes.typing import DataType
from arpes.utilities import normalize_to_spectrum

__all__ = ('remove_incoherent_background',)


@update_provenance('Remove incoherent background from above Fermi level')
def remove_incoherent_background(data: DataType, set_zero=True):
    """
    Sometimes spectra are contaminated by data above the Fermi level for
    various reasons (such as broad core levels from 2nd harmonic light,
    or slow enough electrons in ToF experiments to be counted in subsequent
    pulses).
    :param data:
    :param set_zero:
    :return:
    """
    data = normalize_to_spectrum(data)

    approximate_fermi_energy_level = data.S.find_spectrum_energy_edges().max()

    background = data.sel(eV=slice(approximate_fermi_energy_level + 0.1, None))
    density = background.sum('eV') / (np.logical_not(np.isnan(background)) * 1).sum('eV')
    new = data - density
    if set_zero:
        new.values[new.values < 0] = 0

    return new
