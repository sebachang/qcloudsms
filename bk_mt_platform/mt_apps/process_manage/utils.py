import base64

from mt_apps.base.task.task_manager import TaskManager, BK_TaskManager


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        if ',' in x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = x_forwarded_for
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def run_cmd(request, biz_id=None, host=None, user=None, cmd=None, work_dir=None,
            timeout=None, job_uuid=None, task_name=None, **kargs):
    task_manager = TaskManager(request)

    script_content = "cd {} && {}".format(work_dir, cmd)
    task = task_manager.run_job(biz_id, job_uuid, ip_list=host, script_content=script_content, run_user=user,
                                task_name=task_name)
    return task


def run_bk_cmd(request, biz_id=None, host=None, user='root', cmd=None, work_dir='/',
               timeout=None, job_uuid=None, task_name=None, **kargs):
    task_manager = BK_TaskManager(request)

    script_content = base64.b64encode(("cd {} && {}".format(work_dir, cmd)).encode('utf-8')).decode('utf-8')
    if ':' in host:
        (cloud_id, ip) = host.split(':')
        ip_list = [{'bk_cloud_id': cloud_id, 'ip': ip}]
    else:
        ip_list = [{'bk_cloud_id': 0, 'ip': host}]
    task = task_manager.run_fast_job(biz_id, '', '', ip_list, user, script_content)
    return task


def get_job_status(request, biz_id, job_id):
    from mt_apps.base.task.task_manager import BK_TaskManager
    manager = BK_TaskManager(request)
    return manager.get_job_status(biz_id, job_id)
