from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from mt_apps.base.audit.impls import add_log_entry
from .auditlog.models import LogEntry
from .serializers import ChangelogSerializer, DateRangeFilter
from ..app_fw.viewsets import ModelViewSet


class ChangelogViewSet(ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = ChangelogSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = DateRangeFilter

    def add_log(self, request):
        biz_id = request.GET.get('biz_id')
        data = request.data
        kwargs = {}
        if 'changes' in data:
            kwargs['changes'] = data['changes']
        add_log_entry(biz_id, data['object_name'], data['addition_data'], **kwargs)
        return Response({})
