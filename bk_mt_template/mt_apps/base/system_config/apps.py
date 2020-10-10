from django.apps import AppConfig


class SystemConfigAppConfig(AppConfig):
    name = 'mt_apps.base.system_config'

    def ready(self):
        from conf.default import INSTALLED_APPS
        for p in INSTALLED_APPS:
            try:
                _module = __import__(p + '.mt_config', fromlist=['register_config'])
                _module.register_config()
            except ImportError as e:
                pass
            except AttributeError as e:
                pass
