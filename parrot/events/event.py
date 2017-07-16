

class BaseMeta(type):

    def __new__(cls, name, parents, attrs):
        return super(BaseMeta, cls).__new__(name, parents, attrs)


class BaseEvent(BaseMeta):
    _name = ''
    _route = ''
    _policy = list()
