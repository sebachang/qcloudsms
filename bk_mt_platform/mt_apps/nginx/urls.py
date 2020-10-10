# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'cluster', ClusterViewSet, base_name='cluster')
router.register(r'config', ConfigViewSet, base_name='config')
router.register(r'config_list', ConfigListViewSet, base_name='config_list')
router.register(r'vhost', VhostViewSet, base_name='vhost')
router.register(r'vhost_list', VhostListViewSet, base_name='vhost_list')
router.register(r'template_base', TemplateBaseViewSet, base_name='template_base')
router.register(r'template_vhost', TemplateVhostViewSet, base_name='template_vhost')
router.register(r'instance', InstanceViewSet, base_name='instance')
router.register(r'job', JobViewSet, base_name='job')
router.register(r'operator', OperationViewSet, base_name='operator')

urlpatterns = [
    url(r'^search/(?P<biz_id>\d+)/', get_by_process_name)
]

urlpatterns += router.urls
