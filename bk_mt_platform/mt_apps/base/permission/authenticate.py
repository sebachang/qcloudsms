# -*- coding: utf-8 -*-
import json

from rest_framework.permissions import BasePermission

from mt_apps.base.api.components.login import LoginAPI
from mt_apps.base.permission.models import Route, Group


class IsBkAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            obj = LoginAPI().get_user_info(request)
            if obj['code'] == 0:
                if obj['data']['bk_role'] == 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


class IsRoutesAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            res = []

            path_info = request._request.path.strip().split('/')
            path_info = [i for i in path_info if i != '']
            if len(path_info) >= 3:
                path = '/' + path_info[0] + '/' + path_info[1]
            else:
                path = path_info
            biz_id = int(request._request.COOKIES['mt_curr_biz'])
            name = request.user
            groups = []
            gObjs = Group.objects.filter(biz_id=int(biz_id))
            for gObj in gObjs:
                users = json.loads(gObj.users)
                if name in users:
                    groups.append(gObj.id)

            if biz_id and name:
                queryset = Route.objects.filter(group__in=groups, biz_id=int(biz_id))
                for obj in queryset:
                    routes = json.loads(obj.routes)
                    res = res + routes

            res = list(set(res))
            if path in res:
                return True
            else:
                return False
        else:
            return False
