from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('channel', ChannelViewSet)
router.register('rule', RuleViewSet)
router.register('tag', TagViewSet, basename='tag')

urlpatterns = router.urls
