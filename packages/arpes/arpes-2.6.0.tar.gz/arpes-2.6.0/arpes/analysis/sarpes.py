import xarray as xr
from arpes.analysis import savitzky_golay
from arpes.provenance import update_provenance
from arpes.typing import DataType
from arpes.utilities import normalize_to_dataset
from arpes.utilities.math import polarization

__all__ = ('to_intensity_polarization', 'to_up_down', 'normalize_sarpes_photocurrent', 'sarpes_smooth')


@update_provenance('Smooth SARPES data')
def sarpes_smooth(data: xr.Dataset, *args, **kwargs):
    """
    Smooths the up and down channels.
    :param data:
    :param args:
    :param kwargs:
    :return:
    """
    up = savitzky_golay(data.up, *args, **kwargs)
    down = savitzky_golay(data.down, *args, **kwargs)
    return data.copy(deep=True).assign(up=up, down=down)


@update_provenance('Normalize SARPES by photocurrent')
def normalize_sarpes_photocurrent(data: DataType):
    """
    Normalizes the down channel so that it matches the up channel in terms of mean photocurrent. Destroys the integrity
    of "count" data.

    :param data:
    :return:
    """

    copied = data.copy(deep=True)
    copied.down.values = (copied.down * (copied.photocurrent_up / copied.photocurrent_down)).values
    return copied


@update_provenance('Convert polarization data to up-down spin channels')
def to_up_down(data: DataType):
    """
    Converts from [intensity, polarization] representation to [up, down] representation.
    :param data:
    :return:
    """
    assert('intensity' in data.data_vars and 'polarization' in data.data_vars)

    return xr.Dataset({
        'up': data.intensity * (1 + data.polarization),
        'down': data.intensity * (1 - data.polarization),
    })


@update_provenance('Convert up-down spin channels to polarization')
def to_intensity_polarization(data: DataType):
    """
    Converts from [up, down] representation (the spin projection) to
    [intensity, polarization] representation.

    In this future, we should also make this also work with the timing signals.
    :param data:
    :return:
    """
    data = normalize_to_dataset(data)

    assert('up' in data.data_vars and 'down' in data.data_vars)

    intensity = data.up + data.down
    spectrum_polarization = polarization(data.up, data.down)

    return xr.Dataset({
        'intensity': intensity,
        'polarization': spectrum_polarization / data.S.sherman_function
    })
