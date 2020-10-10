# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""

import json

import requests
from celery.schedules import crontab
from celery.task import periodic_task


# @task()
# def async_task(x, y):
#     """
#     定义一个 celery 异步任务
#     """
#     logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
#     return x + y


# def execute_task():
#     """
#     执行 celery 异步任务
#
#     调用celery任务方法:
#         task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
#         task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
#         delay(): 简便方法，类似调用普通函数
#         apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
#                       详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
#     """
#     now = datetime.datetime.now()
#     logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
#     # 调用定时任务
#     async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


# def get_time():
#     """
#     celery 周期任务示例
#
#     run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
#     periodic_task：程序运行时自动触发周期任务
#     """
#     execute_task()
#     now = datetime.datetime.now()
#     logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def update_task_status():
    from mt_apps.base.task.models import TaskInstanceModel
    from blueking.component.shortcuts import get_client_by_user

    job_status = {1: '未执行', 2: '正在执行', 3: '执行成功', 4: '执行失败', 5: '跳过', 6: '忽略错误', 7: '等待用户', 8: '手动结束', 9: '状态异常',
                  10: '步骤强制终止中', 11: '步骤强制终止成功', 12: '步骤强制终止失败'}

    client = get_client_by_user('admin')

    for objs in TaskInstanceModel.objects.filter(is_finished=False):
        params = {
            'bk_biz_id': objs.job.bk_biz,
            "job_instance_id": objs.instance
        }

        print("检查到未完成的任务:" + str(params))

        result_status = client.job.get_job_instance_status(params)

        if result_status['data']['is_finished']:
            print("检查到已完成的任务:" + str(params))
            objs.is_finished = result_status['data']['is_finished']
            objs.status = result_status['data']['job_instance']['status']
            objs.start_time = ' '.join(result_status['data']['job_instance']['start_time'].split(' ')[0:2])
            objs.end_time = ' '.join(result_status['data']['job_instance']['end_time'].split(' ')[0:2])
            objs.total_time = result_status['data']['job_instance']['total_time']

            objs.result_log = json.dumps(client.job.get_job_instance_log(params)['data'])

            objs.save()

            if objs.job.callback != None and objs.job.callback != "":
                url = objs.job.callback
                print('检查到任务回调:' + url)
                try:
                    num = 0
                    body = {"taskinstance_id": objs.id, "job_status": objs.status}
                    headers = {'content-type': "application/json"}

                    while num < 2:
                        response = requests.post(url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            print('执行回调:' + url + ' 成功!')
                            break
                        else:
                            print('执行回调:' + url + ' 失败:' + str(num) + '次,返回值:' + str(response.status_code))
                            num += 1
                except:
                    print('回调地址:' + url + ' 错误,请联系管理员!')
