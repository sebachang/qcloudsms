from django.conf.urls import url

from .views import ChangelogViewSet

urlpatterns = [
    url(r'^changelog/$',
        ChangelogViewSet.as_view({'get': 'list', 'post': 'add_log'})),

]
