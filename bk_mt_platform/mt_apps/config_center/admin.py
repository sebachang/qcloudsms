from django.contrib import admin

from .models import ConfigTemplate, ConfigKV


@admin.register(ConfigTemplate)
class ConfigTemplateModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfigKV)
class ConfigKVModelAdmin(admin.ModelAdmin):
    pass
