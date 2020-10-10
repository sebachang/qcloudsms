from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.api.components.cmdb import CmdbAPI
from mt_apps.base.app_fw.exceptions import ParamError
from mt_apps.base.app_fw.viewsets import GenericViewSet
from mt_apps.base.system_config.config_define import get_system_config
from mt_apps.deliver_manage.models import ClearanceDetail


class CmdbClearanceViewSet(GenericViewSet):

    @action(methods=['get'], detail=False, url_path='cmdb/clearance')
    def get_cmdb_clearance(self, request):
        if request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            page = self.request.GET.get('page')
            if page is None or int(page) < 0:
                raise ParamError(u"获取订单时未传递page或page为负值")

            result = CmdbAPI.search_clearance_host(self.request, get_system_config(
                biz_id, 'search_clearance_node'), (int(page) - 1) * 10)

            count = result.get('data', {}).get('count', 0)

            attributes = CmdbAPI.search_object_attribute(request, "host")
            enum_fields = ['isp', 'server_country']
            name_dict = {}
            for obj in attributes['data']:
                if obj['bk_property_id'] in enum_fields:
                    for opt in obj['option']:
                        name_dict[obj['bk_property_id'] +
                                  ':' + opt['id']] = opt['name']
            print(name_dict)
            all_fields = ['bk_host_id', 'remove_id', 'bk_host_innerip', 'bk_host_outerip', 'bk_comment', 'bk_host_outerip_2', 'password', 'disk_type', 'server_city', 'bandwidth', 'price', 'server_country',
                          'sl_account', 'ssh_ip', 'isp', 'bk_host_name', 'bk_os_type', 'bk_os_name', 'bk_os_version', 'bk_os_bit', 'bk_cpu', 'bk_cpu_mhz', 'bk_cpu_module', 'bk_mem', 'bk_disk', 'bk_mac', 'bk_outer_mac', 'create_time', ]

            if count != 0:
                data1 = []
                for x in result.get('data', {}).get('info'):
                    result_host = x.get('host', {})
                    data2 = {}
                    if not result_host.get('remove_id', ''):
                        continue
                    if ClearanceDetail.objects.filter(remove_id=result_host.get('remove_id', ''),
                                                      bk_host_id=result_host['bk_host_id'], biz_id=biz_id).count() != 0:
                        continue

                    data2['biz_id'] = biz_id

                    for f in all_fields:
                        if f in enum_fields:
                            data2[f] = name_dict.get(
                                f+':'+result_host.get(f, ''), '')
                        else:
                            data2[f] = result_host.get(f, '')

                    data1.append(data2)

                # data = {
                #     'count': count,
                #     'data': data1
                # }
                # print(data)
                return Response(data1)

            return Response({})
