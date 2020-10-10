# -*- coding: utf-8 -*-
import json
from enum import Enum, unique

from mt_apps.base.permission.models import Group
from mt_apps.order_center.process_config.utils import get_audit_user
from mt_apps.order_center.process_config.utils.process_config_interface import ProcessConfigInterface, ProcessType
from ..models import OrderConfig

'''
订单模块枚举类型, 保证唯一
    OrderType.module_1.name = "module_1"
    OrderType.module_1.value = 1
'''


@unique
class OrderType(Enum):
    deliver = 1
    release = 2
    clearance = 3
    domain = 4


class OrderConfigInterface(object):
    # 其他业务使用接口
    @classmethod
    def register(cls, biz_id, order_type, order_name, process_type, process_name, process_steps, job_type, job_title):
        # 注册流程 - 每次都跑一次, 可以增删步骤
        process_id = ProcessConfigInterface.register(biz_id, process_type, process_name, process_steps, job_type,
                                                     job_title)

        # 注册订单配置
        result = OrderConfig.objects.filter(biz_id=biz_id, order_type=order_type).first()
        if result is None:
            result = OrderConfig.objects.create(biz_id=biz_id, order_type=order_type, order_name=order_name,
                                                process_id=process_id)

        return result.id

    # 批量业务注册
    @classmethod
    def biz_register(cls, biz_id):
        cls.register(biz_id, OrderType.deliver.name, '交付工单', ProcessType.deliver.name, '交付审批流程', 2,
                     'deliver', "交付流程")
        cls.register(biz_id, OrderType.clearance.name, '清退工单', ProcessType.clearance.name, '清退审批流程', 2,
                     'clearance', "清退流程")
        cls.register(biz_id, OrderType.release.name, '发布工单', ProcessType.release.name, '发布审批流程', 2,
                     'release', "发布流程")
        cls.register(biz_id, OrderType.domain.name, '域名工单', ProcessType.domain.name, '域名审批流程', 2,
                     'domain', "域名流程")

    @classmethod
    def order_type_get_order_config(cls, order_type, biz_id):
        result = OrderConfig.objects.filter(order_type=order_type, biz_id=biz_id).values().first()
        result = {} if result is None else result
        return result

    @classmethod
    def order_type_get_auditor(cls, order_type, biz_id):
        result = cls.order_type_get_order_config(order_type, biz_id)
        process_id = result.get('process_id')
        result = []
        for x in ProcessConfigInterface.get_approval_flow_list(process_id):
            result = result + get_audit_user(x.get('audit_type', 1), x.get('auditor', ''))
        return result

    @classmethod
    def order_type_get_create_order_auditor(cls, order_type, biz_id):
        result = cls.order_type_get_order_config(order_type, biz_id)
        process_id = result.get('process_id')
        result = []
        group_users = {}
        for g in Group.objects.all():
            try:
                group_users[g.id] = json.loads(g.users)
            except ...:
                pass
        for x in ProcessConfigInterface.get_approval_flow_list(process_id):
            result = result + get_audit_user(x.get('audit_type', 1), x.get('auditor', ''))
        return result
