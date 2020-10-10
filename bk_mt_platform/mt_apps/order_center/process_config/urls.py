from rest_framework import routers

from .views import ProcessConfigViewSet, ApprovalFlowViewSet

router = routers.DefaultRouter()

router.register(r'config', ProcessConfigViewSet, base_name='process_config')
router.register(r'approval/flow', ApprovalFlowViewSet, base_name='approval_flow')

urlpatterns = [

]

urlpatterns += router.urls
