# -*- coding: utf-8 -*-
"""
    公共混用类
"""
from rest_framework import status

from mt_apps.base.app_fw import error_code
from mt_apps.base.app_fw.permissions import HasBKAPIPermission


class ApiGenericMixin(object):
    """API视图类通用函数"""

    # TODO 权限部分加载基类中
    permission_classes = (HasBKAPIPermission,)

    def finalize_response(self, request, response, *args, **kwargs):
        """统一数据返回格式"""
        if response.data is None:
            response.data = {
                'result': True,
                'code': error_code.EC_OK,
                'message': 'success',
                'data': None
            }
        elif isinstance(response.data, (list, tuple)):
            response.data = {
                'result': True,
                "code": error_code.EC_OK,
                "message": 'success',
                "data": response.data,
            }
        elif isinstance(response.data, dict) and "code" not in response.data:
            response.data = {
                'result': True,
                "code": error_code.EC_OK,
                "message": 'success',
                "data": response.data,
            }
        if response.status_code == status.HTTP_204_NO_CONTENT and request.method == "DELETE":
            response.status_code = status.HTTP_200_OK
            # response.status_text = "OK"

        return super(ApiGenericMixin, self).finalize_response(
            request, response, *args, **kwargs
        )

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        request = super(ApiGenericMixin, self).initialize_request(request, *args, **kwargs)
        if request.method == "POST" and not request.META.get("HTTP_X_CSRFTOKEN"):
            request.META["HTTP_X_CSRFTOKEN"] = request.data.get("csrfmiddlewaretoken", "")
        return request
