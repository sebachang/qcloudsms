# -*- coding: utf-8 -*-
from django.http import HttpResponse

from .models import CertModel, DomainModel, ClusterModel
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from rest_framework import viewsets

from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins

from .serializers import CertSerializer, DomainSerializer, ClusterSerializer
from rest_framework import serializers
from rest_framework.response import Response

from .cert_manager import register
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from blueapps.account.decorators import login_exempt


class CertViewSet(ModelViewSet):
    queryset = CertModel.objects.all()
    serializer_class = CertSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['domain', 'bk_biz']
    search_fields = ['domain', 'name']
    ordering_fields = ['id', 'create_time', 'expired_time']


class DomainViewSet(ModelViewSet):
    queryset = DomainModel.objects.all()
    serializer_class = DomainSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'bk_biz']
    search_fields = ['name']
    ordering_fields = ['id', 'create_time', 'expired_time', 'check_time']


class ClusterViewSet(ModelViewSet):
    queryset = ClusterModel.objects.all()
    serializer_class = ClusterSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'bk_biz']
    search_fields = ['name', 'hosts']
    ordering_fields = ['id']


class CertCheckViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def retrieve(self, request, *args, **kwargs):
        res = {}

        if 'pk' in self.kwargs:
            if self.kwargs["pk"] != '':
                try:
                    obj = DomainModel.objects.get(id=int(self.kwargs["pk"]))
                    obj.save()
                    res = {'id': obj.id, 'name': obj.name}
                except:
                    pass

        return Response(res)


class CertListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        res = []
        queryset = CertModel.objects.all()
        for obj in queryset:
            res.append({'id': obj.id, 'name': obj.domain})

        return Response(res)


class DomainListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        res = []
        queryset = DomainModel.objects.all()
        for obj in queryset:
            res.append({'id': obj.id, 'name': obj.name})

        return Response(res)


@login_exempt
def CertDownloadViewSet(request, pk, zipfile=''):
    import os
    from .util.zip import ZipUtilities
    from django.http import StreamingHttpResponse
    import settings

    id = int(pk)

    try:
        cert_obj = CertModel.objects.get(id=id)
    except CertModel.DoesNotExist as e:
        return HttpResponse("404 Content Not Found", status=404)
    if cert_obj.name:
        cert_name = cert_obj.name
    else:
        cert_name = cert_obj.domain
    cert_crt = cert_obj.crt
    cert_key = cert_obj.key

    if zipfile == '':
        zipfile = cert_name

    utilities = ZipUtilities()
    file_objs = [cert_name + '.crt', cert_name + '.key']
    for filename in file_objs:
        tmp_dl_path = os.path.join(settings.TMP_DIR, filename)
        with open(tmp_dl_path, 'w') as file_object:
            if filename == cert_name + '.crt':
                file_object.write(cert_crt)
            if filename == cert_name + '.key':
                file_object.write(cert_key)
            file_object.close()
            utilities.toZip(tmp_dl_path, filename)
    # utilities.close()
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(zipfile + ".zip")
    return response


class CertRegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        result = {u'message': u'', u'data': {}, 'result': False}

        if 'domain' in request.data:
            domain = request.data["domain"]
            try:
                result['data'] = register(domain)
                result['result'] = True
            except Exception as e:
                result['message'] = str(e)
        else:
            request['message'] = '请传入domain参数'

        return Response(result)
