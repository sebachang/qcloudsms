# -*- coding: utf-8 -*-

from django.db import models


class Group(models.Model):
    biz_id = models.IntegerField(u'业务ID', default=0)
    name = models.CharField(u'组名', max_length=32)
    users = models.TextField(u'用户列表', default='[]')
    description = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        unique_together = ["biz_id", "name"]
        verbose_name = '用户组'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.biz_id) + "-" + self.name

    def __str__(self):
        return str(self.biz_id) + "-" + self.name


class Route(models.Model):
    biz_id = models.IntegerField(u'业务ID', default=0)
    name = models.CharField(u'角色名', max_length=32)
    group = models.ManyToManyField(Group, verbose_name='用户组')
    routes = models.TextField(u'路由列表', default='[]')
    description = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        unique_together = ["biz_id", "name"]
        verbose_name = '角色授权'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.biz_id) + "-" + self.name

    def __str__(self):
        return str(self.biz_id) + "-" + self.name
