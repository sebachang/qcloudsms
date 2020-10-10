# -*- coding: utf-8 -*-
import uuid

from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog
from mt_apps.base.task.job_module import JobModule


class JobModel(models.Model):
    script_default_template = "#!/bin/bash\necho 'test'\nexit 0"
    # JOB_RTYPE_CHOICES = (
    #     ('script', 'script'),
    #     ('template', 'template'),
    # )
    job_uuid = models.UUIDField(default=uuid.uuid4)
    bk_biz = models.IntegerField(u'蓝鲸项目ID')
    module = models.CharField(u"模块", max_length=32, default='default')
    title = models.CharField(u"标题", max_length=32)
    # type = models.CharField(u"作业类型", choices=JOB_RTYPE_CHOICES, max_length=16, default='script')
    # bk_job_id = models.IntegerField(u"模板ID", default=-1)
    exec_ip = models.TextField(u"执行地址", default='[]')
    username = models.CharField(u"作业账户", max_length=32, blank=True, null=True)
    # script = models.TextField(u"脚本", default=base64.b64encode(script_default_template.encode(encoding="utf-8")))
    script = models.TextField(u"脚本", null=True, blank=True)
    script_name = models.CharField(u"脚本名", max_length=32, blank=True, null=True)
    callback = models.CharField(u"回调地址", max_length=512, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __str__(self):
        return "任务作业[%s]" % self.job_uuid

    class Meta:
        verbose_name = '作业管理'
        verbose_name_plural = verbose_name
        unique_together = (("bk_biz", "job_uuid"),)
        ordering = ['-id']

    def __unicode__(self):
        return str(self.id)


class TaskInstanceModel(models.Model):
    instance = models.IntegerField(u"实例", unique=True)
    job = models.ForeignKey(JobModel, verbose_name="作业ID", on_delete=models.PROTECT)
    name = models.CharField(u"任务名", max_length=128)
    user = models.CharField(u"启动人", max_length=64)
    is_finished = models.BooleanField(u'是否完成', default=False)
    status = models.IntegerField(u"状态", default=-1)
    create_time = models.DateTimeField(u'提交时间', auto_now_add=True)
    start_time = models.DateTimeField(u'启动时间', null=True, blank=True)
    end_time = models.DateTimeField(u'启动时间', null=True, blank=True)
    total_time = models.IntegerField(u"总耗时", default=0)
    result_log = models.TextField(u'返回结果', null=True, blank=True)

    def __str__(self):
        return "作业实例[%s]" % self.instance

    class Meta:
        verbose_name = '任务实例'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.name

    def get_job_name(self):
        return self.job.title

    # def get_job_type(self):
    #     return self.job.type


auditlog.register(JobModel, biz_field='bk_biz')
