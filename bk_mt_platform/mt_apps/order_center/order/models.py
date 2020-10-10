from django.db import models
from django.utils import timezone

from mt_apps.base.audit.auditlog.registry import auditlog
from mt_apps.order_center.order_config.models import OrderConfig


class Orders(models.Model):
    order_config = models.ForeignKey(OrderConfig, on_delete=models.DO_NOTHING, db_constraint=False)
    # order_type_id = models.IntegerField()
    submitter = models.CharField(max_length=255, null=False)
    biz_id = models.IntegerField()
    suborder = models.IntegerField()
    order_state = models.IntegerField(default=1)
    current_approval_step = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'工单[{self.order_config.order_name}]'

    class Meta:
        db_table = "order_center_order_orders"
        ordering = ['id']


class OrderApprovalRecord(models.Model):
    # order_id = models.IntegerField()
    order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING, db_constraint=False)
    auditor = models.CharField(max_length=255, null=False)
    approval_step = models.IntegerField()
    approval_step_result = models.IntegerField()
    approval_step_remark = models.CharField(max_length=2048, null=True, blank=True)
    task_instance_id = models.IntegerField(default=0)
    jobs_state = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    # task_result = models.IntegerField()
    task_response = models.TextField(default='{}')

    class Meta:
        db_table = "order_center_order_order_approval_record"


auditlog.register(Orders)
