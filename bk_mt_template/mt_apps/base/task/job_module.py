# -*- coding: utf-8 -*-

JobModule = (('default', '默认'),)

from conf import default

for a in default.INSTALLED_APPS:
    try:
        p = a + '.mt_config'
        _module = __import__(p, fromlist=['name', 'desc'])
        JobModule += ((_module.name, _module.desc),)
    except ImportError as e:
        # print('failed: ', a, e)
        pass
pass
