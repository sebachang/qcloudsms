# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""

import calendar
import datetime

from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Count
from django.db.models import Q

from mt_apps.base.notify_manage.apis import send_message


def dateformat(dt):
    res_time = None
    try:
        dt = dt.split(' ')
        dt = [i for i in dt if i != '']
        dt[1] = list(calendar.month_abbr).index(dt[1])
        dtf = dt[5] + '-' + str(dt[1]) + '-' + dt[2] + " " + dt[3]
        date_time = datetime.datetime.strptime(dtf, '%Y-%m-%d %H:%M:%S')
        res_time = (date_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass

    return res_time


def getbizname(bk_biz):
    from blueking.component.shortcuts import get_client_by_user
    name = None
    client = get_client_by_user('admin')

    xagrs = {
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ],
        "condition": {
            "bk_biz_id": bk_biz
        },
    }
    result = client.cc.search_business(xagrs)
    if result['result'] and len(result['data']) > 0:
        name = result['data']['info'][0]['bk_biz_name']
    return name


@periodic_task(run_every=crontab(minute='*/30', hour='*', day_of_week="*"))
def domain_check_notice_cron():
    from mt_apps.certificate.models import DomainModel

    now = datetime.datetime.now()
    end_1day = now - datetime.timedelta(days=1)

    domains = DomainModel.objects.filter(Q(check=True), Q(check_time__lte=end_1day) | Q(expired_time__isnull=True))
    for domain in domains:
        domain.save()


@periodic_task(run_every=crontab(minute='0', hour='11', day_of_week="*"))
def cert_check_notice_cron():
    from mt_apps.certificate.models import DomainModel

    ding_title = "域名证书到期检查"

    now = datetime.datetime.now()
    end_7day = now + datetime.timedelta(days=7)
    end_15day = now + datetime.timedelta(days=15)

    for domain in DomainModel.objects.values('bk_biz').annotate(num=Count('bk_biz')):
        bk_biz = domain['bk_biz']
        cert_sum = domain['num']
        biz_name = getbizname(bk_biz)

        cert_error_obj = DomainModel.objects.filter(expired_time__isnull=True, bk_biz=bk_biz, check=True)
        cert_error_num = cert_error_obj.count()
        cert_error_domain = cert_error_obj.values('name')

        cert_expired_7day_obj = DomainModel.objects.filter(expired_time__lte=end_7day, bk_biz=bk_biz)
        cert_expired_7day_num = cert_expired_7day_obj.count()
        cert_expired_7day_domain = cert_expired_7day_obj.values('name')
        cert_expired_15day_obj = DomainModel.objects.filter(expired_time__range=(end_7day, end_15day),
                                                            bk_biz=bk_biz)
        cert_expired_15day_num = cert_expired_15day_obj.count()
        cert_expired_15day_domain = cert_expired_15day_obj.values('name')

        text = "### 总数/错误/1周过期/半月过期:  **<font color=#00ff00>" + str(
            cert_sum) + '</font>** / ' + "**<font color=#a30000>" + str(
            cert_error_num) + '</font>** / ' + "**<font color=#FF0000>" + str(
            cert_expired_7day_num) + '</font>** / ' + "**<font color=#ff9900>" + str(
            cert_expired_15day_num) + "</font>**" + '\n'
        error_domain = "#### **错误的域名列表:**" + '\n'
        for domain in cert_error_domain:
            error_domain += "+ <font color=#a30000>" + domain['name'] + '</font>\n'
        text_7day = "#### **7天内过期的域名列表:**" + '\n'
        for domain in cert_expired_7day_domain:
            text_7day += "+ <font color=#FF0000>" + domain['name'] + '</font>\n'
        text_15day = "#### **15天内过期的域名列表:**" + '\n'
        for domain in cert_expired_15day_domain:
            text_15day += "+ <font color=#ff9900>" + domain['name'] + '</font>\n'

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": ding_title,
                "text": '# **[' + biz_name + ']' + ding_title + '**\n----\n' + text + ' \n' + error_domain + ' \n' + text_7day + ' \n' + text_15day
            },
            "at": {
                "atMobiles": [
                ],
                "isAtAll": True
            }
        }

        send_message(bk_biz, tag='certificate', json=payload)
