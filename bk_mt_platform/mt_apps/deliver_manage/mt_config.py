name = 'deliver_manage'
desc = '交付管理'


def register_jobs(biz_id):
    from mt_apps.base.task.job_manager import JobManager

    JobManager.register(biz_id, '交付检查', 'deliver_check', '09e629d6-44ff-46a3-95a0-19bb3ff4638d')


def register_config():
    from mt_apps.base.system_config.config_define import set_system_config

    cfg_module_deliver = {'index': 17, 'name': u'交付管理', 'icon': 'gear.svg'}

    set_system_config(cfg_module_deliver, 1, u'deliver_api_token', u'交付API Token', u'交付API的Token，用于调用API')
