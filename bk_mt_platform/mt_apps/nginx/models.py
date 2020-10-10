# -*- coding: utf-8 -*-
from django.db import models
from mt_apps.certificate.models import CertModel, DomainModel


# class TemplateModel(models.Model):
#     TEMPLATE_RTYPE_CHOICES = (
#         ('main', 'main'),
#         ('vhost', 'vhost'),
#     )
#     bk_biz = models.IntegerField(u'业务ID', default=3)
#     name = models.CharField(u'模板名', max_length=128)
#     type = models.CharField(u'模板类型', max_length=32, choices=TEMPLATE_RTYPE_CHOICES)
#     description = models.CharField(u'描述', max_length=256, null=True, blank=True)
#     content = models.TextField(u'内容', )

class ConfigModel(models.Model):
    name = models.CharField(u'配置名', max_length=64)
    bk_biz = models.IntegerField(u'业务ID', default=3)
    cert = models.ForeignKey(CertModel, verbose_name=u"证书", null=True, blank=True)
    content = models.TextField(u'内容', )

    class Meta:
        verbose_name = '配置管理'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f'配置管理[{self.name}]'

    def getCertData(self):
        from mt_apps.certificate.serializers import CertSerializer
        if self.cert:
            return CertSerializer(self.cert, many=False).data
        else:
            return {}

    def getVhosts(self):
        from mt_apps.nginx.serializers import VhostModelSerializer
        return VhostModelSerializer(VhostModel.objects.filter(config=self.id), many=True).data

    def getCluster(self):
        try:
            return ClusterModel.objects.values('id', 'name').get(config=self.id)
        except:
            return {'id': 0, 'name': ''}


class VhostModel(models.Model):
    bk_biz = models.IntegerField(u'业务ID', default=3)
    config = models.ForeignKey(ConfigModel, verbose_name=u"配置", on_delete=models.PROTECT)
    domain = models.ForeignKey(DomainModel, verbose_name=u"域名", on_delete=models.PROTECT)
    cert = models.ForeignKey(CertModel, verbose_name=u"证书", null=True, blank=True)
    port = models.IntegerField(u'端口', default=443)
    ssl = models.BooleanField(u'开启ssl', default=False)
    root = models.CharField(u'默认root', max_length=256, default="html")
    index = models.CharField(u'默认index', max_length=64, default="index.html index.htm")
    content = models.TextField(u'内容', )

    class Meta:
        verbose_name = '虚拟主机'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.domain.name + ":" + str(self.port)

    def __str__(self):
        return f'虚拟主机名[{self.domain.name + ":" + str(self.port)}]'

    def getDomainData(self):
        from mt_apps.certificate.serializers import DomainSerializer
        return DomainSerializer(self.domain, many=False).data

    def getCertData(self):
        from mt_apps.certificate.serializers import CertSerializer
        if self.cert:
            return CertSerializer(self.cert, many=False).data
        else:
            return {}

    def getConfigName(self):
        return self.config.name


class ClusterModel(models.Model):
    name = models.CharField(u'集群名', max_length=64)
    bk_biz = models.IntegerField(u'项目ID', default=3)
    config = models.OneToOneField(ConfigModel, verbose_name=u"配置", on_delete=models.PROTECT)
    hosts = models.CharField(u"集群主机", max_length=256, default='[]')
    path = models.CharField(u'工作路径', max_length=128, default="/data/app/openresty-moonton")
    log_path = models.CharField(u'日志路径', max_length=256, default="/data/applog/openresty")
    conf_path = models.CharField(u'主配置', max_length=256, default="/data/app/openresty-moonton/nginx/conf")
    vhost_path = models.CharField(u'虚拟主机', max_length=256, default="/data/app/openresty-moonton/nginx/conf")
    cert_path = models.CharField(u'证书路径', max_length=256, default=" /data/app/openresty-moonton/nginx/conf/ssl")
    module_path = models.CharField(u'模块路径', max_length=256, default="/data/app/openresty-moonton/nginx/conf/modules")
    package = models.CharField(u'程序包名', max_length=255)

    class Meta:
        verbose_name = '集群管理'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f'集群管理[{self.name}]'

    def getConfigName(self):
        return self.config.name
