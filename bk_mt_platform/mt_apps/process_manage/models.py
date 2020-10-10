import hashlib

from django.db.models import *

from mt_apps.base.audit.auditlog.registry import auditlog
from mt_apps.config_center.impls import render_config
from mt_apps.config_center.models import ConfigTemplate


class Process(Model):
    biz_id = IntegerField(u'业务ID')
    name = CharField(u'进程名', max_length=255)
    template = ForeignKey(to=ConfigTemplate)
    conf_path = CharField(u'配置文件路径', max_length=1024)
    start_cmd = CharField(u'启动命令', max_length=1024)
    stop_cmd = CharField(u'停止命令', max_length=1024)
    restart_cmd = CharField(u'重启命令', max_length=1024)
    reload_cmd = CharField(u'重载命令', max_length=1024)
    pack_name = CharField(u'程序包名', max_length=255)

    def __str__(self):
        return f'进程模板[{self.name}]'

    class Meta:
        unique_together = ('biz_id', 'name')
        ordering = ['name']


class Instance(Model):
    biz_id = IntegerField(u'业务ID')
    process = ForeignKey(Process)
    machine = CharField(u'主机', max_length=255)
    desc = CharField(u'描述', max_length=255)
    work_dir = CharField(u'工作目录', max_length=255)
    launch_user = CharField(u'启动用户', max_length=1024)
    pid_path = CharField(u'pid文件路径', max_length=1024)
    auto_restart = IntegerField(u'是否自动拉起', blank=True, default=0)
    restart_interval = IntegerField(u'拉起间隔', blank=True, default=60)
    operate_timeout = IntegerField(u'操作超时时长', blank=True, default=600)

    def get_server_ip(self):
        arr = self.machine.split(':')
        if len(arr) > 1:
            return arr[1]
        else:
            return arr[0]

    def get_config(self):
        machine = self.get_server_ip()

        return render_config(self.biz_id, self.process.template.name, {'ServerIP': machine})

    def get_config_md5(self):
        h = hashlib.md5(self.get_config().encode('utf-8'))
        return h.hexdigest()

    def __str__(self):
        return "进程实例[%s-%s]" % (self.process.name, self.work_dir)

    class Meta:
        unique_together = ('biz_id', 'process', 'machine', 'work_dir')
        ordering = ['-id']


auditlog.register(Process)
auditlog.register(Instance)
