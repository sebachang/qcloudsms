from rest_framework import serializers
from rest_framework.fields import JSONField

from .models import ProcessConfig, ApprovalFlow


class ProcessManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessConfig
        fields = '__all__'


class ApprovalFlowSerializer(serializers.ModelSerializer):
    audit_name = JSONField(source='get_audit_user')

    class Meta:
        model = ApprovalFlow
        fields = '__all__'
