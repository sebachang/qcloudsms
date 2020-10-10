# -*- coding:utf-8 -*-

# 配置可以测试用
from mt_apps.base.system_config.models import SystemSetting
from mt_apps.base.app_fw.exceptions import CommonLogicError

config_dict = {}


# 设置系统配置
def set_system_config(cfg_module, cfg_index, cfg_key, key_desc, value_desc, isNull=False, default=''):
    config_dict[cfg_key] = {
        'cfg_index': cfg_index,
        'module': cfg_module,
        'key_desc': key_desc,
        'value_desc': value_desc,
        'is_null': isNull,
        'default': default
    }


# 获取系统配置, 基于业务id和配置key
def get_system_config(biz_id, config_key):
    config_info = config_dict.get(config_key)
    if not config_info:
        raise CommonLogicError({'code': -500, 'message': u"系统配置key<" + config_key + ">不存在"})

    value = ''
    if config_info['default'] != '':
        value = config_info['default']

    data = SystemSetting.objects.values('config_value').filter(biz_id=biz_id, config_key=config_key)
    if len(data) > 0:
        value = data[0]['config_value']

    if value == '':
        if not config_info['is_null']:
            raise CommonLogicError({'code': -501,
                                    'message': u"系统配置->" + config_info['module']['name'] + "->" + config_info[
                                        'key_desc'] + ": 未配置"})

    return value


def get_system_configs(biz_id, config_keys=[]):
    kvs = {}
    for config_key in set(config_keys):
        kvs[config_key] = get_system_config(biz_id, config_key)

    return kvs

