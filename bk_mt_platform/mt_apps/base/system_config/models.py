# -*- coding: utf-8 -*-

from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog


class SystemSetting(models.Model):
    biz_id = models.IntegerField(default=0)
    config_key = models.CharField(max_length=64, null=True)
    config_value = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'系统配置[{self.config_key}]'

    class Meta:
        unique_together = ("biz_id", "config_key")


auditlog.register(SystemSetting)
