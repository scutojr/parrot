from parrot.models.db.events import *


class RegistrationManager(object):

    def __init__(self, loader):
        self._loader = loader
        self._events = dict()
        self._parse()

    def _parse(self):
        for file_name, src_yml in self._loader:
            # TODO: suport hostname range
            topic, service, hostname = (
                src_yml['topic'],
                src_yml['service'],
                src_yml.get('hostname', '')
            )
            id = self._get_event_id(topic, service, hostname)
            if id in self._events:
                raise Exception('Duplicated event was registered: ' + id)
            self._events[id] = src_yml

    def _get_event_id(self, topic, service, hostname):
        return '%s-%s-%s' % (topic, service, hostname)

    def verify_event(self, topic: str, service: str, hsotname: str):
        return True

    def get_executable(self, event: BasicEvent) -> Executable:
        """

        :param event:
        :return: None or Executable obj
        """
        event_id = self._get_event_id(
            event.topic,
            event.service,
            event.hostname
        )
        event_meta = self._events.get(event_id, None)
        if event_meta is not None:
            exc = event_meta.get('executable', None)
            return exc is None and None or Executable(**exc)
        else:
            return None
