# -*- coding: utf-8 -*-
from mt_apps.nginx.models import ConfigModel, VhostModel, ClusterModel
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from rest_framework import viewsets
from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.app_fw.error_code import *
from mt_apps.base.system_config.config_define import get_system_config
from .constants import job_uuid
from .utils import *
from .script import *
import json
import base64
from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from blueapps.account.decorators import login_exempt
from django.http import HttpResponse, FileResponse
from rest_framework.renderers import JSONRenderer

from .serializers import ConfigModelSerializer, ClusterModelSerializer, VhostModelSerializer
from rest_framework import serializers
from rest_framework.response import Response
from mt_apps.certificate.serializers import CertSerializer

from mt_apps.nginx.template import GetNginxBaseConfig, GetNginxVhost80Config, GetNginxVhostBaseConfig, \
    GetNginxVhostProxyConfig
from mt_apps.certificate.models import CertModel, DomainModel


class ClusterViewSet(ModelViewSet):
    queryset = ClusterModel.objects.all()
    serializer_class = ClusterModelSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bk_biz']
    search_fields = ['name']
    ordering_fields = ['id']


class ConfigViewSet(ModelViewSet):
    queryset = ConfigModel.objects.all()
    serializer_class = ConfigModelSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bk_biz']
    search_fields = ['name']
    ordering_fields = ['id']


class VhostViewSet(ModelViewSet):
    queryset = VhostModel.objects.all()
    serializer_class = VhostModelSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bk_biz', 'config']
    ordering_fields = ['id']


class ConfigListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        res = []
        cluster_id = ClusterModel.objects.values('config')
        config = [cluster['config'] for cluster in cluster_id]
        from django.db.models import Q
        queryset = ConfigModel.objects.filter(~Q(id__in=config))
        for obj in queryset:
            res.append({'id': obj.id, 'name': obj.name})

        return Response(res)

    def retrieve(self, request, *args, **kwargs):
        res = []

        if 'pk' in self.kwargs:
            if self.kwargs["pk"] != '':
                try:
                    cluster_id = ClusterModel.objects.values('config')
                    config = [cluster['config'] for cluster in cluster_id]
                    from django.db.models import Q
                    queryset = ConfigModel.objects.filter(Q(id=int(self.kwargs["pk"])) | ~Q(id__in=config))
                    for obj in queryset:
                        res.append({'id': obj.id, 'name': obj.name})
                except:
                    pass

        return Response(res)


class VhostListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        res = []
        queryset = VhostModel.objects.all()
        for obj in queryset:
            res.append({'id': obj.id, 'name': obj.domain.name + ":" + str(obj.port)})

        return Response(res)


class TemplateBaseViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        res = {"config": None}
        certificate = {"exist": False, "domain": "", "name": ""}

        paths = {"log_dir": "/data/applog/openresty",
                 "work_dir": "/data/app/openresty-moonton",
                 "module_dir": "/data/app/openresty-moonton/nginx/conf/modules",
                 "cert_dir": "/data/app/openresty-moonton/nginx/conf/ssl",
                 "vhost_dir": "/data/app/openresty-moonton/nginx/conf/vhost"}

        data = request.data
        if 'cert' in data.keys() and 'cluster' in data.keys():
            cert = data['cert']
            cluster = data['cluster']

            if cert:
                try:
                    certObj = CertModel.objects.get(id=cert)

                    certificate['exist'] = True
                    certificate['domain'] = certObj.domain.lstrip('*.')
                    if certObj.name:
                        certificate['name'] = certObj.name
                    else:
                        certificate['name'] = certificate['domain']
                except:
                    pass

            if cluster:
                try:
                    clusterObj = ClusterModel.objects.get(id=cluster)
                    paths['log_dir'] = clusterObj.log_path.rstrip('/')
                    paths['work_dir'] = clusterObj.path.rstrip('/')
                    paths['module_dir'] = clusterObj.module_path.rstrip('/')
                    paths['cert_dir'] = clusterObj.cert_path.rstrip('/')
                    paths['vhost_dir'] = clusterObj.vhost_path.rstrip('/')
                except:
                    pass

        nginx_config = GetNginxBaseConfig(certificate, paths)
        res = {"config": nginx_config}

        return Response(res)


