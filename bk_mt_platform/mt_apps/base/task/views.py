# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework import serializers
from rest_framework.response import Response

from blueapps.account.decorators import login_exempt
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.task.job_manager import JobManager
from mt_apps.base.task.task_manager import TaskManager
from .models import JobModel, TaskInstanceModel
from .pagination import StandardResultsSetPagination
from .serializers import JobSerializer, TaskInstanceSerializer


class JobViewSet(ModelViewSet):
    queryset = JobModel.objects.all()
    serializer_class = JobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bk_biz', 'module', 'job_uuid']
    search_fields = ['id', 'title', 'exec_ip']
    ordering_fields = ['id', 'create_time']


class TaskInstanceViewSet(ModelViewSet):
    queryset = TaskInstanceModel.objects.all()
    serializer_class = TaskInstanceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'job__bk_biz', 'job__job_uuid', 'job__module']
    search_fields = ['id', 'user', 'job__title']
    ordering_fields = ['id', 'create_time']

    def get_queryset(self):
        queryset = TaskInstanceModel.objects.all()

        condtions = {}
        for field in self.filterset_fields:
            value = self.request.query_params.get(field)
            if value and field != "job__module":
                condtions[field] = value
            elif value and field == "job__module":
                data = [v.strip('/') for v in value.split(',')]
                condtions[field + '__in'] = data

        queryset = queryset.filter(**condtions)

        return queryset


class TaskViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def retrieve(self, request, *args, **kwargs):
        res = []

        if 'pk' in self.kwargs:
            job_uuid = self.kwargs["pk"]
            if job_uuid != '':
                try:
                    res = \
                        TaskInstanceModel.objects.values().filter(
                            job=JobModel.objects.get(bk_biz=4, job_uuid=job_uuid)).order_by(
                            '-id')[0]
                except:
                    pass

        return Response(res)

    def post(self, request, *args, **kwargs):
        job_uuid = 0

        if 'pk' in self.kwargs:
            if self.kwargs["pk"] != '':
                job_uuid = self.kwargs["pk"]

        taskManager = TaskManager(request)

        if 'bk_biz' in request.data:
            bk_biz = request.data["bk_biz"]
        else:
            bk_biz = 0

        if 'ip_list' in request.data:
            ip_list = request.data["ip_list"]
        else:
            ip_list = None

        if 'script_param' in request.data:
            script_param = request.data["script_param"]
        else:
            script_param = None

        if 'script_content' in request.data:
            script_content = request.data["script_content"]
        else:
            script_content = None

        if 'run_user' in request.data:
            run_user = request.data["run_user"]
        else:
            run_user = None

        if 'task_name' in request.data:
            task_name = request.data["task_name"]
        else:
            task_name = None

        return Response(
            taskManager.run_job(bk_biz, job_uuid, ip_list, script_param, script_content, run_user, task_name))


class LogViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def retrieve(self, request, *args, **kwargs):
        res = []

        if 'pk' in self.kwargs:
            if self.kwargs["pk"] != '':
                taskmanager = TaskManager(request)
                res = taskmanager.get_task_log(int(self.kwargs["pk"]))

        return Response(res)


class RegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        result = {u'message': u'', u'code': 0, u'data': [], 'result': False}

        if 'bk_biz' in request.data:
            bk_biz = request.data["bk_biz"]
            try:
                JobManager().biz_register(bk_biz)
            except Exception as e:
                result["message"] = str(e)

        return Response(result)


@login_exempt
@csrf_exempt
def CallbackViewSet(request):
    from blueking.component.shortcuts import get_client_by_user
    import datetime

    if request.method == 'GET':
        return HttpResponse('测试Callback：%s' % str(request.GET.dict()))
    elif request.method == 'POST':
        try:
            obj = json.loads(request.body)
            if 'job_instance_id' in obj:
                task = TaskInstanceModel.objects.get(instance=obj['job_instance_id'])
                client = get_client_by_user('wujiang')

                params = {
                    'bk_biz_id': task.job.bk_biz,
                    "job_instance_id": task.instance
                }

                print("检查到未完成的任务:" + str(params))

                result_status = client.job.get_job_instance_status(params)

                if result_status['data']['is_finished']:
                    print("检查到已完成的任务:" + str(params))
                    task.is_finished = result_status['data']['is_finished']
                    task.status = result_status['data']['job_instance']['status']
                    task.start_time = datetime.datetime.fromtimestamp(
                        result_status['data']['job_instance']['start_time'] / 1000,
                        datetime.timezone(datetime.timedelta(hours=0))).strftime("%Y-%m-%d %H:%M:%S")
                    task.end_time = datetime.datetime.fromtimestamp(
                        result_status['data']['job_instance']['end_time'] / 1000,
                        datetime.timezone(datetime.timedelta(hours=0))).strftime("%Y-%m-%d %H:%M:%S")
                    task.total_time = result_status['data']['job_instance']['total_time']

                    task.result_log = json.dumps(client.job.get_job_instance_log(params)['data'])

                    task.save()

                return HttpResponse('CallbackInstance ：%s' % str(task.instance))
        except Exception as e:
            print(str(e))
