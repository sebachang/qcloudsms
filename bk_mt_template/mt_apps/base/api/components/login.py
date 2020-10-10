# -*- coding: utf-8 -*-
"""
    登录平台接口
"""

from blueking.component.shortcuts import get_client_by_request, get_client_by_user


class LoginAPI(object):
    """
     登录接口
    """

    @classmethod
    def get_user_info(cls, request):
        client = get_client_by_request(request)
        result = client.bk_login.get_user()
        return result

    @classmethod
    def get_all_user_info(cls, request):
        client = get_client_by_request(request)
        result = client.bk_login.get_all_users()
        return result

    @classmethod
    def get_batch_user_info(cls, request=None, user=None, **bk_username):
        client = ''
        if request:
            client = get_client_by_request(request)
        if user:
            client = get_client_by_user(user)
        result = client.bk_login.get_batch_users(**bk_username)
        return result
