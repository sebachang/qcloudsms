from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.app_fw.exceptions import ParamError
from mt_apps.base.app_fw.viewsets import GenericViewSet
from mt_apps.deliver_manage.models import Platform


class OrderPlatformHostViewSet(GenericViewSet):

    @action(methods=['get'], detail=False, url_path='platform/host')
    def info(self, request):

        id = self.request.GET.get('pid')
        if id is None:
            raise ParamError(u"获取厂商id时未传递pid或pid为负值")
        pid_list = request.GET.getlist("pid")
        if not isinstance(pid_list, list):
            raise ParamError(u"参数pid_list不是数组")
        data = {}
        for p in pid_list:
            data1 = []
            sql = 'SELECT * FROM %s WHERE ' \
                  'id IN ( SELECT %s FROM %s WHERE pid = %s and state = %d)' \
                  % ('deliver_manage_host', 'hid', 'deliver_manage_platform_host_map', p, 0)
            for x in Platform.objects.raw(sql):
                data1.append({"id": x.id, "host_name": x.host_name, "cpu": x.cpu, "mem": x.mem,
                              "sdisk": x.sdisk, "disk": x.disk, "ssd": x.ssd, "net": x.net, "price": x.price})
            data[p] = data1
        return Response(data)


class OrderPlatformCenterViewSet(GenericViewSet):

    @action(methods=['get'], detail=False, url_path='platform/center')
    def info(self, request):
        if self.request.method == 'GET':
            id = self.request.GET.get('pid')
            if id is None:
                raise ParamError(u"获取厂商id时未传递pid或pid为负值")
            pid_list = request.GET.getlist("pid")
            if not isinstance(pid_list, list):
                raise ParamError(u"参数pid_list不是数组")
            data = {}
            for p in pid_list:
                data1 = []
                sql = 'SELECT * FROM %s WHERE ' \
                      'id IN ( SELECT %s FROM %s WHERE pid = %s and state = %d)' \
                      % ('deliver_manage_center', 'cid', 'deliver_manage_platform_center_map', p, 0)
                for x in Platform.objects.raw(sql):
                    data1.append({"id": x.id, "center_name": x.center_name, })
                data[p] = data1
            return Response(data)
