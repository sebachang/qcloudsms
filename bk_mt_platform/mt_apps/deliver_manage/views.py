import xlrd
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response

from blueapps.account.decorators import login_exempt
from mt_apps.base.app_fw.exceptions import ParamError
from mt_apps.base.app_fw.viewsets import ModelViewSet
from mt_apps.order_center.deliver.utils.deliver_order_interface import DeliverOrderInterface
from mt_apps.order_center.order.utils.order_interface import OrderInterface
from mt_apps.order_center.order.views import OrderViewSet
from mt_apps.order_center.order_config.utils.order_config_interface import OrderConfigInterface
from mt_apps.order_center.order_config.utils.order_config_interface import OrderType
from .pagination import DeliverDetailSetPagination, ClearanceDetailSetPagination
from .serializers import *
from .serializers import DeliverDetailSerializer


# 平台操作
from ..base.system_config.config_define import get_system_config


class PlatformViewSet(ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    # 查询
    def filter_queryset(self, queryset):
        # print(self.request.get_full_path())
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取厂商配置时未传递biz_id或biz_id为负值")
            return queryset.filter(biz_id=biz_id)

        return queryset


# 主机操作(管理员)
class HostProfileViewSet(ModelViewSet):
    queryset = HostProfile.objects.all()
    serializer_class = HostProfileSerializer

    # 查询
    def filter_queryset(self, queryset):
        # print(self.request.get_full_path())
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取厂商配置时未传递biz_id或biz_id为负值")
            return queryset.filter(biz_id=biz_id)

        return queryset


# 平台主机关联表操作
class PlatformHostProfileMapViewSet(ModelViewSet):
    queryset = PlatformHostProfileMap.objects.all()
    serializer_class = PlatformHostProfileMapSerializer

    # 查询
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            id = self.request.GET.get('pid')
            if id is None or int(id) < 0:
                raise ParamError(u"获取厂商id时未传递pid或pid为负值")

            return queryset.filter(pid=id)
        return queryset

    # 新建
    def create(self, request, *args, **kwargs):
        res = request.data
        pid = res.get('pid')
        if pid is None or int(pid) < 0:
            raise ParamError(u"获取厂商id时未传递pid或pid为负值")
        hid_list = res.get('hid_list')
        if not isinstance(hid_list, list):
            raise ParamError(u"参数hid_list不是数组或者为空")
        try:
            with transaction.atomic():
                PlatformHostProfileMap.objects.filter(pid=pid).delete()
                if len(hid_list) != 0:
                    for x in hid_list:
                        PlatformHostProfileMap.objects.create(pid=pid, hid=x)
        except Exception as e:
            raise e

        return Response([], status=status.HTTP_201_CREATED, headers='')


# 机房操作
class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer

    # 查询
    def filter_queryset(self, queryset):
        # print(self.request.get_full_path())
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取厂商配置时未传递biz_id或biz_id为负值")
            return queryset.filter(biz_id=biz_id)

        return queryset


# 平台机房关联操作表
class PlatformCenterMapViewSet(ModelViewSet):
    queryset = PlatformCenterMap.objects.all()
    serializer_class = PlatformCenterMapSerializer

    # 查询
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            id = self.request.GET.get('pid')
            if id is None or int(id) < 0:
                raise ParamError(u"获取厂商id时未传递pid或pid为负值")
            return queryset.filter(pid=id)
        return queryset

    # 新建
    def create(self, request, *args, **kwargs):

        res = request.data
        pid = res.get('pid')
        if pid is None or int(pid) < 0:
            raise ParamError(u"获取厂商id时未传递pid或pid为负值")
        cid_list = res.get('cid_list')
        if not isinstance(cid_list, list):
            raise ParamError(u"参数cid_list不是数组")
        try:
            with transaction.atomic():
                PlatformCenterMap.objects.filter(pid=pid).delete()
                if len(cid_list) != 0:
                    for x in cid_list:
                        PlatformCenterMap.objects.create(pid=pid, cid=x)
        except Exception as e:
            raise e
        return Response([], status=status.HTTP_201_CREATED, headers="")


class DeliverOrderViewSet(OrderViewSet):
    serializer_class = DeliverOrderSerializer

    # 获取交付订单

    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            result = OrderConfigInterface.order_type_get_auditor(
                OrderType.deliver.name, biz_id)

            if self.request.user.__str__() in result:
                return queryset.filter(biz_id=biz_id, order_state=0, order_type=OrderType.deliver.name).order_by("-id")
            else:
                return queryset.none()


class MyDeliverOrderViewSet(OrderViewSet):
    serializer_class = DeliverOrderSerializer

    # 获取交付订单
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            return queryset.filter(submitter=self.request.user.__str__(),
                                   biz_id=biz_id, order_state=0, order_type=OrderType.deliver.name).order_by("-id")


class SearchDeliverDetailViewSet(ModelViewSet):
    queryset = DeliverDetail.objects.all()
    serializer_class = DeliverDetailSerializer
    pagination_class = DeliverDetailSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['$order_id__id',
                     '$bk_host_innerip', '$bk_host_outerip', '$isp', '$server_city', '$server_country', '$order_id__submitter']
    filterset_fields = ['biz_id']
    ordering_fields = ['-id']

    # 获取搜索交付订单
    def get_queryset(self):

        biz_id = self.request.GET.get('biz_id')
        if biz_id is None or int(biz_id) < 0:
            raise ParamError(u"获取搜索订单时未传递biz_id或biz_id为负值")
        start_time, end_time = self.request.GET.get(
            'start_time'), self.request.GET.get('end_time')

        queryset = DeliverDetail.objects.all()

        result = OrderConfigInterface.order_type_get_auditor(
            OrderType.deliver.name, biz_id)

        if self.request.user.__str__() not in result:
            return queryset.none()
        if start_time and end_time:
            return queryset.filter(create_time__range=(start_time, end_time))
        return queryset


class DeliverDetailViewSet(ModelViewSet):
    # 获取订单交付详情
    queryset = DeliverDetail.objects.all()
    serializer_class = DeliverDetailSerializer
    pagination_class = DeliverDetailSetPagination

    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            order_id = self.request.GET.get('order_id')
            if order_id is None or int(order_id) < 0:
                raise ParamError(u"获取订单审批流程时未传递order_id或order_id为负值")

            flag = self.request.GET.get('flag')

            if int(flag):
                return queryset.filter(order_id=order_id, detail_flag=0).order_by("create_time")

            result = OrderInterface.order_id_get_order_info(order_id)
            biz_id = result.get('biz_id')
            result = OrderConfigInterface.order_type_get_auditor(
                OrderType.deliver.name, biz_id)

            if self.request.user.__str__() in result:
                return queryset.filter(order_id=order_id).order_by("create_time")

            return queryset.filter(order_id=order_id, detail_flag=0).order_by("create_time")
        return queryset

    def create(self, request, *args, **kwargs):

        order_id = request.data.get('order', None)
        if not order_id:
            raise ParamError(u"未获取参数order_id")

        order_record = OrderInterface.order_id_get_order_info(order_id)

        deliver_order = DeliverOrderInterface.get_suborder(
            order_record.get('suborder'))

        try:
            arr = deliver_order.get('机房').split('-')
            if len(arr) == 3:
                if not request.data.get('server_country', None):
                    request.data['server_country'] = arr[1]
                if not request.data.get('server_city', None):
                    request.data['server_city'] = arr[2]
                if not request.data.get('isp', None):
                    request.data['isp'] = arr[0]
        except ...:
            pass

        return super(DeliverDetailViewSet, self).create(request, *args, **kwargs)


class DeliverDetailUploadViewSet(DeliverDetailViewSet):

    # 上传 excel 批量创建订单交付详情

    def create(self, request, *args, **kwargs):

        f = request.data.get('files', None)
        if not f:
            raise ParamError(u"未获取上传文件")
        if f.size > 500 << 10:
            raise ParamError(u"上传文件大于500kb")
        if f.name.split('.')[-1] not in ['xlsx', 'xls']:
            raise ParamError(u"上传文件类型错误")
        id = request.data.get('id', None)
        if not id:
            raise ParamError(u"未获取参数id")

        order_record = OrderInterface.order_id_get_order_info(id)
        biz_id = order_record.get('biz_id')

        deliver_order = DeliverOrderInterface.get_suborder(
            order_record.get('suborder'))

        wb = xlrd.open_workbook(filename=None, file_contents=f.read())
        table = wb.sheets()[0]
        rows = table.nrows
        cols = table.ncols
        key = table.row_values(0)
        num = 0
        try:
            with transaction.atomic():
                result = {}
                try:
                    arr = deliver_order.get('机房').split('-')
                    if len(arr) == 3:
                        result.setdefault('server_country', arr[1])
                        result.setdefault('server_city', arr[2])
                        result.setdefault('isp', arr[0])
                except ...:
                    pass
                for r in range(1, rows):
                    v = table.row_values(r)
                    for i in range(0, cols):
                        if v[i]:
                            result.update({key[i]: v[i]})
                    try:
                        data, created = DeliverDetail.objects.get_or_create(biz_id=int(biz_id), order_id=int(id),
                                                                            bk_host_innerip=result.get(
                                                                                'bk_host_innerip'))
                        if created:
                            for (k, v) in result.items():
                                if hasattr(data, k) and v:
                                    setattr(data, k, v)

                            data.save()
                            num += 1
                    except IntegrityError as e:
                        pass
        except Exception as e:
            raise e

        return Response({'created': num})


class ClearanceOrderViewSet(OrderViewSet):

    # 获取清退订单  待清退clearance_flag = 1 ，待确认clearance_flag = 2 ，已完成clearance_flag = 0
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            clearance_flag = self.request.GET.get('clearance_flag')
            if clearance_flag is None or int(clearance_flag) < 0:
                raise ParamError(u"获取订单时未传递clearance_flag或clearance_flag为负值")
            result = OrderConfigInterface.order_type_get_auditor(
                OrderType.clearance.name, biz_id)

            if self.request.user.__str__() in result:

                return queryset.filter(
                    biz_id=biz_id, order_state=0, order_type=OrderType.clearance.name,
                    clearancedetail__clearance_flag=clearance_flag
                ).distinct().order_by('-id')
            else:
                return queryset.none()


class ClearanceDetailViewSet(ModelViewSet):
    # 获取订单清退详情 待清退clearance_flag = 1 ，待确认clearance_flag = 2 ，已完成clearance_flag = 0
    queryset = ClearanceDetail.objects.all()
    serializer_class = ClearanceDetailSerializer
    pagination_class = ClearanceDetailSetPagination

    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            order_id = self.request.GET.get('order_id')
            if order_id is None or int(order_id) < 0:
                raise ParamError(u"获取订单审批流程时未传递order_id或order_id为负值")

            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            clearance_flag = self.request.GET.get('clearance_flag')
            if clearance_flag is None or int(clearance_flag) < 0:
                raise ParamError(u"获取订单时未传递clearance_flag或clearance_flag为负值")

            result = OrderConfigInterface.order_type_get_auditor(
                OrderType.clearance.name, biz_id)

            if self.request.user.__str__() in result:
                if int(clearance_flag) == 4:
                    return queryset.filter(biz_id=biz_id).order_by("-id")
                return queryset.filter(order_id=order_id, clearance_flag=clearance_flag).order_by("create_time")

            return queryset.filter(order_id=0).order_by('-id')

        return queryset


class SearchClearanceDetailViewSet(ModelViewSet):
    # 搜索清退详情
    serializer_class = ClearanceDetailSerializer
    pagination_class = ClearanceDetailSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['$order_id__id', '$remove_id',
                     '$bk_host_innerip', '$bk_host_outerip', '$isp', '$server_city', '$server_country']
    filterset_fields = ['biz_id']
    ordering_fields = ['-id']

    def get_queryset(self):

        if self.request.method == 'GET':

            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取搜索订单时未传递biz_id或biz_id为负值")

            start_time, end_time = self.request.GET.get(
                'start_time'), self.request.GET.get('end_time')

            queryset = ClearanceDetail.objects.all()

            result = OrderConfigInterface.order_type_get_auditor(
                OrderType.clearance.name, biz_id)

            if self.request.user.__str__() not in result:
                return queryset.none()

            if start_time and end_time:
                return queryset.filter(clearance_create_time__range=(start_time, end_time))

            return queryset


@login_exempt
@csrf_exempt
def update_deliver_host_passwd(request):
    biz_id = request.GET.get('biz_id')
    order_id = request.POST.get('order_id')
    token = request.POST.get("token")
    ip = request.POST.get('ip')
    passwd = request.POST.get('passwd')

    config_token = get_system_config(biz_id, "deliver_api_token")

    if biz_id is None or order_id is None or ip is None or passwd is None:
        return JsonResponse(data={"message": u"参数biz_id, order_id, ip, passwd不能为空", "code": -1})

    if token != config_token:
        return JsonResponse(data={"message": u"token错误", "code": -1})

    try:
        record = DeliverDetail.objects.get(biz_id=biz_id, order_id=order_id, bk_host_innerip=ip)
        record.password = passwd
        record.save()
    except DeliverDetail.DoesNotExist as e:
        return JsonResponse(data={"message": u"找不到这个IP", "code": -1})
    return JsonResponse(data={"code": 0})

update_deliver_host_passwd.csrf_exempt = True
update_deliver_host_passwd.login_exempt = True
