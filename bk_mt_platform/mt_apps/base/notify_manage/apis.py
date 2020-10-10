from mt_apps.base.notify_manage.constants import Types
from mt_apps.base.notify_manage.impls.notify_manager import NotifyManager


# 参考 https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
def send_message(biz_id, content=None, tag=None, type=Types.notify, json=None, at_users=None, at_all=False):
    NotifyManager().send_message(biz_id, tag, type, json=json, content=content, at_users=at_users, at_all=at_all)
