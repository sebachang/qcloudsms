from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer

from .models import Channel, NotifyRule


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class DestinationField(RelatedField):
    def to_representation(self, value):
        return value.name


class NotifyRuleSerializer(ModelSerializer):
    dest_name = DestinationField(source='destination', many=True, read_only=True)

    class Meta:
        model = NotifyRule
        fields = '__all__'
