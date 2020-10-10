from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog


class ProcessConfig(models.Model):
    biz_id = models.IntegerField(u'蓝鲸项目ID')
    process_type = models.CharField(max_length=255, null=False)
    process_name = models.CharField(max_length=255, null=False)
    process_steps = models.IntegerField()

    def __str__(self):
        return f'流程配置[{self.process_name}]'

    class Meta:
        db_table = "order_center_process_config_process_config"
        unique_together = ["biz_id", "process_type"]
        ordering = ['id']


class ApprovalFlow(models.Model):
    process = models.ForeignKey(ProcessConfig, on_delete=models.DO_NOTHING, db_constraint=False)
    step = models.IntegerField()
    step_name = models.CharField(max_length=255, default=None, blank=True)
    auditor = models.CharField(max_length=2048, default=None, blank=True)
    AUDIT_TYPE_USER = 1
    AUDIT_TYPE_GROUP = 2
    AUDIT_TYPE = (
        (AUDIT_TYPE_USER, '用户'),
        (AUDIT_TYPE_GROUP, '用户组')
    )
    audit_type = models.IntegerField(default=1, choices=AUDIT_TYPE)
    step_flag = models.IntegerField(default=1)
    description = models.CharField(max_length=255, default=None, blank=True)
    task_id = models.CharField(max_length=255, null=False)
    task_flag = models.IntegerField(default=1)
    notify_flag = models.IntegerField(default=0)

    class Meta:
        # unique_together = ["process_id"]
        db_table = "order_center_process_config_approval_flow"

    def get_audit_user(self):
        from .utils import get_audit_user
        return get_audit_user(self.audit_type, self.auditor)


auditlog.register(ProcessConfig)
