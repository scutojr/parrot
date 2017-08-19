import abc
from subprocess import Popen, PIPE

from jinja2 import Template


# TODO: develop a metaclass to inmitate java enumeration
# TODO: to_string()
class Status(object):
    INITIAL = 1
    RUNNING = 2
    PASSED = 3
    FAILED = 4
    KILLED = 5


class BaseExecutor(object):

    __metaclass__ = abc.ABCMeta

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
        super(LocalShellExecutor, self).__init__()
        self._cmd = Template(cmd)
        self._proc = None
        self._status = Status.INITIAL

    def start(self, params, payload):
        cmd = self._cmd.render(params)
        self._status = Status.RUNNING
        self._proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self._proc.stdin.write(payload)
        self._proc.wait()
        self._status = self._proc.returncode != 0 and Status.FAILED or Status.PASSED

    def stop(self):
        self._proc.terminate()
        self._status = self._proc.returncode != 0 and Status.FAILED or Status.PASSED

    def get_status(self):
        return self._status
