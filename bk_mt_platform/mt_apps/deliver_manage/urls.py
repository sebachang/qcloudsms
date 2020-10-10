from django.conf.urls import url
from rest_framework import routers

from .views import PlatformViewSet, HostProfileViewSet, CenterViewSet, PlatformHostProfileMapViewSet, \
    PlatformCenterMapViewSet, DeliverDetailViewSet, DeliverDetailUploadViewSet, DeliverOrderViewSet, \
    SearchDeliverDetailViewSet, MyDeliverOrderViewSet, ClearanceOrderViewSet, ClearanceDetailViewSet, \
    SearchClearanceDetailViewSet, update_deliver_host_passwd

router = routers.DefaultRouter()

router.register(r'platform', PlatformViewSet, base_name='deliver_platform')
router.register(r'host', HostProfileViewSet, base_name='deliver_host')
router.register(r'center', CenterViewSet, base_name='deliver_center')
router.register(r'map/platform/host', PlatformHostProfileMapViewSet, base_name='deliver_platform_host_map')
router.register(r'map/platform/center', PlatformCenterMapViewSet, base_name='deliver_platform_center_map')
router.register(r'deliver/order', DeliverOrderViewSet, base_name='deliver_order')
router.register(r'my/deliver/order', MyDeliverOrderViewSet, base_name='my_deliver_order')
router.register(r'search/deliver/detail', SearchDeliverDetailViewSet, base_name='search_detail')
router.register(r'deliver/detail', DeliverDetailViewSet, base_name='deliver_detail')
router.register(r'deliver/upload/detail', DeliverDetailUploadViewSet, base_name='deliver_detail_upload')
router.register(r'clearance/order', ClearanceOrderViewSet, base_name='clearance_order')
router.register(r'clearance/detail', ClearanceDetailViewSet, base_name='clearance_detail')
router.register(r'search/clearance/detail', SearchClearanceDetailViewSet, base_name='search_clearance_detail')
urlpatterns = [
    url('update_deliver_host_passwd', update_deliver_host_passwd)
]
urlpatterns += router.urls
