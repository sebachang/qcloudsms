from django.conf.urls import url
from rest_framework import routers

from .views import OrderViewSet, MyOrderViewSet, MyApprovalOrderViewSet, \
    OrderApprovalRecordViewSet, OrderApprovalPermissionViewSet, OrderApprovalFlowViewSet, SubOrderInfoViewSet, \
    SearchOrderViewSet, ExceptionOrderViewSet, OrderJobReExecuteViewSet, OrderScriptParamViewSet, script_param

router = routers.DefaultRouter()

router.register(r'order', OrderViewSet, base_name='order')
router.register(r'my/order', MyOrderViewSet, base_name='my_order')
router.register(r'my/approval/order', MyApprovalOrderViewSet, base_name='my_approval_order')
router.register(r'exception/order', ExceptionOrderViewSet, base_name='exception_order')
router.register(r'search/order', SearchOrderViewSet, base_name='search_order')
router.register(r'order/approval/record', OrderApprovalRecordViewSet, base_name='order_approval_record')
router.register(r'', OrderApprovalPermissionViewSet, base_name='get_approval')
router.register(r'order/approval/flow', OrderApprovalFlowViewSet, base_name='order_approval_flow')
router.register(r'', SubOrderInfoViewSet, base_name='suborder')
router.register(r'', OrderJobReExecuteViewSet, base_name='job_execute')
router.register(r'', OrderScriptParamViewSet, base_name='script_param')
urlpatterns = [url(r'^script/param/(?P<pk>\d+)/$',
                   script_param, name="script_param_api")

               ]

urlpatterns += router.urls
