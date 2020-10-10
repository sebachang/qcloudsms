# -*- coding: utf-8 -*-
"""
    配置平台查询接口
"""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.app_fw.viewsets import GenericViewSet
from mt_apps.base.utils.util_site import get_jump_site, get_download_site


class AppUtilViewSet(GenericViewSet):
    """
    App通用相关接口
    """
    serializer_class = serializers.Serializer

    @action(methods=['get'], detail=False, url_path='get_jump_site')
    def get_jump_site(self, request):
        router = request.GET.get('router', '')
        result = {
            'site': get_jump_site(router)
        }

        return Response(result)

    @action(methods=['get'], detail=False, url_path='get_download_site')
    def get_download_site(self, request):
        router = request.GET.get('router', '')
        result = {
            'site': get_download_site(router)
        }
        return Response(result)
