from flask import Flask, request
from flask.views import View

from parrot.events.event import BaseEvent, Schedulable, Executable


class FifoScheduler(object):

    def __init__(self, event_manager, queue_size):
        pass

    def register(self, event):
        if not isinstance(event, Schedulable):
            raise Exception('failed to register non schedulable object.')

    def dispatch(self, event):
        pass


class HttpHandler(View):
    methods = ['GET', 'POST']

    def __init__(self, event):
        super(HttpHandler, self).__init__()
        self._event = event

    def dispatch_request(self, *args, **kwarg):
        print 'you passed the basic flow!'
        return str(132)


class HttpBackend(object):

    def __init__(self):
        self.app = Flask('HttpParrot')

    def route(self, events):
        for e in events:
            self.app.add_url_rule(e.route, view_func=HttpHandler.as_view('HttpHandler', event=e))

    def get_app(self):
        return self.app

