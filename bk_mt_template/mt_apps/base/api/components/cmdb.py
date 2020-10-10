# -*- coding: utf-8 -*-
"""
    配置平台接口
"""

from blueking.component.shortcuts import get_client_by_request


class CmdbAPI(object):
    """
    配置中心接口
    """

    @classmethod
    def get_biz_list_by_user(cls, request):
        # 老版本接口
        # client = get_client_by_request(request)
        # client.set_bk_api_ver('')
        # result = client.cc.get_app_by_user()

        # 新版本接口
        bk_username = request.GET.get('name')
        client = get_client_by_request(request)
        xagrs = {
            "fields": [
                "bk_biz_id",
                "bk_biz_name"
            ],
            "condition": {
                "bk_biz_maintainer": bk_username
            },
        }
        result = client.cc.search_business(xagrs)

        return result

    @classmethod
    def search_host(cls, request, page_start_num=0, page_limit_num=10, ip_addr=''):
        bk_biz_id = request.GET.get('biz_id')
        page_start = int(request.GET.get('page_start', page_start_num))
        page_limit = int(request.GET.get('page_limit', page_limit_num))
        ip = request.GET.get('ip', ip_addr)
        client = get_client_by_request(request)
        xagrs = {
            'bk_biz_id': bk_biz_id,
            'condition': [{
                'bk_obj_id': 'host',
                'fields': ['bk_host_innerip']
            }, {
                'bk_obj_id': 'set',
                'fields': []
            }, {
                'bk_obj_id': 'module',
                'fields': []
            }, {
                'bk_obj_id': 'biz',
                'fields': []
            }],
            'page': {
                'start': page_start,
                'limit': page_limit,
                'sort': 'bk_host_id'
            },
            "pattern": "123",
            "ip": {
                "data": [ip],
                "flag": "bk_host_innerip|bk_host_outerip"
            }
        }

        result = client.cc.search_host(xagrs)
        return result

    @classmethod
    def search_host2(cls, request):
        client = get_client_by_request(request)
        xagrs = request.data
        result = client.cc.search_host(xagrs)
        return result

    @classmethod
    def search_biz_inst_topo(cls, request):
        bk_biz_id = request.GET.get('biz_id')
        client = get_client_by_request(request)
        xagrs = {
            'bk_biz_id': bk_biz_id,
            'level': -1,
        }
        result = client.cc.search_biz_inst_topo(xagrs)
        return result

    @classmethod
    def search_inst_by_object(cls, request):
        xargs = request.data
        client = get_client_by_request(request)
        result = client.cc.search_inst_by_object(xargs)
        return result

    @classmethod
    def search_custom_query(cls, request):
        bk_biz_id = request.GET.get('biz_id')
        client = get_client_by_request(request)
        xagrs = {
            'bk_biz_id': bk_biz_id,
            'condition': {'name': ''},
            'start': 0,
            'limit': 200,
        }
        result = client.cc.search_custom_query(xagrs)
        return result

    @classmethod
    def search_object_attribute(cls, request, obj_id):
        client = get_client_by_request(request)
        xargs = {
            "bk_obj_id": obj_id,
            "bk_supplier_account": "0"
        }
        result = client.cc.search_object_attribute(xargs)
        return result
        pass

    @classmethod
    def search_clearance_host(cls, request, search_clearance_node, start_page):
        bk_biz_id = request.GET.get('biz_id')
        # ip = request.GET.get('ip')
        client = get_client_by_request(request)
        xagrs = {
            'bk_biz_id': bk_biz_id,
            'condition': [
                {
                    'bk_obj_id': 'set',
                    'fields': [],
                },
                {
                    'bk_obj_id': 'module',
                    'fields': [],
                    'condition': [
                        {
                            "field": "bk_module_name",
                            "operator": "$regex",
                            "value": search_clearance_node
                        }
                    ]
                },
                {
                    'bk_obj_id': 'biz',
                    'fields': [],
                },
                {
                    'bk_obj_id': 'object',
                    'fields': [],
                },
                {
                    'bk_obj_id': 'host',
                    'fields': [],
                },
            ],
            # "page": {
            #     "start": start_page,
            #     "limit": 10,
            #     "sort": "bk_host_id"
            # },
            # "pattern": ""
        }
        result = client.cc.search_host(xagrs)
        return result
