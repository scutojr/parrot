import queue
import json
import threading
import multiprocessing.dummy as pdummy

from flask import Flask, request, Response
from flask.views import View

from parrot.executor.base import LocalShellExecutor
from parrot.events.register import RegistrationManager
from parrot.models.db.events import BasicEvent
from parrot.events.manager import EventManager


class FifoScheduler(object):

    def __init__(self, register: RegistrationManager):
        self._queue = queue.Queue()
        self.register = register

    def register(self, event):
        pass

    def dispatch(self, event: BasicEvent):
        exec = self.register.get_executable(event)
        if self.register.get_executable(event) is not None:
            self._queue.put(event)

    def pop(self):
        return self._queue.get()


class ExecutorManager(threading.Thread):

    def __init__(self, register: RegistrationManager,
                 scheduler: FifoScheduler, max_running: int = 512):
        super(ExecutorManager, self).__init__()
        self._pool = pdummy.Pool(max_running)
        self._register = register
        self._scheduler = scheduler
        self._is_running = False

    def _get_executor(self, name: str):
        return LocalShellExecutor()

    def run(self):
        scheduler = self._scheduler
        pool = self._pool
        def worker(event: BasicEvent):
            try:
                executable = self._register.get_executable(event)
                executor = self._get_executor(executable.name)
                executor.start(executable.params)
            except Exception as e:
                # TODO: log the error
                pass
        while self._is_running:
            event = scheduler.pop()
            pool.apply(worker, (event,))

    def start(self):
        self._is_running = True
        super(ExecutorManager, self).start()

    def stop(self):
        self._is_running = False
        self._pool.close()

    def join(self, timeout=None):
        self._pool.close()
        self._pool.join()
        super().join(timeout)


class HttpHandler(View):
    methods = ['POST']

    def __init__(self, event_manager: EventManager):
        super(HttpHandler, self).__init__()
        self._event_manager = event_manager

    def dispatch_request(self, *args, **kwarg):
        try:
            payload = request.data.decode()
            event = BasicEvent.from_dict(json.loads(payload))
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
