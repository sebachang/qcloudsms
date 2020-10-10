from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('mt_apps.base.urls')),
    url(r'^example/', include('mt_apps.example.urls')),

    # 在下面增加逻辑功能url
    url(r'^process_manage/', include('mt_apps.process_manage.urls')),
    url(r'^config_center/', include('mt_apps.config_center.urls')),
    url(r'^order_center/process/', include('mt_apps.order_center.process_config.urls')),
    url(r'^order_center/config/', include('mt_apps.order_center.order_config.urls')),
    url(r'^order_center/order/', include('mt_apps.order_center.order.urls')),
    url(r'^order_center/deliver/', include('mt_apps.order_center.deliver.urls')),
    url(r'^order_center/clearance/', include('mt_apps.order_center.clearance.urls')),
    url(r'^order_center/release/', include('mt_apps.order_center.release.urls')),
    url(r'^order_center/domain/', include('mt_apps.order_center.domain.urls')),
    url(r'^deliver_manage/', include('mt_apps.deliver_manage.urls')),
    url(r'^certificate/', include('mt_apps.certificate.urls')),
    url(r'^nginx/', include('mt_apps.nginx.urls')),
]
