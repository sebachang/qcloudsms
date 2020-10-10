# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'cert', CertViewSet, base_name='cert')
router.register(r'register', CertRegisterViewSet, base_name='register')
router.register(r'domain', DomainViewSet, base_name='domain')
router.register(r'cluster', ClusterViewSet, base_name='cluster')
router.register(r'check', CertCheckViewSet, base_name='check')
router.register(r'cert_list', CertListViewSet, base_name='cert_list')
router.register(r'domain_list', DomainListViewSet, base_name='domain_list')

urlpatterns = [
    url('^download/(?P<pk>[0-9]+)/(?P<zipfile>.*)\.zip$', CertDownloadViewSet, name='download')
]

urlpatterns += router.urls

