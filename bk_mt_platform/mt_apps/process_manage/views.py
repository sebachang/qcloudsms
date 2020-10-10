import urllib.parse

import boto3
import requests
from botocore.exceptions import ClientError
from django.http import HttpResponse, FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from blueapps.account.decorators import login_exempt
from mt_apps.base.app_fw.decorators import need_biz_id
from mt_apps.base.app_fw.error_code import *
from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.system_config.config_define import get_system_config
from mt_apps.base.utils.util_site import get_download_site
from .constants import job_uuid
from .pagination import StandardResultsSetPagination
from .serializers import *
from .utils import *


class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

    def filter_queryset(self, queryset):
        if self.request.method == 'GET' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise CommonLogicError(
                    {'code': 10001, 'message': u"获取Process时未传递biz_id或biz_id为负值"})
            return queryset.filter(biz_id=biz_id)

        return queryset


class InstanceViewSet(ModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['desc', 'machine', 'process__name']
    filter_fields = ['id', 'biz_id']
    ordering_fields = ['id', 'create_time']

    # def filter_queryset(self, queryset):
    #     if self.request.method == 'GET' or self.request.method == 'PUT' or self.request.method == 'DELETE':
    #         biz_id = self.request.GET.get('biz_id')
    #         if biz_id is None or int(biz_id) < 0:
    #             raise CommonLogicError(
    #                 {'code': 10001, 'message': u"获取instance时未传递biz_id或biz_id为负值"})
    #         return queryset.filter(biz_id=biz_id)
    #
    #     return queryset

    @action(methods=['get'], detail=True, url_path='')
    def get_instance_status(self, request, pk=None):
        record = Instance.objects.get(pk=pk)
        cmd = "echo -n '!!!!!' ;[ -d {work_dir} ] || (echo '进程尚未部署' && exit 1); \
         [ -f {work_dir}/{conf_path} ] && md5sum {work_dir}/{conf_path} | awk '{{print $1}}' || echo '配置文件不存在'; \
         [ -f {work_dir}/{pid_path} ] && pid=$(cat {work_dir}/{pid_path}) && ps -p $pid >/dev/null && echo '运行中' || echo '已停止'".format(
            conf_path=record.process.conf_path,
            work_dir=record.work_dir, pid_path=record.pid_path)
        res = run_bk_cmd(request, biz_id=record.biz_id, host=record.machine, user=record.launch_user, cmd=cmd)
        print(res)
        return Response(res)


class InstanceOperationViewSet(GenericViewSet):

    @action(methods=['post'], detail=True, url_path=r'(?P<action>\w+)')
    def run_operation(self, request, pk=None, action=None):
        record = Instance.objects.get(pk=pk)
        if record is None:
            raise CommonLogicError({
                'code': EC_OBJECT_NOT_EXIST,
                'message': u'找不到这个实例'
            })
        attr = "%s_cmd" % action
        cmd = None
        work_dir = None
        if not hasattr(record.process, attr) or getattr(record.process, attr).strip() == '':
            server_ip = record.get_server_ip()
            pathname = f'mt_apps/config_center/template/render/{record.process.template_id}/?ServerIP={server_ip}'
            if action == 'publish':
                pack_url = get_system_config(record.biz_id, 'process_pack_url')
                header = get_system_config(record.biz_id, 'process_header')

                pack_url = pack_url + '/' if not pack_url.endswith('/') else pack_url
                full_pack_name = pack_url + f'{record.biz_id}/' + record.process.pack_name
                if header.strip() != '':
                    header = '-H "%s"' % header
                else:
                    header = '-H "Referer: %s"' % request.META['HTTP_HOST']
                cmd = "tmp_path=$(mktemp -d) && " \
                      "curl {header} -o $tmp_path/{pack_name} {full_pack_name} " \
                      "&& mkdir -p {work_dir} " \
                      "&& cd {work_dir} && tar xf $tmp_path/{pack_name} && rm -f $tmp_path/{pack_name}" \
                      "&& curl \"{config_url}\" -o {conf_path}"
                cmd = cmd.format(
                    header=header,
                    full_pack_name=full_pack_name,
                    pack_name=record.process.pack_name,
                    work_dir=record.work_dir,
                    url=pack_url,
                    config_url=urllib.parse.urljoin(get_download_site(''), pathname),
                    conf_path=record.process.conf_path
                )
                # 由于执行发布命令时，进程所在的目录尚未创建，所以需要找个可以进去的临时目录
                work_dir = '/tmp'
            elif action == 'pull_config' or action == 'pull_config_restart' or action == 'pull_config_reload':
                cmd = 'curl "{config_url}" -o {conf_path}'.format(
                    config_url=urllib.parse.urljoin(get_download_site(''), pathname),
                    conf_path=record.process.conf_path)

                work_dir = record.work_dir
                if action == 'pull_config_restart':
                    cmd += f"&& PATH=$PATH:{work_dir} {getattr(record.process, 'restart_cmd')}"
                elif action == 'pull_config_reload':
                    cmd += f"&& PATH=$PATH:{work_dir} {getattr(record.process, 'reload_cmd')}"
                pass
            else:
                raise CommonLogicError({
                    'code': EC_OPERATION_NOT_SUPPORTED,
                    'message': u'当前进程不支持这个操作: %s' % action
                })

        if work_dir is None:
            work_dir = record.work_dir

        if cmd is None:
            cmd = getattr(record.process, attr)
            if not cmd.startswith('/'):
                if not cmd.startswith('./'):
                    cmd = ("export PATH=$PATH:%s;" + cmd) % work_dir

        result = run_cmd(request, biz_id=record.biz_id, host=record.machine, user=record.launch_user, cmd=cmd,
                         work_dir=work_dir,
                         timeout=record.operate_timeout,
                         task_name="%s %s" % (action, str(record)),
                         job_uuid=job_uuid)
        return Response(result)

    @need_biz_id
    @action(methods=['get'], detail=False, url_path=r'job_status/(?P<job_id>\d+)')
    def job_status(self, request, job_id=None, biz_id=None):
        result = get_job_status(request, biz_id, job_id)
        return Response(result['data'])


def get_s3_client(biz_id):
    aws_access_key = get_system_config(biz_id, 'aws_access_key')
    aws_secret_key = get_system_config(biz_id, 'aws_secret_key')

    return boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


class ProcessGenericViewSet(GenericViewSet):
    serializer_class = serializers.Serializer

    @need_biz_id
    @action(methods=['get'], detail=False, url_path=r'job_log/(?P<id>\d+)')
    def get_job_log(self, request, id=None, biz_id=None):
        manager = BK_TaskManager(request)
        res = manager.get_task_log(biz_id, id)
        return Response(res)

    @need_biz_id
    @action(methods=['get', 'post'], detail=False, url_path=r'package')
    def handle_package(self, request, biz_id=None):
        if request.method == 'GET':

            raw_url = get_system_config(biz_id, 'process_pack_url')
            header = get_system_config(biz_id, 'process_header')
            headers = {}
            if header != '':
                a = [p.strip() for p in header.split(':')]
                headers[a[0]] = a[1]

            from urllib.parse import urlparse
            u = urlparse(raw_url)
            request_url = u.scheme + "://" + u.netloc + "/"
            prefix = u.path[1:] + f'{biz_id}/'

            res = requests.get(request_url, params={'prefix': prefix}, headers=headers)
            return Response({'content': res.content})
        elif request.method == 'POST':

            raw_url = get_system_config(biz_id, 'process_pack_url')
            bucket_name = get_system_config(biz_id, 'aws_s3_bucket')

            from urllib.parse import urlparse
            u = urlparse(raw_url)

            key = u.path[1:] if u.path.endswith('/') else u.path[1:]
            key += f'{biz_id}/' + request.POST.get('key')

            client = get_s3_client(biz_id)
            try:
                client.upload_fileobj(request.FILES.get('file'), bucket_name, key)
                return Response({'content': ''})
            except ClientError as e:
                raise CommonLogicError({'code': -101, 'message': e.message})

    @need_biz_id
    @action(methods=['delete'], detail=False, url_path=r'package/(?P<file>[^/]+)')
    def handle_package_item(self, request, file=None, biz_id=None):
        raw_url = get_system_config(biz_id, 'process_pack_url')
        bucket_name = get_system_config(biz_id, 'aws_s3_bucket')

        from urllib.parse import urlparse
        u = urlparse(raw_url)
        key = u.path[1:].rstrip('/') + f'/{biz_id}/{file}'

        client = get_s3_client(biz_id)
        try:
            client.delete_object(Bucket=bucket_name, Key=key)
        except ClientError as e:
            raise CommonLogicError({'code': 10001, 'message': e.message})

        return Response({})

    @need_biz_id
    @action(methods=['get'], detail=False, url_path=r'download/(?P<file>[^/]+)')
    def download_package(self, request, file=None, biz_id=None):

        raw_url = get_system_config(biz_id, 'process_pack_url')
        bucket_name = get_system_config(biz_id, 'aws_s3_bucket')

        from urllib.parse import urlparse
        u = urlparse(raw_url)
        key = u.path[1:].rstrip('/') + f'/{biz_id}/{file}'

        client = get_s3_client(biz_id)
        try:
            url = client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key},
                                                ExpiresIn=3600)
            return Response({'code': 0, 'data': url})
        except ClientError as e:
            raise CommonLogicError({'code': 10001, 'message': e.message})


@login_exempt
def get_by_process(request, pk=None):
    records = Instance.objects.filter(process_id=pk)

    i = TrivialInstanceSerializer(records, many=True)
    return HttpResponse(JSONRenderer().render(i.data))


@login_exempt
def get_by_process_name(request, biz_id=None, name=None):
    records = Instance.objects.filter(biz_id=biz_id, process__name__icontains=name)

    i = TrivialInstanceSerializer(records, many=True)
    return HttpResponse(JSONRenderer().render(i.data))


