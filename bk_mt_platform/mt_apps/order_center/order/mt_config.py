name = 'order'
desc = '工单'
approval = 'approval'
approval_deliver = 'approval_deliver'
approval_clearance = 'approval_clearance'
approval_release = 'approval_release'
approval_domain = 'approval_domain'


def register_config():
    from mt_apps.base.system_config.config_define import set_system_config
    cfg_module_order = {'index': 7, 'name': u'清退工单', 'icon': 'gear.svg'}
    set_system_config(cfg_module_order, 1, u'search_clearance_node', u'清退CMDB节点名称', u'如果需要获取清退主机列表，请填写清退节点名称: 待清退机器',
                      default='待清退机器')

    # svn配置
    cfg_module_svn_test = {'index': 8, 'name': u'发布工单', 'icon': 'gear.svg'}
    set_system_config(cfg_module_svn_test, 1, u'svn_host', u'svn请求主机名', u'填写主机地址')
    set_system_config(cfg_module_svn_test, 2, u'svn_protocol', u'请求协议', u'http / https')
    set_system_config(cfg_module_svn_test, 3, u'svn_path', u'请求路径', u'填写请求路径 例如:/svn/mlserver/branches/')
    set_system_config(cfg_module_svn_test, 5, u'svn_port', u'请求端口', u'请填写端口')
    set_system_config(cfg_module_svn_test, 6, u'svn_username', u'svn用户名', u'请填写用户名')
    set_system_config(cfg_module_svn_test, 7, u'svn_password', u'svn密码', u'请填写登录密码', isNull=True)


def register_notify():
    global approval, approval_deliver, approval_clearance, approval_release, approval_domain
    return (approval, '工单审批'), (approval_deliver, '交付审批'), (approval_clearance, '清退审批'), (approval_release, '发布审批'), (approval_domain, '域名申请')
