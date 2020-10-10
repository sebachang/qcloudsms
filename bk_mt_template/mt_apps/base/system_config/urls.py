# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers

from mt_apps.base.system_config.views import SystemConfigGeneric, SystemConfigViewSet, SCViewSet

router = routers.DefaultRouter()
router.register(r'setting_generic', SystemConfigGeneric, base_name='setting_generic')
router.register(r'sc', SCViewSet, base_name='sc')

urlpatterns = [
    url(r'^setting/$', SystemConfigViewSet.as_view({"post": "create"})),
    url(r'^setting/(?P<config_key>.+)/', SystemConfigViewSet.as_view({"put": "update"})),
]

urlpatterns += router.urls
