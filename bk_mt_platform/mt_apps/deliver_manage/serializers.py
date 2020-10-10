# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField, CharField

from mt_apps.deliver_manage.models import *
from mt_apps.order_center.order.serializers import OrdersSerializer


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class HostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostProfile
        fields = '__all__'


class PlatformHostProfileMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformHostProfileMap
        fields = '__all__'


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'


class PlatformCenterMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformCenterMap
        fields = '__all__'


class DeliverDetailSerializer(serializers.ModelSerializer):
    submitter = CharField(source="order.submitter", read_only=True)
    class Meta:
        model = DeliverDetail
        fields = '__all__'


class ClearanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceDetail
        fields = '__all__'


class DeliverFinishField(serializers.Field):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        has_deliver = DeliverDetail.objects.filter(Q(order_id=value) & Q(detail_flag=0)).count() > 0
        not_deliver = DeliverDetail.objects.filter(Q(order_id=value) & Q(detail_flag=1)).count() == 0
        return has_deliver and not_deliver


class DeliverOrderSerializer(OrdersSerializer):
    deliver_finish = DeliverFinishField(source='id')

    class Meta:
        model = Orders

        fields = [
            'id', 'order_config_id', 'submitter', 'biz_id', 'suborder', 'order_state', 'current_approval_step',
            'create_time', 'update_time', 'order_type', 'order_name', 'process_steps', 'deliver_finish'
        ]
