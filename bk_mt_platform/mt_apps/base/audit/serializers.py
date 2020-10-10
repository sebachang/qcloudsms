import django_filters
from django.db.models import Q
from rest_framework import serializers

from mt_apps.base.audit.auditlog.models import LogEntry


class ChangelogSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    action = serializers.ReadOnlyField(source='get_action_display')

    class Meta:
        model = LogEntry
        fields = ('timestamp', 'object_repr', 'action', 'changes', 'actor', 'additional_data')


def biz_id_match_or_empty(queryset, name, value):
    return queryset.filter(Q(**{name: value}) | Q(**{name: 0}))


class DateRangeFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(field_name='timestamp', lookup_expr=('gte'), )
    end = django_filters.DateFilter(field_name='timestamp', lookup_expr=('lte'), )
    biz_id = django_filters.NumberFilter(field_name='biz_id', method=biz_id_match_or_empty)

    class Meta:
        model = LogEntry
        fields = ['timestamp', 'biz_id']
