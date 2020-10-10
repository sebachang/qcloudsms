from rest_framework import routers

from .views import CmdbClearanceViewSet

router = routers.DefaultRouter()
router.register(r'', CmdbClearanceViewSet, base_name='cmdb_clearance')
urlpatterns = [

]
urlpatterns += router.urls
