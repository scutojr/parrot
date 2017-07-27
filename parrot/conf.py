import os


__all__ = [
    'Configuration'
]


class Configuration(dict):

    @staticmethod
    def load():
        conf = Configuration()
        prod = os.environ.get('PARROT_CONF_PROD', '')
        test = os.environ.get('PARROT_CONF_TEST', '')
        if prod:
            conf_root = prod
        elif test:
            conf_root = test
        else:
            conf_root = os.path.abspath(os.path.dirname(__file__)) + '/../conf/events'
        conf = Configuration()
        conf['event.root_dir'] = conf_root
        return conf

