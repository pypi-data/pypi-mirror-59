import numpy as np
import xarray as xr

from arpes.provenance import update_provenance
from arpes.utilities.conversion.bounds_calculations import (euler_to_kx, euler_to_ky, euler_to_kz,
                                                            full_angles_to_k)
from arpes.typing import DataType

__all__ = ('convert_coordinates_to_kspace_forward', 'convert_coordinates',)


@update_provenance('Forward convert coordinates')
def convert_coordinates(arr: DataType, collapse_parallel=False, **kwargs):
    def unwrap_coord(c):
        try:
            return c.values
        except (TypeError, AttributeError):
            try:
                return c.item()
            except (TypeError, AttributeError):
                return c

    coord_names = ['phi', 'psi', 'alpha', 'theta', 'beta', 'chi', 'hv']
    raw_coords = {k: unwrap_coord(arr.S.lookup_offset_coord(k)) for k in (coord_names + ['eV'])}
    raw_angles = {k: v for k, v in raw_coords.items() if k not in {'eV', 'hv'}}

    parallel_collapsible = len([k for k in raw_angles.keys() if isinstance(raw_angles[k], np.ndarray)]) > 1

    sort_by = ['eV', 'hv', 'phi', 'psi', 'alpha', 'theta', 'beta', 'chi']
    old_dims = sorted([k for k in arr.dims if k in (coord_names + ['eV'])], key=lambda item: sort_by.index(item))

    will_collapse = parallel_collapsible and collapse_parallel

    def expand_to(cname, c):
        if not isinstance(c, np.ndarray):
            return c

        index_list = [np.newaxis] * len(old_dims)
        index_list[old_dims.index(cname)] = slice(None, None)
        return c[tuple(index_list)]

    # build the full kinetic energy array over relevant dimensions
    kinetic_energy = (expand_to('eV', raw_coords['eV']) +
                      expand_to('hv', raw_coords['hv']) -
                      arr.S.work_function)

    kx, ky, kz = full_angles_to_k(kinetic_energy, inner_potential=arr.S.inner_potential,
                                  **{k: expand_to(k, v) for k, v in raw_angles.items()})

    if will_collapse:
        if np.sum(kx ** 2) > np.sum(ky ** 2):
            sign = kx / np.sqrt(kx ** 2 + 1e-8)
        else:
            sign = ky / np.sqrt(ky ** 2 + 1e-8)

        kp = sign * np.sqrt(kx ** 2 + ky ** 2)
        data_vars = {'kp': (old_dims, np.squeeze(kp)),
                     'kz': (old_dims, np.squeeze(kz))}
    else:
        data_vars = {'kx': (old_dims, np.squeeze(kx)),
                     'ky': (old_dims, np.squeeze(ky)),
                     'kz': (old_dims, np.squeeze(kx)),}

    return xr.Dataset(data_vars, coords=arr.indexes)


