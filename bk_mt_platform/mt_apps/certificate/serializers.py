# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models  import CertModel,DomainModel,ClusterModel
from datetime import datetime


class CertSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    expired_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CertModel
        fields = "__all__"

class DomainSerializer(serializers.ModelSerializer):
    check_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',allow_null=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',allow_null=True)
    expired_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',allow_null=True)
    remain_days = serializers.SerializerMethodField()


    class Meta:
        model = DomainModel
        fields = "__all__"

    def get_remain_days(self, obj):
        if obj.expired_time:
            try:
                return (obj.expired_time - datetime.now()).days
            except:
                return None
        else:
            return None


class ClusterSerializer(serializers.ModelSerializer):
    domain_name = serializers.SerializerMethodField()
    cert_domain = serializers.SerializerMethodField()
    cert_name = serializers.SerializerMethodField()

    class Meta:
        model = ClusterModel
        fields = "__all__"

    def get_domain_name(self, obj):
        return obj.get_domain_name()

    def get_cert_domain(self, obj):
        return obj.get_cert_domain()

    def get_cert_name(self, obj):
        return obj.get_cert_name()
