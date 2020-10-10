from rest_framework import routers

from .views import VersionViewSet, SelectServersViewSet, ServerlistViewSet, GetSerVersionViewSet

router = routers.DefaultRouter()
router.register(r'serverlist', ServerlistViewSet, base_name='serverlist')
router.register(r'version', VersionViewSet, base_name='version')
router.register(r'servers', SelectServersViewSet, base_name='servers')
router.register(r'get_version', GetSerVersionViewSet, base_name='get_version')

urlpatterns = [

]
urlpatterns += router.urls
