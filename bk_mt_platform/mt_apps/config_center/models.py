from django.db.models import *

from mt_apps.base.audit.auditlog.registry import auditlog


class ConfigKV(Model):
    biz_id = IntegerField('业务ID')
    key = CharField('配置项', max_length=255)
    value = TextField('配置值')

    def __str__(self):
        return "配置项[%s]" % self.key

    class Meta:
        verbose_name = u'配置项'
        verbose_name_plural = u'配置项'
        unique_together = ('biz_id', 'key')
        ordering = ['key']


class ConfigTemplate(Model):
    biz_id = IntegerField(u'业务ID', default=0)
    name = CharField(u'模板名', max_length=50)
    desc = TextField(u'描述')
    content = TextField(u'模板内容')

    def __str__(self):
        return u"配置模板[%s]" % self.name

    class Meta:
        verbose_name = u'配置模板'
        verbose_name_plural = u'配置模板'
        unique_together = ("biz_id", "name")
        ordering = ['name']


auditlog.register(ConfigKV)
auditlog.register(ConfigTemplate)
