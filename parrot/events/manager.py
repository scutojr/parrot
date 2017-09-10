from collections import defaultdict

from parrot.models.db.events import BasicEvent
from parrot.events.loader import *
from parrot.events.register import RegistrationManager

from parrot.models.db.events import *


class EventManager(object):

    def __init__(self, register: RegistrationManager, scheduler):
        self.register = register
        self.scheduler = scheduler
        self._event_pool = defaultdict(list)

    def get_events(self):
        return self._events

    def add_event(self, event: BasicEvent):
        if not self.register.verify_event(event.topic, event.service,
                                    event.hostname):
            raise Exception('this event may not yet be registered!')
        # event.save()
        id = '%s-%s-%s' % (event.topic, event.service, event.hostname)
        self._event_pool[id].append(event)
        self.scheduler.dispatch(event)

    def get_event(self, topic=None, service=None, hostname=None):
        pass

    def _notify_scheduler(self):
        pass