@update_provenance('Forward convert coordinates to momentum')
def convert_coordinates_to_kspace_forward(arr: DataType, **kwargs):
    """
    Forward converts all the individual coordinates of the data array
    :param arr:
    :param kwargs:
    :return:
    """

    arr = arr.copy(deep=True)

    skip = {'eV', 'cycle', 'delay', 'T'}
    keep = {'eV', }

    all = {k: v for k, v in arr.indexes.items() if k not in skip}
    kept = {k: v for k, v in arr.indexes.items() if k in keep}

    old_dims = list(all.keys())
    old_dims.sort()

    if not old_dims:
        return None

    dest_coords = {
        ('phi',): ['kp', 'kz'],
        ('theta',): ['kp', 'kz'],
        ('beta',): ['kp', 'kz'],
        ('phi', 'theta',): ['kx', 'ky', 'kz'],
        ('beta', 'phi',): ['kx', 'ky', 'kz'],
        ('hv', 'phi',): ['kx', 'ky', 'kz'],
        ('hv',): ['kp', 'kz'],
        ('beta', 'hv', 'phi',): ['kx', 'ky', 'kz'],
        ('hv', 'phi', 'theta'): ['kx', 'ky', 'kz'],
        ('hv', 'phi', 'psi'): ['kx', 'ky', 'kz'],
        ('chi', 'hv', 'phi',): ['kx', 'ky', 'kz'],
    }.get(tuple(old_dims))

    full_old_dims = old_dims + list(kept.keys())
    projection_vectors = np.ndarray(shape=tuple(len(arr.coords[d]) for d in full_old_dims), dtype=object)

    # these are a little special, depending on the scan type we might not have a phi coordinate
    # that aspect of this is broken for now, but we need not worry
    def broadcast_by_dim_location(data, target_shape, dim_location=None):
        if isinstance(data, xr.DataArray):
            if not data.dims:
                data = data.item()

        if isinstance(data, (int, float,)):
            return np.ones(target_shape) * data

        # else we are dealing with an actual array
        the_slice = [None] * len(target_shape)
        the_slice[dim_location] = slice(None, None, None)

        return np.asarray(data)[the_slice]

    raw_coords = {
        'phi': arr.coords['phi'].values - arr.S.phi_offset,
        'beta': (0 if arr.coords['beta'] is None else arr.coords['beta'].values) - arr.S.beta_offset,
        'theta': (0 if arr.coords['theta'] is None else arr.coords['theta'].values) - arr.S.theta_offset,
        'hv': arr.coords['hv'],
    }

    raw_coords = {k: broadcast_by_dim_location(v, projection_vectors.shape, full_old_dims.index(k) if k in full_old_dims else None)
                  for k, v in raw_coords.items()}

    # fill in the vectors
    binding_energy = broadcast_by_dim_location(arr.coords['eV'] - arr.S.work_function,
                                               projection_vectors.shape, full_old_dims.index('eV') if 'eV' in full_old_dims else None)
    photon_energy = broadcast_by_dim_location(arr.coords['hv'], projection_vectors.shape, full_old_dims.index('hv') if 'hv' in full_old_dims else None)
    kinetic_energy = binding_energy + photon_energy

    inner_potential = arr.S.inner_potential

    # some notes on angle conversion:
    # BL4 conventions
    # angle conventions are standard:
    # phi = analyzer acceptance
    # polar = perpendicular scan angle
    # theta = parallel to analyzer slit rotation angle

    # [ 1  0          0          ]   [  cos(polar) 0 sin(polar) ]   [ 0          ]
    # [ 0  cos(theta) sin(theta) ] * [  0          1 0          ] * [ k sin(phi) ]
    # [ 0 -sin(theta) cos(theta) ]   [ -sin(polar) 0 cos(polar) ]   [ k cos(phi) ]
    #
    # =
    #
    # [ 1  0          0          ]     [ sin(polar) * cos(phi) ]
    # [ 0  cos(theta) sin(theta) ] * k [ sin(phi) ]
    # [ 0 -sin(theta) cos(theta) ]     [ cos(polar) * cos(phi) ]
    #
    # =
    #
    # k ( sin(polar) * cos(phi),
    #     cos(theta)*sin(phi) + cos(polar) * cos(phi) * sin(theta),
    #     -sin(theta) * sin(phi) + cos(theta) * cos(polar) * cos(phi),
    #   )
    #
    # main chamber conventions, with no analyzer rotation (referred to as alpha angle in the Igor code
    # angle conventions are standard:
    # phi = analyzer acceptance
    # polar = perpendicular scan angle
    # theta = parallel to analyzer slit rotation angle

    # [ 1 0 0                    ]     [ sin(phi + theta) ]
    # [ 0 cos(polar) sin(polar)  ] * k [ 0                ]
    # [ 0 -sin(polar) cos(polar) ]     [ cos(phi + theta) ]
    #
    # =
    #
    # k (sin(phi + theta), cos(phi + theta) * sin(polar), cos(phi + theta) cos(polar), )
    #

    # for now we are setting the theta angle to zero, this only has an effect for vertical slit analyzers,
    # and then only when the tilt angle is very large

    # TODO check me
    raw_translated = {
        'kx': euler_to_kx(kinetic_energy, raw_coords['phi'], raw_coords['beta'], theta=0,
                          slit_is_vertical=arr.S.is_slit_vertical),
        'ky': euler_to_ky(kinetic_energy, raw_coords['phi'], raw_coords['beta'], theta=0,
                          slit_is_vertical=arr.S.is_slit_vertical),
        'kz': euler_to_kz(kinetic_energy, raw_coords['phi'], raw_coords['beta'], theta=0,
                          slit_is_vertical=arr.S.is_slit_vertical,
                          inner_potential=inner_potential),
    }

    if 'kp' in dest_coords:
        if np.sum(raw_translated['kx'] ** 2) > np.sum(raw_translated['ky'] ** 2):
            sign = raw_translated['kx'] / np.sqrt(raw_translated['kx'] ** 2 + 1e-8)
        else:
            sign = raw_translated['ky'] / np.sqrt(raw_translated['ky'] ** 2 + 1e-8)

        raw_translated['kp'] = np.sqrt(raw_translated['kx'] ** 2 + raw_translated['ky'] ** 2) * sign

    data_vars = {}
    for dest_coord in dest_coords:
        data_vars[dest_coord] = (full_old_dims, np.squeeze(raw_translated[dest_coord]))

    return xr.Dataset(data_vars, coords=arr.indexes)
