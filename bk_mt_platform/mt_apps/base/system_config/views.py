# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.system_config.impls import SystemConfigGenericAPI
from mt_apps.base.system_config.models import SystemSetting
from mt_apps.base.system_config.serializers import SystemConfigSerializer


class SystemConfigViewSet(ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemConfigSerializer

    lookup_field = 'config_key'

    def filter_queryset(self, queryset):
        if self.request.method == 'GET' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise CommonLogicError({'code': 10001, 'message': u"未传递biz_id或biz_id为负值"})
            return queryset.filter(biz_id=biz_id)
        return queryset


class SystemConfigGeneric(GenericViewSet):
    serializer_class = serializers.Serializer

    @action(methods=['get'], detail=False, url_path='get_list')
    def get_list(self, request):
        data = SystemConfigGenericAPI.get_list(request)
        return Response(data)


class SCViewSet(ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemConfigSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['biz_id', 'config_key']
    search_fields = ['config_key', ]
    ordering_fields = ['id', 'biz_id', ]
