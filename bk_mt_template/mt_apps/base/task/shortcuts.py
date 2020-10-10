# -*- coding: utf-8 -*-
import time

from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from mt_apps.base.app_fw.error_code import EC_PARAM_INCORRECT
from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.task.task_manager import TaskManager


def run_job_sync(biz_id, job_uuid, request=None, bk_username=None, user=None, ip=None, script=None, params=None,
                 task_name=None):
    """
    这个方法会等待作业执行完成再返回，只允许在celery里面调用
    :rtype: str
    """
    client = None
    if request is not None:
        client = get_client_by_request(request)
    elif bk_username is not None:
        client = get_client_by_user(bk_username)
    if client is None:
        raise CommonLogicError({'code': EC_PARAM_INCORRECT, 'message': 'bk_username和request不能同时为空'})

    manager = TaskManager(None, user=bk_username, client=client)
    result = manager.run_job(biz_id, job_uuid, ip_list=ip, script_param=params, script_content=script, run_user=user,
                             task_name=task_name)

    task_instance_id = result['data']['task_instance_id']

    while True:
        time.sleep(5)
        instance_status = manager.get_task_status(task_instance_id)
        if instance_status['is_finished']:
            break

    task_log = manager.get_task_log(task_instance_id)

    ip_logs = {}
    for log in task_log[0]['step_results'][0]['ip_logs']:
        ip_logs[log['ip']] = log['log_content']

    if len(ip_logs) == 1:
        return next(iter(ip_logs.values()))
    return ip_logs
