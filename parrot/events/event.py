import copy
from functools import partial


__all__ = [
    'BaseEvent'
]


def _generic_getter(prop_name, self):
    try:
        return self._attributes[prop_name]
    except:
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, prop_name))


def _generic_setter(prop_name, self, value):
    self._attributes[prop_name] = value


def _generic_deleter(prop_name, self):
    del self._attributes.pop[prop_name]


class FieldAttribute(object):

    def __init__(self, type, default):
        self.type = type
        self.default = default


class Base(type):

    def __new__(cls, name, bases, namespace):
        dst = super(Base, cls).__new__(cls, name, bases, namespace)
        attributes = dict()
        for member in dir(dst):
            value = getattr(dst, member)
            if isinstance(value, FieldAttribute):
                member = member.lstrip('_')
                getter = partial(_generic_getter, member)
                setter = partial(_generic_setter, member)
                deleter = partial(_generic_deleter, member)
                setattr(dst, member, property(getter, setter, deleter))
                attributes[member] = copy.deepcopy(value.default)
        dst._attributes = attributes
        return dst


class Schedulable(object):

    _name = FieldAttribute('str', '')
    _route = FieldAttribute('str', '')
    _policy = FieldAttribute('list', [])
    _executor = FieldAttribute('str', '')

    def load_from_ds(self, ds):
        self.name = ds['name']
        self.route = ds['route']
        self.policy = ds['policy']
        self.executor = ds['executor']


class Executable(object):

    _params = FieldAttribute('dict', {})
    _payload = FieldAttribute('str', '')

    def load_from_req(self, params, payload=''):
        self.params = params
        self.payload = payload


class BaseEvent(Schedulable, Executable):
    __metaclass__ = Base

