from django.db import models


class ServerModel(models.Model):
    app = models.CharField(u"应用", max_length=64, )
    server = models.CharField(u"服务", max_length=64, )
    division = models.CharField(u"分区", max_length=64, primary_key=True)
    node = models.CharField(u"节点", max_length=64)
    status = models.IntegerField(u"状态")
    use_agent = models.IntegerField(u"代理")

    class Meta:
        unique_together = ('app', 'server', 'division', 'node')
        db_table = "t_server"
        verbose_name = 'Server管理'
        verbose_name_plural = verbose_name


class ReleaseOrder(models.Model):
    release_id = models.AutoField(u"发布id", primary_key=True)
    env = models.CharField(u"发布环境", max_length=64, default='aliyun')
    release_version = models.CharField(u"发布版本号", max_length=64, null=False)
    svn_version = models.IntegerField(u"svn版本号", null=False)
    release_flag = models.CharField(u"发布标志", max_length=64, default='0:0:0')
    state = models.IntegerField(u"状态", default=1)
    enable = models.IntegerField(u"是否启用", default=1)
    contact_user = models.CharField(u"内容提供人", max_length=128, null=True, blank=True)
    desc = models.CharField(u"数据库脚本描述", max_length=256, default='0')
    reason = models.CharField(u"原因", max_length=256, null=False)
    level = models.IntegerField(u"优先等级", default=0)
    servers = models.CharField(u"服务", max_length=512, null=False)
    server_list = models.TextField(u"服务列表", null=False)
    remark = models.TextField(u"描述/说明", default='无')

    class Meta:
        db_table = "order_center_release_release_order"
        verbose_name = '发布申请'
        verbose_name_plural = verbose_name
