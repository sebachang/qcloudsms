# -*- coding: utf-8 -*-

from rest_framework import serializers

from mt_apps.base.system_config.models import SystemSetting


class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ('biz_id', 'config_key', 'config_value',)
