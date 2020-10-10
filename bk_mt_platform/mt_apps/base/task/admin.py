from django.contrib import admin

from .models import JobModel, TaskInstanceModel


class JobModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_uuid', 'title', 'module', 'exec_ip', 'username', 'script_name', 'create_time')
    search_fields = ('id', 'title', 'job_uuid', 'exec_ip')
    list_filter = ('module',)
    ordering = ('id', 'create_time')


class TaskInstanceModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'instance', 'job', 'name', 'user', 'create_time')
    search_fields = ('user', 'create_time',)
    list_filter = ('job',)
    ordering = ('id', 'create_time')


admin.site.register(JobModel, JobModelAdmin)
admin.site.register(TaskInstanceModel, TaskInstanceModelAdmin)
