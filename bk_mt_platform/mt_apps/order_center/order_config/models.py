from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog
from mt_apps.order_center.process_config.models import ProcessConfig


class OrderConfig(models.Model):
    biz_id = models.IntegerField(u'蓝鲸项目ID')
    order_type = models.CharField(max_length=255, null=False)
    order_name = models.CharField(max_length=255, null=False)
    process = models.ForeignKey(ProcessConfig, on_delete=models.DO_NOTHING, db_constraint=False)
    ding_api = models.CharField(max_length=1024, null=True, blank=True)
    ding_token = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'工单配置[{self.order_name}]'

    class Meta:
        db_table = "order_center_order_config_order_config"
        unique_together = ["biz_id", "order_type"]
        ordering = ['id']


auditlog.register(OrderConfig)
