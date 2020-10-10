# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers

from mt_apps.example.views import ExampleGenericViewSet, ExampleViewSet, test_example

router = routers.DefaultRouter()
router.register(r'generic_view', ExampleGenericViewSet, base_name='generic_view')

urlpatterns = [
    url(r'^test_example/$', test_example),
    url(r'^model_view/$', ExampleViewSet.as_view({'get': 'list', "post": "create"})),
    url(r'^model_view/(?P<pk>\d+)/', ExampleViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
]

urlpatterns += router.urls
