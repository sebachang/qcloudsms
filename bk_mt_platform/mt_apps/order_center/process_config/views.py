from mt_apps.base.app_fw.exceptions import ParamError
from mt_apps.base.app_fw.viewsets import ModelViewSet
from .models import ProcessConfig, ApprovalFlow
from .pagination import ProcessConfigSetPagination
from .serializers import ProcessManagementSerializer, ApprovalFlowSerializer


# 流程表操作
class ProcessConfigViewSet(ModelViewSet):
    queryset = ProcessConfig.objects.all()
    serializer_class = ProcessManagementSerializer
    pagination_class = ProcessConfigSetPagination

    def filter_queryset(self, queryset):

        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取订单时未传递biz_id或biz_id为负值")

            return queryset.filter(biz_id=biz_id)

        return queryset


# 审批表操作
class ApprovalFlowViewSet(ModelViewSet):
    queryset = ApprovalFlow.objects.all()
    serializer_class = ApprovalFlowSerializer

    def filter_queryset(self, queryset):

        if self.request.method == 'GET':
            process_id = self.request.GET.get('process_id')
            if process_id is None or int(process_id) < 0:
                raise ParamError(u"未传递approval_id或approval_id为负值")
            return queryset.filter(process_id=process_id).order_by("step")

        return queryset
