# -*- coding: utf-8 -*-
import json
from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog
from .cert_manager import CertInfo
from datetime import datetime


class CertModel(models.Model):
    bk_biz = models.IntegerField(u'业务ID', default=3)
    domain = models.CharField(u'域名', max_length=128)
    name = models.CharField(u'名字', max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(u'创建时间')
    expired_time = models.DateTimeField(u'过期时间')
    ca = models.TextField(u"CA证书", null=True, blank=True)
    crt = models.TextField(u"证书文件")
    key = models.TextField(u"证书秘钥")

    class Meta:
        verbose_name = '证书管理'
        unique_together = (("bk_biz", "domain"),)
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.domain

    def __str__(self):
        return f'证书管理[{self.domain}]'


class DomainModel(models.Model):
    name = models.CharField(u'域名', max_length=64)
    bk_biz = models.IntegerField(u'业务ID', default=3)
    cdn = models.BooleanField(u'CDN', default=False)
    check = models.BooleanField(u'是否检查', default=True)
    check_time = models.DateTimeField(u'检查时间', null=True, blank=True, default=None)
    create_time = models.DateTimeField(u'创建时间', null=True, blank=True, default=None)
    expired_time = models.DateTimeField(u'过期时间', null=True, blank=True, default=None)

    class Meta:
        verbose_name = '域名管理'
        unique_together = (("bk_biz", "name"),)
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.check:
            self.name = self.name.strip()
            domain = self.name.split(':')
            if len(domain) == 2:
                domain_name = domain[0]
                domain_port = int(domain[1])
            else:
                domain_name = self.name
                domain_port = 443

            info = CertInfo(domain_name, domain_port,self.cdn)
            self.check_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if info["notbefore"] and info["notafter"]:
                self.create_time = info["notbefore"]
                self.expired_time = info["notafter"]
            else:
                self.create_time = None
                self.expired_time = None
        super(DomainModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f'域名管理[{self.name}]'


class ClusterModel(models.Model):
    name = models.CharField(u'集群名', max_length=64)
    bk_biz = models.IntegerField(u'项目ID')
    domain = models.ForeignKey(DomainModel, verbose_name=u"域名", on_delete=models.PROTECT)
    cert = models.ForeignKey(CertModel, verbose_name=u"证书", on_delete=models.PROTECT)
    hosts = models.CharField(u"集群主机", max_length=256, default='[]')
    path = models.CharField(u'证书路径', max_length=64)
    script = models.CharField(u"服务器管理", max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '集群管理'
        unique_together = (("bk_biz", "name"),)
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f'集群管理[{self.name}]'

    def get_domain_name(self):
        return self.domain.name

    def get_cert_domain(self):
        return self.cert.domain

    def get_cert_name(self):
        return self.cert.name


auditlog.register(CertModel)
auditlog.register(DomainModel, biz_field='bk_biz')
auditlog.register(ClusterModel, biz_field='bk_biz')
