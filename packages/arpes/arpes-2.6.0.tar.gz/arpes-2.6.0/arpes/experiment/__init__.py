"""
This module is a work-in-progress. Ideally, we would one day like to offer
a simple graphical utility that can communicate with various ARPES DAQ hardware using
a file based interchange format. Currently, DAQ sequences roughly consistent with the
capabilities of the MAESTRO beamlines are supported via JSON.

More capabiities are also available for Tr-ARPES (shuffling to prevent laser and drift
skewing datasets) with more to come.
"""

import json
from itertools import chain, product
from pathlib import Path
from typing import Any, Iterable, Iterator, Union

import numpy as np

__all__ = ('JSONExperimentDriver', 'linspace', 'shuffled', 'move', 'comment', 'collect')


def flatten(lists):
    return chain.from_iterable([l if np.iterable(l) else [l] for l in lists])


class ExperimentTreeItem:
    def __add__(self, other):
        if isinstance(other, ExperimentTreeItem):
            return [self] + [other]

        return [self] + other

    def __mul__(self, other):
        return Product(self, other)


class Product(ExperimentTreeItem):
    items = None

    def __init__(self, *args):
        self.items = args
        self._iter = None

    def __len__(self):
        return np.product([len(item) for item in self.items])

    def __iter__(self):
        def safeiter(item_or_iterable: Union[Any, Iterable[Any]]) -> Iterator[Any]:
            try:
                return iter(item_or_iterable)
            except TypeError:
                return iter([item_or_iterable])

        self._iter = product(*[safeiter(i) for i in self.items])
        return self

    def __next__(self):
        return next(self._iter)

    def __repr__(self):
        front = '<Product>'
        content = '\n[\n{}\n]\n'.format((', \n'.join(['\t' + repr(f) for f in self.items])))

        back = '</ Product>'

        return front + content + back


class Collect(ExperimentTreeItem):
    def __init__(self, duration, configuration):
        self.duration = duration
        self.configuration = configuration

    def __repr__(self):
        return '<Collect duration={} configuration={} />'.format(self.duration, self.configuration)


class Move(ExperimentTreeItem):
    moveset = None
    wait_after = 0
    measure_while_moving = False
    backlash_compensate = False

    def __init__(self, wait_after=0, measure_while_moving=False, backlash_compensate=False, **kwargs):
        self.moveset = kwargs
        self.wait_after = wait_after
        self.measure_while_moving = measure_while_moving
        self.backlash_compensate = backlash_compensate

    def __repr__(self):
        return '<Move {} wait_after={} measure_while_moving={} backlash_compensate={}/>'.format(
            ' '.join(['{}={}'.format(k, v) for k, v in self.moveset.items()]),
            self.wait_after,
            self.measure_while_moving,
            self.backlash_compensate
        )


class Comment(ExperimentTreeItem):
    comment = ''

    def __init__(self, the_comment):
        self.comment = the_comment


class Shuffled(ExperimentTreeItem):
    values = None

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        front = '<Shuffled>'
        try:
            content = '\n[\n{}\n]\n'.format((', \n'.join([
                '\t' + repr(v) for v in list(flatten(self.values))
            ])))
        except Exception: # pylint: disable=broad-except
            content = repr(self.values)

        back = '</ Shuffled>'
        return front + content + back


class Linspace(ExperimentTreeItem):
    start = 0
    stop = 0
    num = 0
    endpoint = True

    def __init__(self, f, start, stop, num, endpoint=True):
        self.f = f
        self.start = start
        self.stop = stop
        self.num = num
        self.endpoint = endpoint

    def __len__(self):
        return self.num

    def __iter__(self):
        return iter(self.values)

    @property
    def values(self):
        values = np.linspace(self.start, self.stop, self.num)
        return [self.f(v) for v in values]

    def __repr__(self):
        front = '<Linspace {} --> {}, {} steps endpoint={}>'.format(
            self.start, self.stop, self.num, self.endpoint)
        content = '\n[\n{}\n]\n'.format((', \n'.join(['\t' + repr(f) for f in self.values])))
        back = '</ Linspace>'
        return front + content + back

