import logging
import os
import re
import uuid
import warnings
from collections import namedtuple
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd

import arpes.config
from arpes.exceptions import ConfigurationError
from arpes.utilities.string import snake_case
from typing import Any, List, Optional, Union

__all__ = ['clean_xlsx_dataset', 'default_dataset', 'infer_data_path',
           'attach_extra_dataset_columns', 'swap_reference_map',
           'cleaned_dataset_exists', 'modern_clean_xlsx_dataset', 'cleaned_pair_paths',
           'list_files_for_rename', 'rename_files']

_DATASET_EXTENSIONS = {'.xlsx', '.xlx',}

def shorten_left(s, max_length=20):
    if len(s) > max_length:
        return '...' + s[-(max_length - 3):]


def list_files_for_rename(path=None, extensions=None):
    if path is None:
        path = os.getcwd()

    if extensions is None:
        extensions = ['.txt', '.nxs']

    files_list = list((Path(path).glob('*')))
    files_list = [p for p in files_list if p.suffix in extensions]
    return files_list


def rename_files(dry=True, path=None, extensions=None, starting_index=1):
    if path is None:
        path = os.getcwd()

    files = list_files_for_rename(path=path, extensions=extensions)
    for i, file in enumerate(files):
        extra = '_{}'.format(i + starting_index)
        new_file = file.parent / (file.stem + extra + file.suffix)

        short_input = shorten_left(str(file), max_length=20)
        short_output = shorten_left(str(file.parent / (file.stem + extra + file.suffix)),
                                    max_length=20 + len(extra))

        print('{} -> {}'.format(short_input, short_output))
        if not dry:
            os.rename(str(file), str(new_file))


def is_blank(item: Union[float, str]) -> bool:
    if isinstance(item, str):
        return item == '' or item == 'NaN'

    if isinstance(item, float):
        return np.isnan(item)

    if pd.isnull(item):
        return True

    return False


def infer_data_path(file: int, scan_desc: pd.Series, allow_soft_match: bool = False, use_regex: bool = True) -> str:
    if not isinstance(file, str):
        file = str(int(file))

    if 'path' in scan_desc and not is_blank(scan_desc['path']):
        return scan_desc['path']

    from arpes.endstations import resolve_endstation
    endstation_cls = resolve_endstation(retry=True, **scan_desc)
    return endstation_cls.find_first_file(file, scan_desc)


def swap_reference_map(df: pd.DataFrame, old_reference, new_reference):
    """
    Replaces instances of a reference map old_reference in the ref_map column with
    new_reference.
    :param df:
    :return:
    """
    df = df.copy()

    new_ref_id = df.loc[new_reference, ('id',)]

    for id, row in df.iterrows():
        if row.ref_map == old_reference:
            df.loc[id, ('ref_map', 'ref_id',)] = new_reference, new_ref_id

    return df


