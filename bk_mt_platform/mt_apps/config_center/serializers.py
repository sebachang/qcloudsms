# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import *


class ConfigTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigTemplate
        fields = ('id', 'biz_id', 'name', 'desc', 'content')


class ConfigKVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigKV
        fields = ('id', 'biz_id', 'key', 'value')
