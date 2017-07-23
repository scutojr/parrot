from functools import partial


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

    def __new__(cls, *args, **kwarg):
        dst = super(Base, cls).__new__(cls, *args, **kwarg)
        attributes = dict()
        for attr_name, attr in dst.__dict__.items():
            if isinstance(attr, FieldAttribute):
                attr_name = attr_name.lstrip('_')
                getter = partial(_generic_getter, attr_name)
                setter = partial(_generic_setter, attr_name)
                deleter = partial(_generic_deleter, attr_name)
                setattr(dst, attr_name, property(getter, setter, deleter))
                attributes[attr_name] = attr.default
        dst._attributes = attributes
        return dst


class BaseEvent(object):
    __metaclass__ = Base

    _name = FieldAttribute('str', '')
    _route = FieldAttribute('str', '')
    _policy = FieldAttribute('list', [])

