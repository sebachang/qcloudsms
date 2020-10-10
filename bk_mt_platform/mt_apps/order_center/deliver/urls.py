from rest_framework import routers

from .views import OrderPlatformHostViewSet, OrderPlatformCenterViewSet

router = routers.DefaultRouter()

router.register(r'order', OrderPlatformHostViewSet, base_name='order_platform_host')
router.register(r'order', OrderPlatformCenterViewSet, base_name='order_platform_center')
urlpatterns = [

]
urlpatterns += router.urls
