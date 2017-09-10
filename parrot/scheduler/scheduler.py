import queue
import json
import threading
import multiprocessing.dummy as pdummy

from flask import Flask, request, Response
from flask.views import View

from parrot.events.event import Schedulable
from parrot.models.db.events import BasicEvent
from parrot.events.manager import EventManager



class FifoScheduler(object):

    def __init__(self, queue_size):
        self._queue = queue.Queue()

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
    methods = ['POST']

    def __init__(self, event_manager: EventManager):
        super(HttpHandler, self).__init__()
        self._event_manager = event_manager

    def dispatch_request(self, *args, **kwarg):
        try:
            payload = request.data.decode()
            event = BasicEvent.from_dict(json.loads(payload))
            print(event.tags)
            self._event_manager.add_event(event)
        except ValueError as e:
            # TODO log here
            return Response('failed to parse the json: ' + str(e), 400)
        except TypeError as e:
            return Response('data contains undesired fields: ' + str(e), 400)
        return Response('')


class HttpBackend(object):

    def __init__(self, event_manager: EventManager):
        self._app = Flask('HttpParrot')
        self._event_manager = event_manager
        self._route()

    def _route(self):
        self._app.add_url_rule(
            '/parrot/api/v1/events',
            view_func=HttpHandler.as_view(
                'dispatch-event', event_manager=self._event_manager
            )
        )

    def get_app(self):
        return self._app

