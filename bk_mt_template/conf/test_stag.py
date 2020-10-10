# -*- coding: utf-8 -*-
from conf import RUN_VER

if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 预发布环境
RUN_MODE = 'STAGING'

# 正式环境的日志级别可以在这里配置
# V2
# import logging
# logging.getLogger('root').setLevel('INFO')


# 预发布环境数据库可以在这里配置
DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bk_mt_template_stag',
            'USER': 'bk_dev',
            'PASSWORD': 'bk_dev2016',
            'HOST': '192.168.40.24',
            'PORT': '3306',
        },
    }
)
