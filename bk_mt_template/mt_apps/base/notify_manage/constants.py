from enum import Enum


Tags = (('default', '默认',),)


class Types(Enum):
    notify = 1
    warn = 2


from conf.default import INSTALLED_APPS

for p in INSTALLED_APPS:
    try:
        _module = __import__(p + '.mt_config', fromlist=['register_notify'])
        Tags += _module.register_notify()
    except ImportError as e:
        pass
    except AttributeError as e:
        pass
