import sys
import os

import yaml


class Loader(object):

    def __init__(self, conf):
        self.config_dir = conf['event.root_dir']
        self.reload()

    def __iter__(self):
        return self.event_books.iteritems()

    def reload(self):
        files = os.listdir(self.config_dir)
        event_books = dict()
        for f in files:
            event_books[f] = Loader.load(os.path.join(self.config_dir, f))
        self.event_books = event_books

    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as src:
            return yaml.load(src)
