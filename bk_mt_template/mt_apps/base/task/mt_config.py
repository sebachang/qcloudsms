name = 'task'
desc = '任务作业'


def register_config():
    from mt_apps.base.system_config.config_define import set_system_config
    cfg_module_task = {'index': 5, 'name': u'任务管理', 'icon': 'gear.png'}

    set_system_config(cfg_module_task, 1, u'task_callback_url', u'任务回调URL', u'URL地址, 例如: http://127.0.0.1/callback',
                      isNull=True)
    set_system_config(cfg_module_task, 2, u'task_instance_refresh', u'任务状态刷新开关', u'true/false 默认为true', default='true')
