# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Q

from blueapps.core.celery.celery import app
from mt_apps.base.api.components.login import LoginAPI
from mt_apps.base.utils.util_site import get_jump_site
from mt_apps.order_center.process_config.utils import get_audit_user
from ..order.utils.order_interface import OrderInterface, OrderInterfaceManagement
from ..process_config.utils.process_config_interface import ProcessConfigInterface


@app.task()
def order_approval_notice(order_id):
    result = OrderInterface.order_id_get_order_info(order_id)

    current_approval_step = result.get('current_approval_step', None)
    process_id = result.get('order_config__process_id', None)
    order_type = result.get('order_type', None)

    finish = False
    if result.get('order_state') == 1:
        approval_flow = ProcessConfigInterface.get_order_next_approval_flow(
            process_id, current_approval_step)
        notify_users = get_audit_user(approval_flow.get(
            'audit_type', '1'), approval_flow.get('auditor', ''))
    else:
        finish = True
        approval_flow = ProcessConfigInterface.get_approval_flow_list(
            process_id).first()
        notify_users = [result.get('submitter')]
    notify_flag = approval_flow.get('notify_flag', 0)

    if notify_users and notify_flag == 0:
        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()
        if hasattr(order_obj, 'ding_massage'):
            text = order_obj.ding_massage(**result)
            if text and isinstance(text, str):
                result_api = LoginAPI.get_batch_user_info(
                    user="admin", **{"bk_username_list": notify_users})

                phone = [v['phone'] for k, v in result_api['data'].items()
                         if k in notify_users if v['phone']]
                at_phone = ['@' + x for x in phone]

                if not finish:
                    content = "待审批工单:" + "\n\n" +\
                        "> 审批工单地址: [点击连接](" + get_jump_site('order/order_table/3') + ")" + "\n\n" +\
                        "> 工单号: " + str(result['id']) + "\n\n" +\
                        "> 提单人: " + result['submitter'] + "\n\n" +\
                        "> 工单名称: " + result['order_name'] + "\n\n" +\
                        text + ','.join(at_phone)
                else:
                    if result['order_state'] == 0:
                        approval_result = '审批通过'
                    else:
                        approval_result = '审批不通过\n\n'
                        approval_record = OrderInterface.order_id_get_order_approval_record_list(
                            order_id).first()
                        approval_result += "> 拒绝原因：" + approval_record.approval_step_remark

                    content = approval_result + "\n\n" +\
                        "> 审批工单地址: [点击连接](" + get_jump_site('order/order_table/3') + ")" + "\n\n" +\
                        "> 工单号: " + str(result['id']) + "\n\n" +\
                        text + ','.join(at_phone)

                payload = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "工单审批通知",
                        "text": content
                    },
                    "at": {
                        "atMobiles": phone,
                        "isAtAll": False
                    }
                }

                from mt_apps.base.notify_manage.apis import send_message
                tag = 'approval_' + order_type
                send_message(result['biz_id'], tag=tag, json=payload)


@periodic_task(run_every=crontab(minute='0', hour='11', day_of_week="*"))
def order_approval_notice_cron():
    print("order_approval_notice_cron")
    for x in OrderInterface.get_order_info_list().filter(order_state=1).order_by('-id'):
        order_id = x.get('id', '')
        if order_id:
            order_approval_notice(order_id)


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def order_jobs_state_check():
    from mt_apps.base.task.models import TaskInstanceModel
    from blueking.component.shortcuts import get_client_by_user

    job_status = {1: '未执行', 2: '正在执行', 3: '执行成功', 4: '执行失败', 5: '跳过',
                  6: '忽略错误', 7: '等待用户', 8: '手动结束', 9: '状态异常',
                  10: '步骤强制终止中', 11: '步骤强制终止成功', 12: '步骤强制终止失败'}

    client = get_client_by_user('admin')

    for x in OrderInterface.get_order_approval_record_list().filter(
            ~Q(task_instance_id=0), ~Q(jobs_state=3)).order_by('-id'):

        for objs in TaskInstanceModel.objects.filter(id=x.task_instance_id):
            params = {
                'bk_biz_id': objs.job.bk_biz,
                "job_instance_id": objs.instance
            }

            result_status = client.job.get_job_instance_status(params)
            state = result_status['data']['job_instance']['status']
            if state == 3:
                x.jobs_state = state
                x.save()
            elif state > 3:
                if x.jobs_state != state:
                    x.jobs_state = state
                    x.save()
                    result = OrderInterface.order_id_get_order_info(x.order_id)

                    payload = {
                        "msgtype": "markdown",
                        "markdown": {
                            "title": "工单作业通知测试",
                            "text": "工单作业异常" + "\n\n" +
                                    "> 异常工单地址: [点击连接](" + get_jump_site('order/order_table/4') + ")" + "\n\n" +
                                    "> 工单号: " + str(x.order_id) + "\n\n" +
                                    "> 步骤: " + str(x.approval_step) + "\n\n" +
                                    "> 作业实例: " + str(x.task_instance_id) + "\n\n" +
                                    "> 作业状态: " + job_status[state] + "\n\n"
                        },
                        "at": {
                            "atMobiles": [
                            ],
                            "isAtAll": True
                        }
                    }

                    from mt_apps.base.notify_manage.apis import send_message
                    from .mt_config import approval
                    if 'order_type' in result:
                        tag = 'approval_' + result.get('order_type', '')
                    else:
                        tag = approval
                    send_message(result['biz_id'], tag, json=payload)
