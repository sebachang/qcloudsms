from django.db.models import *
from jsonfield import JSONField

from mt_apps.base.audit.auditlog.registry import auditlog


class Channel(Model):
    biz_id = IntegerField()
    name = CharField(max_length=255)
    type = CharField(max_length=255)
    enabled = BooleanField()
    params = JSONField(default={})


class NotifyRule(Model):
    biz_id = IntegerField()
    name = CharField(max_length=255)
    types = JSONField()
    tags = JSONField()
    destination = ManyToManyField(Channel)


auditlog.register(Channel)
auditlog.register(NotifyRule)
