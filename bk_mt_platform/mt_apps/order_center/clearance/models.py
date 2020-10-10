from django.db import models


class ClearanceOrder(models.Model):
    remove_id = models.CharField(max_length=255, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_center_clearance_clearance_order"