class TemplateVhostViewSet(mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def update(self, request, *args, **kwargs):
        res = {"config": None}
        certificate = {"exist": False, "domain": "", "name": ""}
        paths = {"log_dir": "/data/applog/openresty",
                 "work_dir": "/data/app/openresty-moonton",
                 "module_dir": "/data/app/openresty-moonton/nginx/conf/modules",
                 "cert_dir": "/data/app/openresty-moonton/nginx/conf/ssl",
                 "vhost_dir": "/data/app/openresty-moonton/nginx/conf/vhost"}

        if 'pk' in self.kwargs:
            if self.kwargs["pk"] != '':
                id = int(self.kwargs["pk"])
                data = request.data
                cluster = data['cluster']
                cert = data['cert']

                data['domain_data'] = DomainModel.objects.values('name').get(id=data['domain'])

                if cert:
                    try:
                        certObj = CertModel.objects.get(id=cert)

                        certificate['exist'] = True
                        certificate['domain'] = certObj.domain.lstrip('*.')
                        if certObj.name:
                            certificate['name'] = certObj.name
                        else:
                            certificate['name'] = certificate['domain']
                    except:
                        pass

                if cluster:
                    try:
                        clusterObj = ClusterModel.objects.get(id=cluster)
                        paths['log_dir'] = clusterObj.log_path.rstrip('/')
                        paths['work_dir'] = clusterObj.path.rstrip('/')
                        paths['module_dir'] = clusterObj.module_path.rstrip('/')
                        paths['cert_dir'] = clusterObj.cert_path.rstrip('/')
                        paths['vhost_dir'] = clusterObj.vhost_path.rstrip('/')
                    except:
                        pass

                if id == 1:
                    res["config"] = GetNginxVhostBaseConfig(data, paths, certificate)

                if id == 2:
                    res["config"] = GetNginxVhostProxyConfig(data, paths, certificate)

                if id == 3:
                    res["config"] = GetNginxVhost80Config(data, paths)

        return Response(res)


class InstanceViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def retrieve(self, request, *args, **kwargs):
        res = []

        if 'pk' in self.kwargs:
            if self.kwargs["pk"] != '':
                try:
                    cluster = ClusterModel.objects.get(id=int(self.kwargs["pk"]))
                    cmd = "echo -n '!!!!!' ;[ -d {work_dir} ] || (echo '进程尚未部署' && exit 1); \
                       [ -f {work_dir}/{conf_path} ] && md5sum {work_dir}/{conf_path} | awk '{{print $1}}' || echo '配置文件不存在'; \
                       [ -f {work_dir}/{pid_path} ] && pid=$(cat {work_dir}/{pid_path}) && ps -p $pid >/dev/null && echo '运行中' || echo '已停止'".format(
                        conf_path='nginx/conf/nginx.conf',
                        work_dir=cluster.path, pid_path='openresty.pid')
                    hosts = json.loads(cluster.hosts)
                    res = run_bk_cmd(request, biz_id=cluster.bk_biz, hosts=hosts, user='root', cmd=cmd)
                except:
                    pass

        return Response(res)


class JobViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        res = None

        bk_biz = int(request.GET.get("bk_biz", default=0))
        job_id = int(request.GET.get("job_id", default=0))

        if bk_biz != 0 and job_id != 0:
            try:
                obj = get_job_status(request, bk_biz, job_id)
                if obj["data"]["is_finished"]:
                    res = get_job_log(request, job_id, bk_biz)
            except:
                pass

        return Response(res)


class OperationViewSet(mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def update(self, request, *args, **kwargs):
        res = None
        id = int(self.kwargs["pk"])
        data = request.data
        action = data['action']
        hosts = []
        for host in data['hosts']:
            if 'sttaus' in host.keys():
                del host['status']
            hosts.append(host)

        record = ClusterModel.objects.get(id=id)

        if record is None:
            raise CommonLogicError({
                'code': EC_OBJECT_NOT_EXIST,
                'message': u'找不到这个实例'
            })
        cmd = None
        work_dir = record.path
        if action:
            if action == 'publish':
                pack_url = get_system_config(record.bk_biz, 'process_pack_url')
                header = get_system_config(record.bk_biz, 'process_header')

                pack_url = pack_url + '/' if not pack_url.endswith('/') else pack_url
                full_pack_name = pack_url + f'{record.bk_biz}/' + record.package
                if header.strip() != '':
                    header = '-H "%s"' % header
                else:
                    header = '-H "Referer: %s"' % request.META['HTTP_HOST']
                cmd = "tmp_path=$(mktemp -d) && " \
                      "curl {header} -o $tmp_path/{pack_name} {full_pack_name} " \
                      "&& mkdir -p {work_dir} " \
                      "&& cd {work_dir} && tar xf $tmp_path/{pack_name} && rm -f $tmp_path/{pack_name}"
                cmd = cmd.format(
                    header=header,
                    full_pack_name=full_pack_name,
                    pack_name=record.package,
                    work_dir=record.path,
                    url=pack_url,
                )
                # 由于执行发布命令时，进程所在的目录尚未创建，所以需要找个可以进去的临时目录
                work_dir = '/tmp'
            elif action in ['pull_config', 'pull_config_restart', 'pull_config_reload']:
                config = record.config
                nginx_base_config = config.content

                vhost = config.getVhosts()

                cmd = NginxBasePushScript.format(CONF_DIR=record.conf_path.rstrip('/'), NGINX_CONFIG=base64.b64encode(
                    nginx_base_config.encode('utf-8')).decode("utf-8"))

                if config.cert:
                    certData = config.getCertData()
                    domain = certData['domain'].lstrip('*.')
                    name = certData['name']
                    if not name:
                        name = domain
                    cmd = cmd + '\n' + CertPushScript.format(CERT_PATH=record.cert_path.rstrip('/') + '/' + domain,
                                                             DOMAIN_NAME=name,
                                                             CERT_KEY=base64.b64encode(
                                                                 certData['key'].encode('utf-8')).decode("utf-8"),
                                                             CERT_CRT=base64.b64encode(
                                                                 certData['crt'].encode('utf-8')).decode("utf-8"))

                if len(vhost) > 0:
                    vhost_configs = ''
                    for host in vhost:
                        if host['cert']:
                            vhostCertData = CertSerializer(CertModel.objects.get(id=host['cert']), many=False).data
                            domain = vhostCertData['domain'].lstrip('*.')
                            name = vhostCertData['name']
                            if not name:
                                name = domain
                            cmd = cmd + '\n' + CertPushScript.format(
                                CERT_PATH=record.cert_path.rstrip('/') + '/' + domain,
                                DOMAIN_NAME=name,
                                CERT_KEY=base64.b64encode(
                                    vhostCertData['key'].encode('utf-8')).decode("utf-8"),
                                CERT_CRT=base64.b64encode(
                                    vhostCertData['crt'].encode('utf-8')).decode("utf-8"))

                        host_domain = host['domain_data']['name']
                        if len(host_domain.split(':')) == 1:
                            host_domain = host_domain + ':' + str(host['port'])
                        host_content = host['content']
                        vhost_configs = vhost_configs + host_domain + '@' + base64.b64encode(
                            host_content.encode('utf-8')).decode("utf-8") + ' '

                    cmd = cmd + '\n' + NginxVhostPushScript.format(VHOST_DIR=record.vhost_path.rstrip('/'),
                                                                   NGINX_CONFIG=base64.b64encode(
                                                                       vhost_configs.encode('utf-8')).decode("utf-8"))

                if action == 'pull_config_restart':
                    cmd = cmd + '\n' + 'bash -x {work_dir}/restart.sh {work_dir} {config_dir} {vhost_dir} {cert_dir} {log_dir} {module_dir}'.format(
                        work_dir=record.path, config_dir=record.conf_path, vhost_dir=record.vhost_path,
                        cert_dir=record.cert_path, log_dir=record.log_path, module_dir=record.module_path)

                if action == 'pull_config_reload':
                    cmd = cmd + '\n' + 'bash -x {work_dir}/reload.sh {work_dir} {config_dir} {vhost_dir} {cert_dir} {log_dir} {module_dir}'.format(
                        work_dir=record.path, config_dir=record.conf_path, vhost_dir=record.vhost_path,
                        cert_dir=record.cert_path, log_dir=record.log_path, module_dir=record.module_path)

            elif action == 'start':
                cmd = 'bash -x {work_dir}/start.sh {work_dir} {config_dir} {vhost_dir} {cert_dir} {log_dir} {module_dir}'.format(
                    work_dir=record.path, config_dir=record.conf_path, vhost_dir=record.vhost_path,
                    cert_dir=record.cert_path, log_dir=record.log_path, module_dir=record.module_path)
            elif action == 'stop':
                cmd = 'bash -x {work_dir}/stop.sh {work_dir} {config_dir} {vhost_dir} {cert_dir} {log_dir} {module_dir}'.format(
                    work_dir=record.path, config_dir=record.conf_path, vhost_dir=record.vhost_path,
                    cert_dir=record.cert_path, log_dir=record.log_path, module_dir=record.module_path)
            elif action == 'reload':
                cmd = 'bash -x {work_dir}/reload.sh {work_dir} {config_dir} {vhost_dir} {cert_dir} {log_dir} {module_dir}'.format(
                    work_dir=record.path, config_dir=record.conf_path, vhost_dir=record.vhost_path,
                    cert_dir=record.cert_path, log_dir=record.log_path, module_dir=record.module_path)
            elif action == 'restart':
                cmd = 'bash -x {work_dir}/restart.sh {work_dir} {config_dir} {vhost_dir} {cert_dir} {log_dir} {module_dir}'.format(
                    work_dir=record.path, config_dir=record.conf_path, vhost_dir=record.vhost_path,
                    cert_dir=record.cert_path, log_dir=record.log_path, module_dir=record.module_path)
            else:
                raise CommonLogicError({
                    'code': EC_OPERATION_NOT_SUPPORTED,
                    'message': u'当前进程不支持这个操作: %s' % action
                })

        result = run_cmd(request, biz_id=record.bk_biz, host=json.dumps(hosts), user='root', cmd=cmd,
                         work_dir=work_dir,
                         timeout=600,
                         task_name="%s %s" % (action, str(record)),
                         job_uuid=job_uuid)
        return Response(result)


@login_exempt
def get_by_process_name(request, biz_id=None):
    res = []
    records = ClusterModel.objects.filter(bk_biz=biz_id)
    for obj in records:
        for host in json.loads(obj.hosts):
            data = {"id": obj.id, "biz_id": obj.bk_biz, "machine": host['ip'],
                    "machine_full": str(host['bk_cloud_id']) + ':' + host['ip'],
                    "desc": "nginx-" + obj.name + '-' + host['ip'], "work_dir": obj.path, "pid_path": "openresty.pid"}
            res.append(data)

    return HttpResponse(JSONRenderer().render(res))
