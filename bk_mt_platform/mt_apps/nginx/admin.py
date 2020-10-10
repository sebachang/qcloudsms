from django.contrib import admin
from .models import ClusterModel, ConfigModel, VhostModel


class ClusterModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bk_biz', 'name', 'config', 'hosts', "package")
    search_fields = ('name',)
    ordering = ('id',)


class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bk_biz', 'name', 'cert')
    search_fields = ('name',)
    ordering = ('id',)


class VhostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bk_biz', 'config', 'domain', 'port', 'ssl', 'root', 'index')
    ordering = ('id',)


admin.site.register(ClusterModel, ClusterModelAdmin)
admin.site.register(ConfigModel, ConfigModelAdmin)
admin.site.register(VhostModel, VhostModelAdmin)