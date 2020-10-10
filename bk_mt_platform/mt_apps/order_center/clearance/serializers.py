from rest_framework import serializers

from .models import ClearanceOrder


class ClearanceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceOrder
        fields = '__all__'
