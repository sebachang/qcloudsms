"""config_center URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register("operation", InstanceOperationViewSet, base_name="operation")
router.register("", ProcessGenericViewSet, base_name="process")

urlpatterns = [
    url(r'^process/$',
        ProcessViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^process/(?P<pk>\d+)/',
        ProcessViewSet.as_view({"get": "retrieve",
                                "put": "update",
                                "delete": "destroy"})),
    url(r'^instance/$',
        InstanceViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^instance/(?P<pk>\d+)/status/', InstanceViewSet.as_view({'get': 'get_instance_status'})),
    url(r'^instance/(?P<pk>\d+)/',
        InstanceViewSet.as_view({"get": "retrieve",
                                 "put": "update",
                                 "delete": "destroy"})),
    url(r'^(?P<pk>\d+)/list', get_by_process),
    url(r'^search/(?P<biz_id>\d+)/(?P<name>\w+)', get_by_process_name),
]

urlpatterns += router.urls
