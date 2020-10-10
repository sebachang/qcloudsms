from django.db.models import Model, CharField, TextField


class DomainOrder(Model):
    domain = CharField(max_length=255)
    type = CharField(max_length=10)
    value = TextField()
    purpose = CharField(max_length=255)
    remark = TextField(null=True, blank=True, default='')
