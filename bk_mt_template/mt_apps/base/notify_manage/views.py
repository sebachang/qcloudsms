from rest_framework.decorators import action
from rest_framework.response import Response

from mt_apps.base.app_fw.decorators import filter_biz_id
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.notify_manage.constants import Tags
from .serializers import *


class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    @filter_biz_id
    def filter_queryset(self, queryset):
        return queryset

    pass


class RuleViewSet(ModelViewSet):
    queryset = NotifyRule.objects.all()
    serializer_class = NotifyRuleSerializer

    @filter_biz_id
    def filter_queryset(self, queryset):
        return queryset


class TagViewSet(GenericViewSet):
    @action(methods=['get'], detail=False)
    def taglist(self, request):
        return Response([{'key': v[0], 'name': v[1]} for v in Tags])
