from rest_framework import serializers

from .models import OrderConfig


class OrderConfigSerializer(serializers.ModelSerializer):
    process__process_name = serializers.CharField(read_only=True)
    process__process_type = serializers.CharField(read_only=True)
    process__process_steps = serializers.IntegerField(read_only=False)

    class Meta:
        model = OrderConfig
        fields = [
            'id', 'biz_id', 'order_type', 'order_name', 'ding_api', 'ding_token',
            'process_id', 'process__process_name',
            'process__process_type', 'process__process_steps'
        ]
