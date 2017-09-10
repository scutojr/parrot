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
            id = '%s-%s-%s' % (topic, service, hostname)
            if id in self._events:
                raise Exception('Duplicated event was registered: ' + id)
            self._events[id] = src_yml

    def verify_event(self, topic: str, service: str, hsotname: str):
        return True
