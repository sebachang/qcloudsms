# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers as drf_routers

from mt_apps.base.api.test_views import test_api
from mt_apps.base.api.views.app_util import AppUtilViewSet
from mt_apps.base.api.views.cmdb import CmdbViewSet
from mt_apps.base.api.views.login import LoginViewSet

router = drf_routers.DefaultRouter(trailing_slash=True)

router.register(r'login', LoginViewSet, base_name='login')
router.register(r'cmdb', CmdbViewSet, base_name='cmdb')
router.register(r'app_util', AppUtilViewSet, base_name='app_util')

urlpatterns = [
    url(r'^test_api/$', test_api),
]

urlpatterns += router.urls
