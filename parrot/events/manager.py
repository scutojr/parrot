from collections import defaultdict

from parrot.events.event import BaseEvent
from parrot.events.loader import *


class EventManager(object):

    def __init__(self, register):
        self.register = register
        self._event_pool = defaultdict(list)

    def get_events(self):
        return self._events

    def add_event(self, event):
        if not self.register.verify(event):
            raise Exception('this event may not yet be registered!')
        id = '%s-%s-%s' % (event.topic, event.service, event.hostname)
        self._event_pool[id].append(event)

    def get_event(self, topic=None, service=None, hostname=None):
        pass

    def _notify_scheduler(self):
        pass
