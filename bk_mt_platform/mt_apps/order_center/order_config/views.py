from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.app_fw.exceptions import ParamError
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from .models import OrderConfig
from .pagination import OrderConfigSetPagination
from .serializers import OrderConfigSerializer
from ..order_config.utils.order_config_interface import OrderConfigInterface


class OrderConfigViewSet(ModelViewSet):
    queryset = OrderConfig.objects.values('id', 'biz_id', 'order_type', 'order_name', 'ding_api', 'ding_token',
                                          'process',
                                          "process__process_name", "process__process_type",
                                          "process__process_steps")
    serializer_class = OrderConfigSerializer
    pagination_class = OrderConfigSetPagination

    # 获取所有订单配置
    def filter_queryset(self, queryset):

        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            return queryset.filter(biz_id=biz_id)

        return OrderConfig.objects.all()


class AutoOrderConfig(GenericViewSet):
    # 自动创建订单配置
    @action(methods=['post'], detail=False, url_path='auto/create')
    def create_order_config_api(self, request):

        biz_id = request.data.get('biz_id', None)
        if biz_id is None or int(biz_id) < 0:
            raise ParamError(u"生成订单配置未传递biz_id或者biz_id为负值")
        try:
            with transaction.atomic():
                OrderConfigInterface.biz_register(int(biz_id))
        except Exception as e:
            raise e

        return Response([], status=status.HTTP_201_CREATED, headers='')
