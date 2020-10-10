# -*- coding: utf-8 -*-
"""
    配置平台查询接口
"""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.api.components.login import LoginAPI
from mt_apps.base.app_fw.viewsets import GenericViewSet


class LoginViewSet(GenericViewSet):
    """
    登录相关接口
    """
    serializer_class = serializers.Serializer

    @action(methods=['get'], detail=False, url_path='get_user_info')
    def get_user_info(self, request):
        """
            获取用户信息
        """
        data = LoginAPI.get_user_info(request)
        return Response(data)

    @action(methods=['get'], detail=False, url_path='get_all_user_info')
    def get_all_user_info(self, request):
        """
            获取所有用户信息
        """
        data = LoginAPI.get_all_user_info(request)
        return Response(data)
