name = 'release'
desc = '发布工单'


def register_config():
    cfg_module_db_mfw = {'index': 10, 'name': u'db_mfw配置', 'icon': 'gear.svg'}

    from mt_apps.base.system_config.config_define import set_system_config

    # db_mfw配置
    set_system_config(cfg_module_db_mfw, 1, u'db_mfw_host', u'host地址', u'数据库host地址')
    set_system_config(cfg_module_db_mfw, 2, u'db_mfw_port', u'端口', u'数据库端口')
    set_system_config(cfg_module_db_mfw, 3, u'db_mfw_db', u'库名', u'数据名称')
    set_system_config(cfg_module_db_mfw, 4, u'db_mfw_user', u'用户', u'数据库用户')
    set_system_config(cfg_module_db_mfw, 5, u'db_mfw_pwd', u'密码', u'数据库密码', isNull=True)
