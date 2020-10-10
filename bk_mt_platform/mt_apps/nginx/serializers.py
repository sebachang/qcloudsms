# -*- coding: utf-8 -*-

from rest_framework import serializers

from mt_apps.nginx.models import ConfigModel, VhostModel, ClusterModel


class ConfigModelSerializer(serializers.ModelSerializer):
    cert_data = serializers.SerializerMethodField()
    cluster_data = serializers.SerializerMethodField()
    vhosts = serializers.SerializerMethodField()

    class Meta:
        model = ConfigModel
        fields = "__all__"

    def get_cert_data(self, obj):
        return obj.getCertData()

    def get_cluster_data(self, obj):
        return obj.getCluster()

    def get_vhosts(self, obj):
        return obj.getVhosts()


class VhostModelSerializer(serializers.ModelSerializer):
    domain_data = serializers.SerializerMethodField()
    config_name = serializers.SerializerMethodField()

    class Meta:
        model = VhostModel
        fields = "__all__"

    def get_domain_data(self, obj):
        return obj.getDomainData()

    def get_config_name(self, obj):
        return obj.getConfigName()


class ClusterModelSerializer(serializers.ModelSerializer):
    config_name = serializers.SerializerMethodField()

    class Meta:
        model = ClusterModel
        fields = "__all__"

    def get_config_name(self, obj):
        return obj.getConfigName()
