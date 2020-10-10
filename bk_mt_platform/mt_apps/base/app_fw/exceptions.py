# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from mt_apps.base.app_fw import error_code


class ServerError(Exception):
    """
        后台错误类
    """
    MESSAGE = _(u"系统异常")
    ERROR_CODE = error_code.EC_SERVER_500_ERROR

    def __init__(self, *args):
        self.code = self.ERROR_CODE
        self.message = u"%s: %s" % (self.MESSAGE, args[0]) if args else self.MESSAGE
        super(ServerError, self).__init__(*args)

    def __str__(self):
        return "<AppError %s:(%s)>" % (self.code, self.message)


class ParamError(ServerError):
    MESSAGE = _(u"参数验证失败")
    ERROR_CODE = error_code.EC_PARAM_INCORRECT


class PermissionError(ServerError):
    MESSAGE = _(u"权限不足")
    ERROR_CODE = error_code.EC_PERMISSION_DENIED


class CommonLogicError(ServerError):
    MESSAGE = _(u"逻辑错误")
    ERROR_CODE = error_code.EC_COMMON_LOGIC_ERROR

    def __init__(self, *args):
        """组件错误信息格式化"""
        if args:
            res = args[0]
            self.MESSAGE = u"%s: %s(code=%s)" % (self.MESSAGE, res.get('message'), res.get('code'))

            super(CommonLogicError, self).__init__()
        else:
            super(CommonLogicError, self).__init__(*args)


class ComponentCallError(ServerError):
    MESSAGE = _(u"组件调用异常")
    ERROR_CODE = error_code.EC_COMPONENT_CALL

    def __init__(self, *args):
        """组件错误信息格式化"""
        if args:
            res = args[0]
            self.MESSAGE = u"%s: %s(code=%s)" % (self.MESSAGE, res.get('message'), res.get('code'))

            super(ComponentCallError, self).__init__()
        else:
            super(ComponentCallError, self).__init__(*args)
