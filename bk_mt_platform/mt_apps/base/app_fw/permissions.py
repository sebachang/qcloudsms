# -*- coding: utf-8 -*-
"""
权限校验类

class XxxPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

"""
from rest_framework import permissions


class HasBKAPIPermission(permissions.BasePermission):
    """
        业务所有者权限控制
    """

    def has_permission(self, request, view):
        return True
