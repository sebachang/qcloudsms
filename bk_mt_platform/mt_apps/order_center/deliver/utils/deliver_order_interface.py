import json
from base64 import b64encode

from mt_apps.deliver_manage.models import DeliverDetail
from ..models import DeliverOrder
from ...order.views import DateEncoder
from ....order_center.order.utils.order_interface import OrderInterface
from ....order_center.order_config.utils.order_config_interface import OrderType, OrderConfigInterface
from ....order_center.process_config.utils.process_config_interface import ProcessConfigInterface


class DeliverOrderInterface(OrderInterface, OrderConfigInterface, ProcessConfigInterface):
    order_type = OrderType.deliver.name

    @classmethod
    def create_suborder(cls, **kwargs):
        result = DeliverOrder.objects.create(
            platform_id=kwargs.get('platform_id'), host_id=kwargs.get('host_id'),
            center_id=kwargs.get('center_id'), vlan=kwargs.get('vlan'),
            system=kwargs.get('system'), amount=kwargs.get('amount'),
            desc=kwargs.get('desc'), remark=kwargs.get('remark'),
        )
        return result.id

    @classmethod
    def get_suborder(cls, suborder_id):
        result = DeliverOrder.objects.all().filter(id=suborder_id).values(
            'platform__platform_name', 'center__center_name', 'host__host_name', 'host__cpu',
            'host__mem', 'host__disk', 'host__sdisk', 'host__ssd', 'host__net', 'host__price',
            'system', 'amount', 'desc', 'remark'
        ).first()

        data = {
            "机型": result['host__host_name'],
            "平台": result['platform__platform_name'],
            "机房": result['center__center_name'],
            "配置": ', '.join(["核心(" + result['host__cpu'] + ")",
                             "内存(" + result['host__mem'] + ")",
                             "系统盘(" + result['host__sdisk'] + ")",
                             "硬盘(" + result['host__disk'] + ")",
                             "固态硬盘(" + result['host__ssd'] + ")",
                             "带宽(" + result['host__net'], ]) + ")",
            "系统": result['system'],
            "单价": str(result['host__price']),
            "数量": str(result['amount']),
            "原因": result['desc'],
            "备注": result['remark'],
        }
        return data

    @classmethod
    def script_param(cls, order_id):
        order = super(DeliverOrderInterface,
                      cls).order_id_get_order_info(order_id)
        sub_order = DeliverOrder.objects.all().filter(id=order['suborder']).values(
            'platform_id__platform_name', 'center_id__center_name', 'host__host_name', 'host__cpu',
            'host__mem', 'host__disk', 'host__sdisk', 'host__ssd', 'host__net', 'host__price',
            'system', 'amount', 'desc', 'remark'
        ).first()

        detail = DeliverDetail.objects.values().filter(order_id=order_id)

        param = {
            "order": order,
            "sub_order": sub_order,
            "detail": list(detail)
        }

        param = json.dumps(param, cls=DateEncoder).encode()
        return b64encode(param).decode()

    @classmethod
    def ding_massage(cls, **order_info):
        sub_data = ''
        for k, v in cls.get_suborder(order_info['suborder']).items():
            sub_data = sub_data + ">" + k + ": " + v + "\n\n"

        return sub_data
