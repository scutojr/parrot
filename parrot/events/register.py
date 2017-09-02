



class RegistrationManager(object):

    def __init__(self, loader):
        self._loader = loader
        self._parse()
        self._events = list()

    def _parse(self):
        for file_name, src_yml in self._loader:
            event = BaseEvent()
            event.load_from_ds(src_yml)
            self._events.append(event)

    def verify_event(self, event):
        return True
