# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.utils.util_site import get_jump_site, get_download_site


class ExampleGenericAPI(object):
    @classmethod
    def test_generic_api(cls, request, api_ver):

        api_ver = 4
        if api_ver == 1:
            client = get_client_by_request(request)
            result = client.bk_login.get_user()
            return result

        elif api_ver == 2:
            test_dict = {
                "name": "John",
                "age": 30,
                "city": "New York",
            }

            return test_dict

        elif api_ver == 3:
            test_dict = {
                "name": u"测试异常",
                "id": 100001000,
            }

            if True:
                raise CommonLogicError({'code': 100001000, 'message': u"调用登录接口失败"})

            return test_dict
        elif api_ver == 4:
            result = {
                'jump': get_jump_site('123'),
                'download': get_download_site('456')
            }
            return result
