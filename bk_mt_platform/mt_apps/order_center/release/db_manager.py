# -*- coding: utf-8 -*-

from django.conf import settings

from mt_apps.base.system_config.config_define import get_system_configs


class DBManager:
    def __init__(self, biz_id):
        self.biz_id = biz_id

    def set_mfw_db_settings(self, type, db_name):
        db_config = self.get_mfw_database_config(db_name)
        settings.DATABASES[type] = db_config

    def get_mfw_database_config(self, db_name):
        system_config = get_system_configs(self.biz_id,
                                           ['db_mfw_host', 'db_mfw_port', 'db_mfw_db', 'db_mfw_user', 'db_mfw_pwd'])

        return {
            'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
            'NAME': system_config['db_mfw_db'],  # 数据库名 (默认与APP_ID相同)
            'USER': system_config['db_mfw_user'],  # 你的数据库user
            'PASSWORD': system_config['db_mfw_pwd'],  # 你的数据库password
            'HOST': system_config['db_mfw_host'],  # 开发的时候，使用localhost
            'PORT': system_config['db_mfw_port'],  # 默认3306
        }

    def set_mfw_db(self):
        try:
            self.set_mfw_db_settings('mfw', 'db_mfw')
            return True
        except:
            return False
