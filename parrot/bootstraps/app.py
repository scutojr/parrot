from parrot.conf import Configuration
from parrot.events.loader import Loader
from parrot.events.register import RegistrationManager
from parrot.events.manager import EventManager
from parrot.scheduler.scheduler import (
    HttpBackend, FifoScheduler, ExecutorManager
)


def main():
    conf = Configuration.load()
    loader = Loader(conf)
    register = RegistrationManager(loader)
    scheduler = FifoScheduler(512)
    event_manager = EventManager(register, scheduler)

    # executor_manager = ExecutorManager(scheduler)
    # executor_manager.start()

    backend = HttpBackend(event_manager)
    app = backend.get_app()
    app.run('localhost', 12213, True)
