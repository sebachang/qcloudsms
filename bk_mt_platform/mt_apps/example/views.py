# -*- coding: utf-8 -*-
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.app_fw.viewsets import GenericViewSet, ModelViewSet
from mt_apps.example.impls import ExampleGenericAPI
from mt_apps.example.models import ExampleModel
from mt_apps.example.serializers import ExampleSerializer


def test_example(request):
    return HttpResponse("test_example")


class ExampleViewSet(ModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleSerializer


class ExampleGenericViewSet(GenericViewSet):
    serializer_class = serializers.Serializer

    @action(methods=['get'], detail=False, url_path='test_generic_api')
    def test_generic_api(self, request):
        data = ExampleGenericAPI.test_generic_api(request, 1)
        return Response(data)
