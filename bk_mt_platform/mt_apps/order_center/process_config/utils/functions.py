import json

from mt_apps.base.permission.models import Group
from mt_apps.order_center.process_config.models import ApprovalFlow


def get_audit_user(audit_type, auditor):
    if auditor == '':
        return []
    result = []
    group_users = {}
    for g in Group.objects.all():
        try:
            group_users[g.id] = json.loads(g.users)
        except ...:
            pass

    if audit_type == ApprovalFlow.AUDIT_TYPE_USER:
        result = result + auditor.split(',')
    elif audit_type == ApprovalFlow.AUDIT_TYPE_GROUP:
        for gid in auditor.split(','):
            gid = int(gid)
            if gid in group_users:
                result = result + group_users[gid]
    return result
