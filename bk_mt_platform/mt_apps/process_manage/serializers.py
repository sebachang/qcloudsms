from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import *


class ProcessSerializer(serializers.ModelSerializer):
    instance_set = serializers.StringRelatedField(many=True, read_only=True)
    template_name = serializers.StringRelatedField(
        read_only=True, source="template.name")

    class Meta:
        model = Process
        fields = '__all__'


class InstanceSerializer(serializers.ModelSerializer):
    process_obj = ProcessSerializer(read_only=True, source='process')
    config = ReadOnlyField(source='get_config')
    config_md5 = ReadOnlyField(source='get_config_md5')

    class Meta:
        model = Instance
        fields = '__all__'


class MachineField(serializers.ReadOnlyField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        if ':' not in value:
            return '0:' + value
        return value


class TrivialInstanceSerializer(serializers.ModelSerializer):
    machine_full = MachineField(source='machine')

    class Meta:
        model = Instance
        fields = ['id', 'biz_id', 'machine', 'machine_full', 'desc',
                  'work_dir', 'launch_user', 'pid_path']
