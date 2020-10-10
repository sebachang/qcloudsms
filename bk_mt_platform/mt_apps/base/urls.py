# -*- coding: utf-8 -*-

from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/', include('mt_apps.base.api.urls')),
    url(r'^permission/', include('mt_apps.base.permission.urls')),
    url(r'^system_config/', include('mt_apps.base.system_config.urls')),
    url(r'^audit/', include('mt_apps.base.audit.urls')),
    url(r'^task/', include('mt_apps.base.task.urls')),
    url(r'^notify_manage/', include('mt_apps.base.notify_manage.urls')),
]