def default_dataset(workspace: Optional[Any] = None, match: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
    if workspace is not None:
        arpes.config.CONFIG['WORKSPACE'] = workspace

    workspace = arpes.config.CONFIG['WORKSPACE']

    if not workspace:
        raise ConfigurationError('You need to set the WORKSPACE attribute on CONFIG!')

    workspace_name = workspace['name']
    data_dir = os.path.join(arpes.config.DATASET_PATH, workspace_name)

    def is_dataset(filename: str) -> bool:
        if filename.startswith('~$') or filename.startswith('._'):
            # temporary files on Windows
            return False
        rest, ext = os.path.splitext(filename)
        rest, internal_ext = os.path.splitext(rest)

        return ext in _DATASET_EXTENSIONS and internal_ext != '.cleaned'

    candidates = list(filter(is_dataset, os.listdir(data_dir)))
    if match is not None:
        candidates = list(filter(lambda p: match in p, candidates))

    if (len(candidates)) > 1:
        print('Available candidates are:')
        print(candidates)

    assert len(candidates) == 1

    return clean_xlsx_dataset(os.path.join(data_dir, candidates[0]), **kwargs)


def attach_extra_dataset_columns(path, **kwargs):
    from arpes.io import load_dataset
    import arpes.xarray_extensions # pylint: disable=unused-import, redefined-outer-name

    base_filename, extension = os.path.splitext(path)
    if extension not in _DATASET_EXTENSIONS:
        logging.warning('File is not an excel file')
        return None

    if 'cleaned' in base_filename:
        new_filename = base_filename + extension
    else:
        new_filename = base_filename + '.cleaned' + extension
    assert os.path.exists(new_filename)

    ds = pd.read_excel(new_filename, **kwargs)

    ColumnDef = namedtuple('ColumnDef', ['default', 'source'])
    add_columns = {'spectrum_type': ColumnDef('', 'attr'), }

    for column, definition in add_columns.items():
        ds[column] = definition.default

    # Add required columns
    if 'id' not in ds:
        ds['id'] = np.nan

    if 'path' not in ds:
        ds['path'] = ''

    # Cascade blank values
    for index, row in ds.sort_index().iterrows():
        row = row.copy()

        print(row.id)
        try:
            scan = load_dataset(dataset_uuid=row.id, df=ds)
        except ValueError as e:
            logging.warning(str(e))
            logging.warning('Skipping {}! Unable to load scan.'.format(row.id))
            continue
        for column, definition in add_columns.items():
            if definition.source == 'accessor':
                ds.loc[index, (column,)] = getattr(scan.S, column)
            elif definition.source == 'attr':
                ds.loc[index, (column,)] = scan.attrs[column]

    os.remove(new_filename)
    excel_writer = pd.ExcelWriter(new_filename)
    ds.to_excel(excel_writer, index=False)
    excel_writer.save()

    return ds.set_index('file')


def with_inferred_columns(df: pd.DataFrame):
    """
    Attach inferred columns to a data frame representing an ARPES dataset.

    So far the columns attached are the reference map name, and the reference map_id
    :param df:
    :return: pd.DataFrame which is the union of columns in `df` and the columns produced here
    """

    df = df.copy()

    if 'spectrum_type' not in df.columns:
        warnings.warn('You need to have a spectrum_type column. Try using `prepare_raw_files` first.')
        return df

    df['ref_map'] = ''
    df['ref_id'] = ''

    last_map = None
    logging.warning('Assuming sort along index')
    for index, row in df.sort_index().iterrows():

        if last_map is not None:
            df.loc[index, ('ref_map', 'ref_id')] = last_map, df.loc[last_map, ('id',)]

        if row.spectrum_type == 'map':
            last_map = index

    return df


def cleaned_path(path: str) -> str:
    base_filename, extension = os.path.splitext(path)
    if '.cleaned' in base_filename:
        return base_filename + extension
    return base_filename + '.cleaned' + extension


def cleaned_pair_paths(path):
    base_filename, extension = os.path.splitext(path)
    if 'cleaned' in base_filename:
        return base_filename.replace('.cleaned', '') + extension, base_filename + extension

    return base_filename + extension, base_filename + '.cleaned' + extension


def cleaned_dataset_exists(path):
    return os.path.exists(cleaned_path(path))


def safe_read(path: str, **kwargs: Any) -> pd.DataFrame:
    REATTEMPT_LIMIT = 8
    skiprows = kwargs.pop('skiprows', None)

    def read_snake(x: Union[int, str]) -> Union[List[int], List[str]]:
        try:
            return [x, snake_case(x.strip())]
        except:
            try:
                return [x, x.strip()]
            except AttributeError:
                return [x, x]

    if skiprows is not None:
        read = pd.read_excel(path, skiprows=skiprows, **kwargs)

        return read.rename(columns=dict([read_snake(x) for x in list(read.columns)]))

    for skiprows in range(REATTEMPT_LIMIT):
        try:
            read = pd.read_excel(path, skiprows=skiprows, **kwargs)
            read = read.rename(columns=dict([read_snake(x) for x in list(read.columns)]))
            if 'file' in read.columns:
                return read
        except TypeError:
            # sometimes this happens due to what looks like a bug in pandas
            pass

    warnings.warn('You must supply both a `file` and a `location` column in your '
                  'spreadsheet in order to load data.')
    raise ValueError('Did you supply both a `file` and a `location` column in your spreadsheet? '
                     'Could not safely read dataset. Supply a `skiprows` parameter and check '
                     'the validity of your data.')


def modern_clean_xlsx_dataset(path, allow_soft_match=False, with_inferred_cols=True, write=False, **kwargs):
    original_path, cleaned_path_str = cleaned_pair_paths(path)
    original = safe_read(original_path, **kwargs)
    original = original[original.file.notnull()]
    cleaned = pd.DataFrame({'id': [], 'path': [], 'file': [], 'spectrum_type': []})
    if os.path.exists(cleaned_path_str):
        cleaned = safe_read(cleaned_path_str, skiprows=0, **kwargs)
        if 'file' in cleaned.columns:
            cleaned = cleaned[cleaned.file.notnull()]
        else:
            cleaned['file'] = cleaned.index

    joined = original.set_index('file').combine_first(cleaned.set_index('file'))

    last_index = None

    # Cascade blank values
    for index, row in joined.iterrows():
        row = row.copy()

        for key, value in row.iteritems():
            if key == 'path':
                continue

            if key == 'id' and is_blank(row.id):
                joined.loc[index, ('id',)] = str(uuid.uuid1())

            elif last_index is not None and is_blank(value) and not is_blank(joined.loc[last_index, (key,)]):
                joined.loc[index, (key,)] = joined.loc[last_index, (key,)]

        last_index = index

    for index, row in joined.iterrows():
        joined.loc[index, ('path',)] = infer_data_path(index, row, allow_soft_match)



    if write:
        excel_writer = pd.ExcelWriter(cleaned_path_str)
        joined.to_excel(excel_writer, index=False)
        excel_writer.save()

    if with_inferred_cols:
        return with_inferred_columns(joined)

    return joined


def clean_xlsx_dataset(path: str, allow_soft_match: bool = False, write: bool = True, with_inferred_cols: bool = True,
                       warn_on_exists: bool = False, **kwargs: Any) -> pd.DataFrame:
    reload = kwargs.pop('reload', False)
    _, extension = os.path.splitext(path)
    if extension not in _DATASET_EXTENSIONS:
        logging.warning('File is not an excel file')
        return None

    new_filename = cleaned_path(path)
    if os.path.exists(new_filename):
        if reload:
            if warn_on_exists:
                logging.warning('Cleaned dataset already exists! Removing...')

            os.remove(new_filename)
        else:
            if warn_on_exists:
                logging.warning('Cleaned dataset already exists! Reading existing...')
            ds = pd.read_excel(new_filename).set_index('file')
            if with_inferred_cols:
                return with_inferred_columns(ds)
            return ds

    ds = safe_read(path, **kwargs)
    ds.rename(columns=lambda c: c.lower().strip().replace(' ', '_'), inplace=True)

    column_renamings = {
        'photon_energy': 'hv',
        'temp': 'temperature',
        # 't': 'temperature', # This is ambiguous between temperature and delay!
    }
    ds.rename(columns=lambda c: column_renamings.get(c, c), inplace=True)

    ds = ds.loc[ds.index.dropna()]
    if 'path' not in ds.columns:
        ds = ds[pd.notnull(ds['file'])] # drop null files if path not specified
    else:
        try:
            ds = ds[pd.notnull(ds['file']) | pd.notnull('path')]
        except KeyError:
            pass

    last_index = None

    # Add required columns
    if 'id' not in ds:
        ds['id'] = np.nan

    if 'path' not in ds:
        ds['path'] = ''

    # Cascade blank values
    for index, row in ds.sort_index().iterrows():
        row = row.copy()

        for key, value in row.iteritems():
            if key == 'id' and is_blank(row.id):
                ds.loc[index, ('id',)] = str(uuid.uuid1())

            if key == 'path':
                continue

            elif last_index is not None and is_blank(value) and not is_blank(ds.loc[last_index, (key,)]):
                ds.loc[index, (key,)] = ds.loc[last_index, (key,)]

        last_index = index

    for index, row in ds.sort_index().iterrows():
        if is_blank(row['path']):
            ds.loc[index, ('path',)] = infer_data_path(row['file'], row, allow_soft_match)

    ds = ds.loc[:, ~ds.columns.str.contains('^unnamed:_')]

    if write:
        excel_writer = pd.ExcelWriter(new_filename)
        ds.to_excel(excel_writer, index=False)
        excel_writer.save()

    if with_inferred_cols:
        return with_inferred_columns(ds.set_index('file'))

    return ds.set_index('file')


def walk_datasets(skip_cleaned: bool = True, use_workspace: bool = False) -> Iterator[str]:
    root = os.getcwd()

    if use_workspace:
        root = arpes.config.CONFIG['WORKSPACE']['path']

    for path, _, files in os.walk(root):
        excel_files = [f for f in files if '.xlsx' in f or '.xlx' in f]

        for x in excel_files:
            if x[0] == '~':
                continue

            if skip_cleaned and 'cleaned' in os.path.join(path, x):
                continue

            print("├{}".format(x))
            yield os.path.join(path, x)
