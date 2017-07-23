from parrot.events.loader import *


class EventManager(object):

    def __init__(self, loader):
        self._loader = loader

        self._parse()

    def _parse(self):
        for file_name, src_yml in self._loader:
            print file_name, src_yml

    def get_events(self):
        pass
