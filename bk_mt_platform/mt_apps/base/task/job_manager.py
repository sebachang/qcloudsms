# -*- coding: utf-8 -*-

import uuid
from base64 import b64encode

from mt_apps.base.task.models import JobModel


class JobManager:
    # 其他业务使用接口
    @classmethod
    def register(cls, bk_biz, title, module, job_uuid=None, script=None, exec_ip='[]', username='', script_name='', ):
        if job_uuid:
            cls.job_uuid = job_uuid
        else:
            cls.job_uuid = str(uuid.uuid4())

        if script:
            try:
                script = script.encode()
            except ...:
                pass
            script = b64encode(script).decode()

        # 检查重复插入
        jobObj = JobModel.objects.filter(bk_biz=bk_biz, job_uuid=job_uuid)
        if len(jobObj) != 0:
            return jobObj[0].job_uuid
        else:
            data = {'job_uuid': cls.job_uuid, 'bk_biz': bk_biz, 'title': title, 'module': module,
                    'exec_ip': exec_ip, 'username': username, 'script_name': script_name, 'script': script}
            if JobModel.objects.create(**data):
                return cls.job_uuid
            else:
                return None

    # 批量业务注册
    @classmethod
    def biz_register(cls, bk_biz):
        # 场景: 手动注册, 直接拿uuid使用任务接口
        from conf import default
        for a in default.INSTALLED_APPS:
            try:
                _module = __import__(a + '.mt_config', fromlist=['register_jobs'])
                _module.register_jobs(bk_biz)
            except ImportError as e:
                pass
            except AttributeError as e:
                pass
        pass
