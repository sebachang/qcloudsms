name = 'nginx_manage'
desc = 'nginx管理'

def register_jobs(biz_id):
    global name, desc
    from mt_apps.base.task.job_manager import JobManager
    from .constants import job_uuid
    JobManager.register(biz_id, desc, name, job_uuid)
