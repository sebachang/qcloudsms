from mt_apps.deliver_manage.models import ClearanceDetail
from ..models import ClearanceOrder
from ....order_center.order.utils.order_interface import OrderInterface
from ....order_center.order_config.utils.order_config_interface import OrderType, OrderConfigInterface
from ....order_center.process_config.utils.process_config_interface import ProcessConfigInterface


class ClearanceOrderInterface(OrderInterface, OrderConfigInterface, ProcessConfigInterface):
    order_type = OrderType.clearance.name

    @classmethod
    def create_suborder(cls, **kwargs):
        result = ClearanceOrder.objects.create(remove_id=kwargs.get('remove_id'))
        return result.id

    @classmethod
    def get_suborder(cls, suborder_id):
        result = ClearanceOrder.objects.all().filter(id=suborder_id).values().first()

        data = {
            "清退编号": result['remove_id'],
        }
        return data

    @classmethod
    def create_detail(cls, order_id, **kwargs):
        for x in kwargs.get('clearance_list'):
            x['order_id_id'] = order_id
            ClearanceDetail.objects.create(**x)

    @classmethod
    def cancel_order(cls, order_id):
        ClearanceDetail.objects.filter(order_id=order_id).delete()
        return

    @classmethod
    def ding_massage(cls, **order_info):

        sub_data = ''
        for k, v in cls.get_suborder(order_info['suborder']).items():
            sub_data = sub_data + ">" + k + ": " + v + "\n\n"

        return sub_data
