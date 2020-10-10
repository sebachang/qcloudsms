from rest_framework import routers

from .views import OrderConfigViewSet, AutoOrderConfig

router = routers.DefaultRouter()

router.register(r'config', OrderConfigViewSet, base_name='order_config')
router.register(r'', AutoOrderConfig, base_name='auto_create_order_config')
urlpatterns = [

]

urlpatterns += router.urls
