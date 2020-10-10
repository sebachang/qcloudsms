import json

from .auditlog.middleware import get_current_user, get_current_request
from .auditlog.models import LogEntry


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_log_entry(biz_id, object_name, additional_data, changes={}):
    obj = LogEntry()
    obj.biz_id = biz_id
    obj.object_repr = object_name
    obj.object_pk = ''
    obj.action = 0
    obj.changes = json.dumps(changes)
    obj.additional_data = additional_data
    obj.actor = get_current_user()
    # obj.content_type_id = 0

    request = get_current_request()
    if request is not None:
        obj.remote_addr = get_client_ip(request)
    obj.save()
    pass
