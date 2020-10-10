import importlib
import pkgutil
from inspect import getmembers, isclass

from django.db.models import F

from mt_apps.order_center.order.models import Orders, OrderApprovalRecord


class OrderInterface(object):
    order_type = ''

    @classmethod
    def order_id_get_order_config(cls, order_id):
        result = Orders.objects.filter(id=order_id).values(
            'order_config_id', 'order_config__order_type', 'order_config__order_name', 'order_config__process_id'
        ).first()
        result = {} if result is None else result
        return result

    @classmethod
    def order_id_get_order_info(cls, order_id):
        result = Orders.objects.filter(id=order_id).annotate(
            order_type=F('order_config__order_type'),
            order_name=F('order_config__order_name'),
            process_steps=F('order_config__process__process_steps'),
        ).values(
            'id', 'order_config_id', 'submitter', 'biz_id', 'suborder', 'order_state',
            'create_time', 'update_time', 'order_type', 'order_name', 'current_approval_step', 'process_steps',
            'order_config__process_id', 'order_config__ding_api', 'order_config__ding_token'
        ).first()
        result = {} if result is None else result
        return result

    @classmethod
    def get_order_info_list(cls):
        result = Orders.objects.annotate(
            order_type=F('order_config__order_type'),
            order_name=F('order_config__order_name'),
            process_steps=F('order_config__process__process_steps'),
        ).values(
            'id', 'order_config_id', 'submitter', 'biz_id', 'suborder', 'order_state',
            'create_time', 'update_time', 'order_config', 'order_name', 'current_approval_step', 'process_steps',
            'order_config__process_id', 'order_config__ding_api', 'order_config__ding_token'
        )
        return result

    @classmethod
    def order_id_get_order_approval_record_list(cls, order_id):
        result = OrderApprovalRecord.objects.filter(order_id=order_id).order_by('-approval_step')
        return result

    @classmethod
    def get_order_approval_record_list(cls):
        result = OrderApprovalRecord.objects
        return result

    @classmethod
    def update_order_state_current_approval_step(cls, order_id, state, current_approval_step):
        result = Orders.objects.filter(id=order_id).update(order_state=state,
                                                           current_approval_step=current_approval_step)
        return result

    # @classmethod
    # def create_suborder(cls, **kwargs):
    #     return
    #
    # @classmethod
    # def get_suborder(cls, suborder_id):
    #     return
    #
    # @classmethod
    # def create_detail(cls, order_id, **kwargs):
    #     return
    #
    # @classmethod
    # def cancel_order(cls, order_id):
    #     return
    #
    # @classmethod
    # @return string
    # def script_param(cls, order_id):
    #     return


class OrderInterfaceManagement(object):

    def __init__(self, order_type):
        self.order_type = order_type

    def get_register_order_class(self):
        import mt_apps.order_center
        for importer, name, is_pkg in pkgutil.walk_packages(
                mt_apps.order_center.__path__, "%s." % mt_apps.order_center.__name__):
            if not is_pkg:
                if name.split('.')[-2] == 'utils':
                    module = importlib.import_module(name)
                    for (_, value) in getmembers(module):
                        if isclass(value):
                            if hasattr(value, 'order_type'):
                                if value.order_type == self.order_type:
                                    return value
        return None
