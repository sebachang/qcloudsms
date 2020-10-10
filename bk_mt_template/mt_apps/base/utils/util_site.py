# -*- coding:utf-8 -*-


# 获取跳转的站点URL
from blueapps.patch.settings_open_saas import SITE_URL, BK_PAAS_HOST, IS_LOCAL


def get_jump_site(router):
    if IS_LOCAL:
        return 'http://dev.bk.oa.mt:9527/#/' + router
    else:
        if BK_PAAS_HOST == 'http://paas.bk.oa.mt:80':
            return BK_PAAS_HOST + SITE_URL + '#/' + router
        elif BK_PAAS_HOST == 'https://paas.bk.moonton.net:443':
            return BK_PAAS_HOST + SITE_URL + '#/' + router
        else:
            return None


# 获取下载站点URL
def get_download_site(router):
    if IS_LOCAL:
        return 'http://dev.bk.oa.mt:9527/' + router
    else:
        if BK_PAAS_HOST == 'http://paas.bk.oa.mt:80':
            return BK_PAAS_HOST + SITE_URL + router
        elif BK_PAAS_HOST == 'https://paas.bk.moonton.net:443':
            return BK_PAAS_HOST + SITE_URL + router
        else:
            return None
