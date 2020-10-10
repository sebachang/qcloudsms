# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['celery_app', 'RUN_VER', 'APP_CODE', 'SECRET_KEY', 'BK_URL', 'BASE_DIR']

import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from blueapps.core.celery import celery_app

# app 基本信息

# SaaS运行版本，如非必要请勿修改
RUN_VER = 'open'
# SaaS应用ID
APP_CODE = 'bk-mt-template'
# SaaS安全密钥，注意请勿泄露该密钥
SECRET_KEY = os.environ.get('APP_TOKEN', 'e9cb1b7c-c327-4a53-a7a3-a5e5707d188a')
# 蓝鲸SaaS平台URL, 如 https://paas.blueking.com/
BK_URL = 'http://paas.bk.oa.mt:80'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__)))
