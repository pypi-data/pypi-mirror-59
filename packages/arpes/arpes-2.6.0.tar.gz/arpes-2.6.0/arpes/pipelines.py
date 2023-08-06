"""
Implements some pipelines for basic tasks.
"""

import xarray as xr
from arpes.corrections import (apply_photon_energy_fermi_edge_correction,
                               apply_quadratic_fermi_edge_correction)

from .pipeline import compose, pipeline
from .preparation import dim_normalizer
from .provenance import update_provenance
from .utilities import conversion

__all__ = ['convert_scan_to_kspace', 'convert_scan_to_kspace_no_corr',
           'tr_prep_scan_ammeter', 'tr_prep_scan_simple', 'convert_mc_map_to_kspace_fft_filter',
           'prep_for_d2']

@pipeline()
def correct_e_fermi_hv(arr: xr.DataArray):
    if isinstance(arr, xr.Dataset):
        arr = arr.raw

    if 'hv' not in arr.dims:
        return arr

    return apply_photon_energy_fermi_edge_correction(arr)


@pipeline()
def correct_e_fermi_spectrometer(arr: xr.DataArray):
    if 'phi' not in arr.dims:
        return arr

    return apply_quadratic_fermi_edge_correction(arr)


@pipeline()
@update_provenance('Sum cycle dimension')
def sum_cycles(arr: xr.DataArray):
    if 'cycle' not in arr.dims:
        return arr

    return arr.sum('cycle', keep_attrs=True)


# TODO: implement pipelines better so that arguments are interned correctly
# in the case where a pipeline step has extra arguments

# Pipelines should never include data loading
# Scans are already normalized at this point, they should be whenever they are first
# interned in the netCDF format
convert_scan_to_kspace = compose(
    pipeline('normalize_hv_axis')(dim_normalizer('hv')),
    correct_e_fermi_hv,
    correct_e_fermi_spectrometer,
    pipeline()(conversion.convert_to_kspace),
)

convert_scan_to_kspace_no_corr = compose(
    pipeline('normalize_hv_axis')(dim_normalizer('hv')),
    pipeline()(conversion.convert_to_kspace),
)

prep_for_d2 = compose(
    pipeline('normalize_hv_axis')(dim_normalizer('hv')),
    correct_e_fermi_hv,
    correct_e_fermi_spectrometer,
)

@pipeline()
def fft_clean_mc_map(data: xr.DataArray):
    from arpes.analysis.fft import fft_filter

    beta_filter = [
        {'beta': slice(0.65, 1.)},
        {'beta': slice(-1., -0.65)},
    ]
    return fft_filter(data, beta_filter)


convert_mc_map_to_kspace_fft_filter = compose(
    pipeline('normalize_polar_axis')(dim_normalizer('beta')),
    fft_clean_mc_map,
    pipeline()(conversion.convert_to_kspace),
)

tr_prep_scan_simple = compose(
    pipeline('normalize_cycle_axis')(dim_normalizer('cycle')),
    sum_cycles,
)

tr_prep_scan_ammeter = compose(
    #normalize_from_ammeter,
    sum_cycles,
)
