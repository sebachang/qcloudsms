from rest_framework import serializers

from .models import DeliverOrder


class DeliverOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverOrder
        fields = '__all__'
