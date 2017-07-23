import os


CONF = dict()

CONF['event.root_dir'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'events')
