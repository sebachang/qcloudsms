from rest_framework import serializers

from .models import Orders, OrderApprovalRecord


class OrdersSerializer(serializers.ModelSerializer):
    order_type = serializers.CharField(read_only=True)
    order_name = serializers.CharField(read_only=True)
    # current_approval_step = serializers.IntegerField(read_only=True)
    order_config_id = serializers.IntegerField(read_only=False)
    process_steps = serializers.IntegerField(read_only=True)

    # order_name = serializers.ReadOnlyField()
    # order_name = serializers.ReadOnlyField()
    # order_type = serializers.ReadOnlyField()
    # order_type = serializers.SerializerMethodField()
    # order_name = serializers.SerializerMethodField()
    # order_type_id

    class Meta:
        model = Orders

        fields = [
            'id', 'order_config_id', 'submitter', 'biz_id', 'suborder', 'order_state', 'current_approval_step',
            'create_time', 'update_time', 'order_type', 'order_name', 'process_steps'
        ]

    # def get_order_type(self, obj):
    #
    #     return obj.get('order_type')
    #
    # def get_order_name(self, obj):
    #
    #     return obj.get('order_name')


class OrderApprovalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderApprovalRecord
        fields = '__all__'
