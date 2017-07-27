import abc
from subprocess import Popen, PIPE


# TODO: develop a metaclass to inmitate java enumeration
# TODO: to_string()
class Status(object):
    INITIAL = 1
    RUNNING = 2
    PASSED = 3
    FAILED = 4
    KILLED = 5


class BaseExecutor(abc.ABCMeta):

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def get_status(self):
        pass


class LocalShellExecutor(BaseExecutor):

    def __init__(self, cmd):
        self._cmd = cmd
        self._proc = None
        self._status = Status.INITIAL

    def run(self):
        self._proc = Popen(self._cmd, shell=True, stdout=PIPE, stderr=PIPE)
        self._proc.wait()
        self._status = self._proc.returncode != 0 and Status.FAILED or Status.PASSED

    def start(self):
        self._status = Status.RUNNING
        self.run()

    def stop(self):
        self._proc.terminate()
        self._status = self._proc.returncode != 0 and Status.FAILED or Status.PASSED

    def get_status(self):
        return self._status
