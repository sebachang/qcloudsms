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

urlpatterns = [url(r'^template/render/(?P<pk>\d+)/$',
                   render_template, name="render_template"),
               url(r'^template/$',
                   ConfigTemplateViewSet.as_view({'get': 'list',
                                                  "post": "create"})),
               url(r'^template/(?P<pk>\d+)/',
                   ConfigTemplateViewSet.as_view({"get": "retrieve",
                                                  "put": "update",
                                                  "delete": "destroy"})),
               url(r'^kv/$',
                   ConfigKVViewSet.as_view({'get': 'list',
                                            'post': 'create'})),
               url(r'^kv/(?P<pk>\d+)/',
                   ConfigKVViewSet.as_view({"get": "retrieve",
                                            "put": "update",
                                            "delete": "destroy"})),
               ]

urlpatterns += router.urls
