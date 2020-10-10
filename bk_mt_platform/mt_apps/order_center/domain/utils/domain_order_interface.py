import json
from base64 import b64encode

from ..models import DomainOrder
from ...order.views import DateEncoder
from ....order_center.order.utils.order_interface import OrderInterface
from ....order_center.order_config.utils.order_config_interface import OrderType, OrderConfigInterface
from ....order_center.process_config.utils.process_config_interface import ProcessConfigInterface


class DomainOrderInterface(OrderInterface, OrderConfigInterface, ProcessConfigInterface):
    order_type = OrderType.domain.name

    @classmethod
    def create_suborder(cls, **kwargs):
        result = DomainOrder.objects.create(
            domain=kwargs.get('domain'), value=kwargs.get('value'),
            type=kwargs.get('type'), purpose=kwargs.get('purpose'),
            remark=kwargs.get('remark'),
        )
        return result.id

    @classmethod
    def get_suborder(cls, suborder_id):
        result = DomainOrder.objects.all().filter(id=suborder_id).values(
            'domain', 'value', 'type', 'purpose', 'remark'
        ).first()

        data = {
            "域名": result['domain'],
            "类型": "修改" if result['type'] == 'update' else "新增",
            "记录值": result['value'],
            "用途": result['purpose'],
            "备注": result['remark'],
        }
        return data

    @classmethod
    def script_param(cls, order_id):
        order = super(DomainOrderInterface,
                      cls).order_id_get_order_info(order_id)
        sub_order = DomainOrder.objects.all().filter(id=order['suborder']).values(
            'domain', 'value', 'type', 'purpose', 'remark'
        ).first()

        param = {
            "order": order,
            "sub_order": sub_order,
        }

        param = json.dumps(param, cls=DateEncoder).encode()
        return b64encode(param).decode()

    @classmethod
    def ding_massage(cls, **order_info):
        sub_data = ''
        for k, v in cls.get_suborder(order_info['suborder']).items():
            if v is None:
                v = ''
            sub_data = f"{sub_data} > {k}: {v} \n\n"

        return sub_data
