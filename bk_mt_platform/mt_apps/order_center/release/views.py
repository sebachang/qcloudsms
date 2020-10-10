# -*- coding: utf-8 -*-
import easywebdav
import operator
import re
import http.client, json
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.response import Response

from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.system_config.config_define import get_system_configs
from .db_manager import DBManager
from .models import ServerModel
from .pagination import StandardResultsSetPagination
from .serializers import ServerModelSerializer


class ServerlistViewSet(ModelViewSet):
    serializer_class = ServerModelSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ServerModel.objects.all()
        try:
            biz_id = self.request.query_params['biz_id']
            sel_server = self.request.query_params['server']
            sel_devision = self.request.query_params['division']
            order_value = self.request.query_params['ordering']
            if DBManager(biz_id).set_mfw_db():
                queryset = ServerModel.objects.using('mfw')
                if sel_server != '':
                    servers = sel_server.split(',')
                    queryset = queryset.filter(server__in=servers)
                if sel_devision != '':
                    queryset = queryset.filter(division__contains=sel_devision)
                queryset = queryset.filter(app='MOBA').order_by(order_value)
        except:
            pass

        return queryset


class SelectServersViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = ServerModelSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ServerModel.objects.all().order_by()
        try:
            biz_id = self.request.query_params['biz_id']
            if DBManager(biz_id).set_mfw_db():
                queryset = ServerModel.objects.using('mfw').raw(
                    'select distinct server, division from t_server group by server order by server asc')
        except:
            pass

        return queryset

    def list(self, request, *args, **kwargs):
        datas = []
        queryset = self.get_queryset()

        for obj in queryset:
            datas.append({"value": obj.server, "label": obj.server})

        return Response(datas)


class VersionViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        try:
            biz_id = self.request.query_params['biz_id']
            system_config = get_system_configs(biz_id,
                                               ['svn_host', 'svn_protocol', 'svn_path', 'svn_port', 'svn_username',
                                                'svn_password'])
            res = []
            webdav = easywebdav.connect(
                host=system_config['svn_host'],
                username=system_config['svn_username'],
                port=system_config['svn_port'],
                protocol=system_config['svn_protocol'],
                password=system_config['svn_password'],
                path=system_config['svn_path'],
                verify_ssl=False)

            datas = []
            for i in webdav.ls():
                datas.append({'name': i.name, 'ctime': i.ctime})

            sorted_x = sorted(datas, key=operator.itemgetter('ctime'), reverse=True)

            for i in sorted_x:
                path = i["name"].split('/')[-2]
                if re.match(r'^Android-[1-9]\.[4-9]\.[0-9]+\.[0-9]+\.[0-9]+(_[0-9a-zA-Z\.]+)*$', path):
                    res.append(path)
            res.sort(reverse = True)
        except Exception as e:
            raise e

        return Response(res)


class GetSerVersionViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        params = json.dumps({"query": "select server,version from \"cmdb-aliyun_version\""})
        headers = {"Content-type": "application/json", "Authorization": "Basic ZWxhc3RpYzpNb29udG9uQDEyM0FiY18x"}
        conn = http.client.HTTPSConnection("elk.mtcc.moonton.net", 9200)
        conn.request('GET', '_sql?format=json', params, headers)
        response = conn.getresponse()
        code = response.status
        reason = response.reason
        res = json.loads(response.read())
        data = {}
        reslist = res['rows']
        for ser in reslist:
            lkey = ser[0]
            data[lkey] = ser[1]
        conn.close()

        return Response(data)
