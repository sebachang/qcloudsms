# -*- coding: utf-8 -*-

import json

from rest_framework import serializers

from mt_apps.base.permission.models import Route, Group


class RouteSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = "__all__"

    def get_group_name(self, obj):
        return [i[0] for i in obj.group.values_list('name')]


class GroupSerializer(serializers.ModelSerializer):
    user_list = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_user_list(self, obj):
        return json.loads(obj.users)
