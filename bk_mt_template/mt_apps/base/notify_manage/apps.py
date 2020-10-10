from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class NotifyAppConfig(AppConfig):
    name = 'mt_apps.base.notify_manage'

    def ready(self):
        from mt_apps.base.notify_manage.models import Channel
        from mt_apps.base.notify_manage.models import NotifyRule
        from mt_apps.base.notify_manage.receivers import rebuild_cache

        post_save.connect(sender=Channel, receiver=rebuild_cache)
        post_save.connect(sender=NotifyRule, receiver=rebuild_cache)
        post_delete.connect(sender=Channel, receiver=rebuild_cache)
        post_delete.connect(sender=NotifyRule, receiver=rebuild_cache)

