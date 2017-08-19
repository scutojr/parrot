import copy
from functools import partial

from parrot.executor.base import LocalShellExecutor


__all__ = [
    'BaseEvent'
]


class Schedulable(object):

    def load_from_ds(self, ds):
        self.name = ds['name']
        self.route = ds['route']
        self.policy = ds['policy']
        self.executor = {
            'class': LocalShellExecutor,
            'params': ds['executor']['params']
        }


class Executable(object):

    def load_from_req(self, params, payload=''):
        self.params = params
        self.payload = payload


class BaseEvent(Schedulable, Executable):
    """
    TODO:
        1. need state info
        2. need to store the execution result
    """
    pass

