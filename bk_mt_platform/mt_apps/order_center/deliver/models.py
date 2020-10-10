from django.db import models

from mt_apps.deliver_manage.models import Platform, HostProfile, Center


class DeliverOrder(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING, db_constraint=False)
    host = models.ForeignKey(HostProfile, on_delete=models.DO_NOTHING, db_constraint=False)
    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, db_constraint=False)
    vlan = models.CharField(max_length=255, null=True, blank=True)
    system = models.CharField(max_length=255, null=False)
    amount = models.IntegerField(default=1)
    desc = models.CharField(max_length=255, null=False)
    remark = models.CharField(max_length=255, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_center_deliver_deliver_order"
