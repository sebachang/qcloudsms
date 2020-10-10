from django.db import models

from mt_apps.base.audit.auditlog.registry import auditlog
from mt_apps.order_center.order.models import Orders


class Platform(models.Model):
    platform_name = models.CharField(max_length=255, null=False)
    account = models.CharField(max_length=255, null=True, blank=True)
    passwd = models.CharField(max_length=255, null=True, blank=True)
    biz_id = models.IntegerField(default=0)
    state = models.IntegerField(default=0)

    def __str__(self):
        return f'厂商[{self.platform_name}]'

    class Meta:
        unique_together = ["platform_name", "biz_id"]
        db_table = "deliver_manage_platform"


class HostProfile(models.Model):
    host_name = models.CharField(max_length=255, null=False)
    cpu = models.CharField(max_length=255, null=False)
    mem = models.CharField(max_length=255, null=False)
    sdisk = models.CharField(max_length=255, null=False)
    disk = models.CharField(max_length=255, null=True, blank=True)
    ssd = models.CharField(max_length=255, null=True, blank=True)
    net = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=False)
    state = models.IntegerField(default=0)
    biz_id = models.IntegerField(default=0)

    def __str__(self):
        return f'机型[{self.host_name}]'

    class Meta:
        db_table = "deliver_manage_host"
        unique_together = ['biz_id', 'host_name']


class PlatformHostProfileMap(models.Model):
    pid = models.IntegerField()
    hid = models.IntegerField()

    class Meta:
        unique_together = ["pid", "hid"]
        db_table = "deliver_manage_platform_host_map"


class Center(models.Model):
    center_name = models.CharField(max_length=255, null=False)
    state = models.IntegerField(default=0, )
    biz_id = models.IntegerField(default=0)

    def __str__(self):
        return f'数据中心[{self.center_name}]'

    class Meta:
        db_table = "deliver_manage_center"
        unique_together = ['biz_id', 'center_name']


class PlatformCenterMap(models.Model):
    pid = models.IntegerField()
    cid = models.IntegerField()

    class Meta:
        unique_together = ["pid", "cid"]
        db_table = "deliver_manage_platform_center_map"


class DeliverDetail(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING, db_constraint=False)
    biz_id = models.IntegerField(default=0)
    bk_host_innerip = models.CharField(max_length=255, null=False)
    bk_host_outerip = models.CharField(max_length=255, null=False)
    bk_comment = models.CharField(max_length=255, null=True, blank=True)
    bk_host_outerip_2 = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    disk_type = models.CharField(max_length=255, null=True, blank=True)
    server_city = models.CharField(max_length=255, null=True, blank=True)
    bandwidth = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    server_country = models.CharField(max_length=255, null=True, blank=True)
    sl_account = models.CharField(max_length=255, null=True, blank=True)
    ssh_ip = models.CharField(max_length=255, null=True, blank=True)
    isp = models.CharField(max_length=255, null=True, blank=True)
    bk_host_name = models.CharField(max_length=255, null=True, blank=True)
    bk_os_type = models.CharField(max_length=255, null=True, blank=True)
    bk_os_name = models.CharField(max_length=255, null=True, blank=True)
    bk_os_version = models.CharField(max_length=255, null=True, blank=True)
    bk_os_bit = models.CharField(max_length=255, null=True, blank=True)
    bk_cpu = models.IntegerField(null=True, blank=True)
    bk_cpu_mhz = models.IntegerField(null=True, blank=True)
    bk_cpu_module = models.CharField(max_length=255, null=True, blank=True)
    bk_mem = models.IntegerField(null=True, blank=True)
    bk_disk = models.IntegerField(null=True, blank=True)
    bk_mac = models.CharField(max_length=255, null=True, blank=True)
    bk_outer_mac = models.CharField(max_length=255, null=True, blank=True)
    detail_flag = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'交付机器[{self.bk_host_innerip}]'

    class Meta:
        db_table = "deliver_manage_deliver_detail"
        ordering = ['-id']
        unique_together = ['biz_id', 'order', 'bk_host_innerip']


class ClearanceDetail(models.Model):
    bk_host_id = models.IntegerField()
    biz_id = models.IntegerField()
    remove_id = models.CharField(max_length=255, null=False)
    order_id = models.ForeignKey(Orders, on_delete=models.DO_NOTHING, db_constraint=False, null=True, blank=True)
    bk_host_innerip = models.CharField(max_length=255, null=True, blank=True)
    bk_host_outerip = models.CharField(max_length=255, null=True, blank=True)
    bk_comment = models.CharField(max_length=255, null=True, blank=True)
    bk_host_outerip_2 = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    disk_type = models.CharField(max_length=255, null=True, blank=True)
    server_city = models.CharField(max_length=255, null=True, blank=True)
    bandwidth = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    server_country = models.CharField(max_length=255, null=True, blank=True)
    sl_account = models.CharField(max_length=255, null=True, blank=True)
    ssh_ip = models.CharField(max_length=255, null=True, blank=True)
    isp = models.CharField(max_length=255, null=True, blank=True)
    bk_host_name = models.CharField(max_length=255, null=True, blank=True)
    bk_os_type = models.CharField(max_length=255, null=True, blank=True)
    bk_os_name = models.CharField(max_length=255, null=True, blank=True)
    bk_os_version = models.CharField(max_length=255, null=True, blank=True)
    bk_os_bit = models.CharField(max_length=255, null=True, blank=True)
    bk_cpu = models.IntegerField(null=True, blank=True)
    bk_cpu_mhz = models.IntegerField(null=True, blank=True)
    bk_cpu_module = models.CharField(max_length=255, null=True, blank=True)
    bk_mem = models.IntegerField(null=True, blank=True)
    bk_disk = models.IntegerField(null=True, blank=True)
    bk_mac = models.CharField(max_length=255, null=True, blank=True)
    bk_outer_mac = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.CharField(max_length=255, null=True, blank=True)
    clearance_flag = models.IntegerField(default=1)
    clearance_create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'清退机器[{self.bk_host_innerip}]'

    class Meta:
        db_table = "deliver_manage_clearance_detail"
        unique_together = ["biz_id", "bk_host_id", "remove_id"]
        ordering = ['id']


auditlog.register(Platform)
auditlog.register(HostProfile)
auditlog.register(Center)
auditlog.register(DeliverDetail)
auditlog.register(ClearanceDetail)
