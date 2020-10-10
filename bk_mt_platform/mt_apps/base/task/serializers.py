# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import JobModel, TaskInstanceModel
from .task_manager import TaskManager


class JobSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = JobModel
        fields = "__all__"


class TaskInstanceSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    job_name = serializers.SerializerMethodField()
    # job_type = serializers.SerializerMethodField()
    job_result = serializers.SerializerMethodField()

    class Meta:
        model = TaskInstanceModel
        # fields = "__all__"
        exclude = ['result_log']

    def get_job_name(self, obj):
        return obj.get_job_name()

    # def get_job_type(self, obj):
    #     return obj.get_job_type()

    def get_job_result(self, obj):
        taskManager = TaskManager(self.context['request'])
        data = taskManager.get_task_status(obj.id)
        if obj.is_finished == False and data["is_finished"]:
            obj.is_finished = data["is_finished"]
            obj.status = data["status"]
            obj.start_time = data["start_time"]
            obj.end_time = data["end_time"]
            obj.total_time = data["total_time"]
        else:
            if obj.start_time:
                obj.start_time = obj.start_time.strftime("%Y-%m-%d %H:%M:%S")
            if obj.end_time:
                obj.end_time = obj.end_time.strftime("%Y-%m-%d %H:%M:%S")

        return []