# pylint: disable=invalid-name

linspace = Linspace
shuffled = Shuffled
move = Move
comment = Comment
collect = Collect

# pylint: enable=invalid-name


class ExperimentDriver:
    queue_location = None
    seconds_per_frame = 1

    # units / second
    movement_speed = {
        'temp': 0.03, # deg kelvin per second

        'x': 1, # mm / sec
        'y': 1,
        'z': 1,

        'theta': 1 * np.pi / 180,
        'beta': 1 * np.pi / 180,
        'chi': 1 * np.pi / 180,
        'alpha': 0.1 * np.pi / 180,
        'psi': 100,
    }

    def __init__(self, queue_location=None):
        self.queue_location = queue_location

    @property
    def ext(self):
        return 'drive'

    def dump(self, file, input_object, **kwargs):
        file.write(self.dumps(input_object, **kwargs))

    def dumps(self, input_object, desired_total_time=None):
        return ''

    def dump_to_queue(self, name, input_object, **kwargs):
        if self.queue_location is None:
            raise ValueError('Must supply a queue location.')

        dump_path = Path(self.queue_location) / '{}.{}'.format(name, self.ext)
        with open(str(dump_path), 'w') as f:
            self.dump(f, input_object, **kwargs)

    def calculate_overhead(self, o):
        return self.calculate_duration(o)[1:]

    def calculate_duration(self, o):
        """
        Returns the anticipated scan duration, together with the
        fraction of time spent as movement or idle time overhead,
        the fraction of time spent in overhead in the spectrometer,
        and the fraction of acquisition time wasted due to overhead
        in sweeping (i.e. the DAQ "efficiency")

        I.e., if you received
        [600, 0.1, 0, 0.25]
        this means that the scan will take about 10 minutes, of which
        60 seconds (10%) of the time is spent in movement overhead, and
        no extra time is anticipated to be spent adjusting voltages
        in the spectrometer, and only 75% of the data recorded by
        the spectrometer will be kept.

        :param o:
        :return:
        """
        return [0, 0, 0, 0]


class ExperimentEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, Product):
            return {
                'type': 'product',
                'items': obj.items,
            }
        if isinstance(obj, Linspace):
            return {
                'type': 'linspace',
                'start': obj.start,
                'stop': obj.stop,
                'num': obj.num,
                'endpoint': obj.endpoint,
                'values': obj.values,
            }
        if isinstance(obj, Move):
            return {
                'type': 'move',
                'wait_after': obj.wait_after,
                'measure_while_moving': obj.measure_while_moving,
                'backlash_compensate': obj.backlash_compensate,
                'moveset': obj.moveset
            }
        if isinstance(obj, Collect):
            return {
                'type': 'collect',
                'duration': obj.duration,
                'configuration': obj.configuration,
            }
        return super().default(obj)


class FlatExperimentEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, Product):
            return flatten(iter(obj))
        if isinstance(obj, Linspace):
            return flatten(obj.values)
        if isinstance(obj, Move):
            return {
                'type': 'move',
                'wait_after': obj.wait_after,
                'measure_while_moving': obj.measure_while_moving,
                'backlash_compensate': obj.backlash_compensate,
                'moveset': obj.moveset
            }
        if isinstance(obj, Collect):
            return {
                'type': 'collect',
                'duration': obj.duration,
                'configuration': obj.configuration,
            }
        return super().default(obj)


class JSONExperimentDriver(ExperimentDriver):
    def dumps(self, o, desired_total_time=None):
        initial_pass = json.dumps({'sequence': o, 'configuration': {}}, cls=FlatExperimentEncoder)

        # we do an extra flattening pass here
        dict_values = json.loads(initial_pass)
        dict_values['sequence'] = flatten(dict_values['sequence'])
        return json.dumps(dict_values)
