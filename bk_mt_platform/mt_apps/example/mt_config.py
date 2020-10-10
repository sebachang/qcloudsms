name = 'example'
desc = '开发示例'


def register_jobs(biz_id):
    global name

    # from mt_apps.redis.constants import job_uuid
    # JobManager.register(biz_id, title=desc, module=name, job_uuid=job_uuid)


def register_notify():
    return (name, desc),


def register_config():
    from mt_apps.base.system_config.config_define import set_system_config

    cfg_module_process = {'index': 100, 'name': u'我的应用', 'icon': 'gear.svg'}

    set_system_config(cfg_module_process, 1, u'myapp_config', u'我的配置显示名称', u'配置描述')
