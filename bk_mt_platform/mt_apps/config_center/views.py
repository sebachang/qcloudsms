from django.http import HttpResponse

from blueapps.account.decorators import login_exempt
from mt_apps.base.app_fw.decorators import filter_biz_id
from mt_apps.base.app_fw.viewsets import ModelViewSet
from mt_apps.process_manage.utils import *
from .serializers import *

job_uuid = 'bfc0a2ea-71a7-40c0-b40a-7334798d4afc'


class ConfigTemplateViewSet(ModelViewSet):
    queryset = ConfigTemplate.objects.all()
    serializer_class = ConfigTemplateSerializer

    @filter_biz_id
    def filter_queryset(self, queryset):
        return queryset


class ConfigKVViewSet(ModelViewSet):
    queryset = ConfigKV.objects.all()
    serializer_class = ConfigKVSerializer

    @filter_biz_id
    def filter_queryset(self, queryset):
        return queryset


@login_exempt
def render_template(request, pk=None):
    record = ConfigTemplate.objects.get(pk=pk)
    data = {"ServerIP": get_client_ip(request)}
    for k, v in request.GET.items():
        data[k] = v
    from mt_apps.config_center.impls import render_config

    return HttpResponse(render_config(record.biz_id, record.name, data), 'text/plain')
