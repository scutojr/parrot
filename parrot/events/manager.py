from parrot.events.event import BaseEvent
from parrot.events.loader import *


class EventManager(object):

    def __init__(self, loader):
        self._loader = loader
        self._events = list()
        self._parse()

    def _parse(self):
        for file_name, src_yml in self._loader:
            event = BaseEvent()
            event.load_from_ds(src_yml)
            self._events.append(event)

    def get_events(self):
        return self._events
