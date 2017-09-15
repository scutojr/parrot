
# when you import this package, it will initialize from
# the env automatically

__all__ = [
    'phase', 'Reporter',
    'Primitive', 'SessionLocalVariable'
]

def phase(description):
    pass


class Reporter(object):

    def print(self, info):
        pass

    def heartbeat(self):
        pass

    def progress(self, int):
        pass

    def set_status(self, status):
        pass


class Primitive(object):

    def wait(self):
        pass


class SessionLocalVariable(object):
    pass


class Transportation(object):
    pass
