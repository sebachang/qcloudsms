# -*- coding: utf-8 -*-

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.response import Response

from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.permission import serializers
from mt_apps.base.permission.models import Route, Group
from .authenticate import IsBkAdminAuthenticated
from .pagination import StandardResultsSetPagination


class RouteViewSet(ModelViewSet):
    permission_classes = (IsBkAdminAuthenticated,)

    queryset = Route.objects.all()
    serializer_class = serializers.RouteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'biz_id']
    search_fields = ['name', 'routes']
    ordering_fields = ['id']


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'biz_id']
    search_fields = ['users', ]
    ordering_fields = ['id']


class GroupsViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.serializers.Serializer

    def retrieve(self, request, *args, **kwargs):
        res = []
        biz_id = int(self.kwargs["pk"])
        if biz_id:
            objs = Group.objects.filter(biz_id=int(biz_id))
            for obj in objs:
                res.append({'id': obj.id, 'name': obj.name})

        return Response(res)


class UserRoutesViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.serializers.Serializer

    def list(self, request, *args, **kwargs):
        import json
        res = []

        biz_id = request.GET.get('biz_id')
        name = request.GET.get('name')
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
        return Response({'setting': json.dumps(res)})
