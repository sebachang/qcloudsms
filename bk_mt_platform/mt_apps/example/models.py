# -*- coding: utf-8 -*-

from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog


class ExampleModel(models.Model):
    biz_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()

    class Meta:
        ordering = ('created',)


auditlog.register(ExampleModel)
