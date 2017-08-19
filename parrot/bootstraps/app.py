from parrot.conf import Configuration
from parrot.events.loader import Loader
from parrot.events.manager import EventManager
from parrot.scheduler.scheduler import HttpBackend, FifoScheduler, ExecutorManager


def main():
    conf = Configuration.load()
    loader = Loader(conf)
    event_manager = EventManager(loader)
    events = event_manager.get_events()

    scheduler = FifoScheduler(event_manager, 512)
    executor_manager = ExecutorManager(scheduler)
    executor_manager.start()

    backend = HttpBackend(scheduler)
    backend.route(events)
    app = backend.get_app()
    app.run('localhost', 12213, True)
