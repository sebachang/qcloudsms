name = 'certificate'
desc = '证书发布'


def register_notify():
    return (name, desc),


def register_jobs(biz_id):
    global name, desc
    from mt_apps.base.task.job_manager import JobManager
    from .constants import job_uuid
    from .job_script import Cert_Deploy_Job_Script
    JobManager.register(biz_id, desc, name, job_uuid, script=Cert_Deploy_Job_Script, username='root')
