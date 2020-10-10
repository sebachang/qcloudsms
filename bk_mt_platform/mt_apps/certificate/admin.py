from django.contrib import admin
from .models import CertModel,DomainModel,ClusterModel

class CertModelAdmin(admin.ModelAdmin):
    list_display = ('id','domain','name','create_time','expired_time')
    search_fields = ('domain','name')
    ordering = ('id','create_time','expired_time')

class DomainModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','check_time','create_time', 'expired_time')
    search_fields = ('name',)
    ordering = ('id','check_time','create_time','expired_time')

class ClusterModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','domain','cert', 'hosts','path','script')
    search_fields = ('name','hosts','path')
    list_filter = ('domain','cert')
    ordering = ('id',)


admin.site.register(CertModel, CertModelAdmin)
admin.site.register(DomainModel, DomainModelAdmin)
admin.site.register(ClusterModel, ClusterModelAdmin)