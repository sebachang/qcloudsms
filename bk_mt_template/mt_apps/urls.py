from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('mt_apps.base.urls')),
    url(r'^example/', include('mt_apps.example.urls')),

    # 在下面增加逻辑功能url
]
