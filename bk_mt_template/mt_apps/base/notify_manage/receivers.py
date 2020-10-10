from mt_apps.base.notify_manage.impls.notify_manager import NotifyManager


def rebuild_cache(sender, **kwards):
    NotifyManager().rebuild_cache()
