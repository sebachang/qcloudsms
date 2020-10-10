# -*- coding: utf-8 -*-

from rest_framework import routers

from mt_apps.base.permission.views import RouteViewSet, UserRoutesViewSet, GroupViewSet, GroupsViewSet

router = routers.DefaultRouter()
router.register(r'route', RouteViewSet, base_name='route')
router.register(r'group', GroupViewSet, base_name='group')
router.register(r'group_list', GroupsViewSet, base_name='group_list')
router.register(r'user_routes', UserRoutesViewSet, base_name='user_routes')

urlpatterns = [
]

urlpatterns += router.urls
