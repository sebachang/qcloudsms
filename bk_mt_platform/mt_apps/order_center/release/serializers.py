from rest_framework import serializers

from .models import ReleaseOrder
from .models import ServerModel


class ServerModelSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    class Meta:
        model = ServerModel
        fields = "__all__"

    def get_group(self, obj):
        division = obj.division.strip()
        if division != "":
            return int(division.split('.')[2]) % 1000
        else:
            return None


class ReleaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseOrder
        fields = '__all__'


class appVersionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
