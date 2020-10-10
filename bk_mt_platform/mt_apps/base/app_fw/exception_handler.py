# -*- coding: utf-8 -*-
import traceback

from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (AuthenticationFailed, MethodNotAllowed, NotAuthenticated,
                                       PermissionDenied, ValidationError)
from rest_framework.response import Response
from rest_framework.views import set_rollback

from blueking.component.exceptions import ComponentBaseException
from mt_apps.base.app_fw import error_code
from mt_apps.base.app_fw.exceptions import *
from mt_apps.base.utils.util_log import util_logger as logger


def exception_handler(exc, context):
    """
        异常统一处理处理
        分类：
            rest_framework框架内异常
            app自定义异常
    """
    data = {
        'result': False,
        'data': None
    }
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        data = {
            'result': False,
            'code': error_code.EC_UNAUTHORIZED,
            'detail': u"用户未登录或登录态失效，请使用登录链接重新登录",
            'login_url': '',
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, PermissionDenied):
        data = {
            'result': False,
            'code': error_code.EC_PERMISSION_DENIED,
            'message': exc.detail,
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    else:
        if isinstance(exc, ValidationError):
            data.update({
                'code': error_code.EC_VALIDATE_ERROR,
                'message': exc.detail,
            })

        elif isinstance(exc, MethodNotAllowed):
            data.update({
                'code': error_code.EC_METHOD_NOT_ALLOWED,
                'message': exc.detail,
            })
        elif isinstance(exc, PermissionDenied):
            data.update({
                'code': error_code.EC_PERMISSION_DENIED,
                'message': exc.detail,
            })

        # 蓝鲸组件接口异常
        elif isinstance(exc, ComponentBaseException):
            data.update({
                'code': error_code.EC_BK_COMPONENT_API,
                'message': exc.error_message,
            })

        # 更改返回的状态为为自定义错误类型的状态码
        elif isinstance(exc, ServerError):
            data.update({
                'code': exc.code,
                'message': exc.message,
            })
        # 更改返回的状态为为自定义错误类型的状态码
        elif isinstance(exc, Http404):
            data.update({
                'code': error_code.EC_OBJECT_NOT_EXIST,
                'message': 'Http404',
            })
        else:
            # 调试模式
            logger.error(traceback.format_exc())
            print(traceback.format_exc())
            # if settings.RUN_MODE != 'PRODUCT':
            #     raise exc
            # 正式环境，屏蔽500
            data.update({
                'code': error_code.EC_SERVER_500_ERROR,
                'message': exc.message,
            })

        set_rollback()
        return Response(data, status=status.HTTP_200_OK)
