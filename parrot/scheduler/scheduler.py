import Queue
import threading
import multiprocessing.dummy as pdummy
from copy import deepcopy

from flask import Flask, request
from flask.views import View

from parrot.events.event import BaseEvent, Schedulable, Executable


class FifoScheduler(object):

    def __init__(self, event_manager, queue_size):
        self._queue = Queue.Queue()

    def register(self, event):
        if not isinstance(event, Schedulable):
            raise Exception('failed to register non schedulable object.')

    def dispatch(self, event):
        self._queue.put(event)

    def pop(self):
        return self._queue.get()


class ExecutorManager(threading.Thread):

    def __init__(self, scheduler, max_running=512):
        super(ExecutorManager, self).__init__()
        self._pool = pdummy.Pool(max_running)
        self._scheduler = scheduler
        self._is_running = False

    def run(self):
        scheduler = self._scheduler
        pool = self._pool
        def worker(event):
            try:
                params, payload = event.params, event.payload
                exe = event.executor
                action = exe['class'](**exe['params'])
                action.start(params, payload)
            except Exception as e:
                # TODO: log the error
                pass
        while self._is_running:
            event = scheduler.pop()
            pool.apply_async(worker, (event,))

    def start(self):
        self._is_running = True
        super(ExecutorManager, self).start()

    def stop(self):
        self._is_running = False
        self._pool.close()

    def join(self):
        self._pool.join()
        super(ExecutorManager, self).join()


class HttpHandler(View):
    methods = ['GET', 'POST']

    def __init__(self, event, scheduler):
        super(HttpHandler, self).__init__()
        self._event = event
        self._scheduler = scheduler

    def dispatch_request(self, *args, **kwarg):
        if request.method == 'POST':
            payload = request.data
        else:
            payload = ''

        ep = dict()
        ep.update(kwarg)
        ep.update(request.args)
        event = deepcopy(self._event)
        event.load_from_req(ep, payload)
        self._scheduler.dispatch(event)
        return str('')


class HttpBackend(object):

    def __init__(self, scheduler):
        self._app = Flask('HttpParrot')
        self._scheduler = scheduler

    def route(self, events):
        for e in events:
            self._app.add_url_rule(e.route,
                    view_func=HttpHandler.as_view('Http-' + e.name,
                    event=e,scheduler=self._scheduler))

    def get_app(self):
        return self._app

