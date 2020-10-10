# -*- coding: utf-8 -*-
"""
    配置平台查询接口
"""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.api.components.cmdb import CmdbAPI
from mt_apps.base.app_fw.viewsets import GenericViewSet


class CmdbViewSet(GenericViewSet):
    """
    配置平台相关接口
    """
    serializer_class = serializers.Serializer

    @action(methods=['get'], detail=False, url_path='get_biz_list_by_user')
    def get_biz_list_by_user(self, request):
        """
        查询用户有权限的业务列表
        """
        data = CmdbAPI.get_biz_list_by_user(request)
        return Response(data)

    @action(methods=['get'], detail=False, url_path='search_host')
    def search_host(self, request):
        data = CmdbAPI.search_host(request)
        return_fields = ''
        req_fields = request.GET.get('fields')
        if req_fields is not None:
            return_fields = req_fields.split(',')
        if data['code'] == 0:
            if return_fields != '':
                def filter_fields(host):
                    ret = {'bk_cloud_id': [{'bk_inst_id': host['bk_cloud_id'][0]['bk_inst_id']}]}
                    for f in return_fields:
                        if f in host:
                            ret[f] = host[f]
                    return ret

                data['data']['info'] = [{'host': filter_fields(h['host'])} for h in data['data']['info']]
        return Response(data)

    @action(methods=['post'], detail=False, url_path='search_host2')
    def search_host2(self, request):
        data = CmdbAPI.search_host2(request)
        return Response(data)

    @action(methods=['get'], detail=False, url_path='search_biz_inst_topo')
    def search_biz_inst_topo(self, request):
        data = CmdbAPI.search_biz_inst_topo(request)
        return Response(data)

    @action(methods=['post'], detail=False, url_path='search_inst_by_object')
    def search_inst_by_object(self, request):
        data = CmdbAPI.search_inst_by_object(request)
        return Response(data)

    @action(methods=['get'], detail=False, url_path='search_custom_query')
    def search_custom_query(self, request):
        data = CmdbAPI.search_custom_query(request)
        return Response(data)
