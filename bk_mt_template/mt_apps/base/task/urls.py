# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'job', JobViewSet, base_name='job')
router.register(r'taskinstance', TaskInstanceViewSet, base_name='taskinstance')

router.register(r'task', TaskViewSet, base_name='task')
router.register(r'log', LogViewSet, base_name='log')

router.register(r'register', RegisterViewSet, base_name='register')

# router.register(r'callback', CallbackViewSet, base_name='callback')

urlpatterns = [
    url('^callback', CallbackViewSet, name='callback')
]

urlpatterns += router.urls
