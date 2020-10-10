# -*- coding: utf-8 -*-
from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.system_config.config_define import config_dict
from mt_apps.base.system_config.models import SystemSetting


class SystemConfigGenericAPI(object):
    @classmethod
    def get_list(cls, request):
        biz_id = request.GET.get('biz_id')
        if biz_id is None or int(biz_id) < 0:
            raise CommonLogicError({'code': 10001, 'message': u"未传递biz_id或biz_id为负值"})

        queryset = SystemSetting.objects.filter(biz_id=biz_id)
        config_db = dict()
        for obj in queryset:
            config_db.setdefault(obj.config_key, obj.config_value)

        result = {'config_dict': config_dict, 'config_db': config_db}
        return result
