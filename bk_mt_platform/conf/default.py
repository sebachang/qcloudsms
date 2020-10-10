from mt_apps.base.conf.default import *

INSTALLED_APPS += (
    'mt_apps.example',
    'mt_apps.config_center',
    'mt_apps.process_manage',
    'mt_apps.order_center.process_config',
    'mt_apps.order_center.order_config',
    'mt_apps.order_center.order',
    'mt_apps.order_center.deliver',
    'mt_apps.order_center.clearance',
    'mt_apps.order_center.release',
    'mt_apps.order_center.domain',
    'mt_apps.deliver_manage',
    'mt_apps.certificate',
    'mt_apps.nginx',
)

CELERY_IMPORTS += (
    'mt_apps.certificate.celery_tasks',
)

REST_FRAMEWORK.update({
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S"
})

