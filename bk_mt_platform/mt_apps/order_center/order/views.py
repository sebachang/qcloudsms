import json
from base64 import b64decode

from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from blueapps.account.decorators import login_exempt
from mt_apps.base.api.components.login import LoginAPI
from mt_apps.base.app_fw.error_code import EC_COMMON_LOGIC_ERROR
from mt_apps.base.app_fw.exceptions import ParamError, CommonLogicError, PermissionError
from mt_apps.base.app_fw.viewsets import ModelViewSet, GenericViewSet
from mt_apps.base.permission.models import Group
from mt_apps.base.task.task_manager import TaskManager
from mt_apps.order_center.order_config.models import OrderConfig
from mt_apps.order_center.order_config.utils.order_config_interface import OrderConfigInterface
from mt_apps.order_center.process_config.models import ApprovalFlow
from mt_apps.order_center.process_config.utils import get_audit_user
from mt_apps.order_center.process_config.utils.process_config_interface import ProcessConfigInterface
from mt_apps.order_center.process_config.views import ApprovalFlowViewSet
from .celery_tasks import order_approval_notice
from .models import Orders, OrderApprovalRecord
from .pagination import OrderSetPagination
from .serializers import OrdersSerializer, OrderApprovalRecordSerializer
from .utils.order_interface import OrderInterfaceManagement, OrderInterface


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        import datetime
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class OrderViewSet(ModelViewSet):
    queryset = Orders.objects.annotate(
        order_type=F('order_config__order_type'),
        order_name=F('order_config__order_name'),
        process_steps=F('order_config__process__process_steps'),
    ).values(
        'id', 'order_config_id', 'submitter', 'biz_id', 'suborder', 'order_state',
        'create_time', 'update_time', 'order_type', 'order_name', 'current_approval_step', 'process_steps'
    )

    serializer_class = OrdersSerializer
    pagination_class = OrderSetPagination

    # 获取所有工单, 可以传入order_state 来显示不同状态
    def filter_queryset(self, queryset):

        if self.request.method == 'GET':
            order_state = self.request.GET.get('order_state')
            biz_id = self.request.GET.get('biz_id')

            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取工单时未传递biz_id或biz_id为负值")

            if order_state is None:
                return queryset.filter(biz_id=biz_id).order_by("-id")

            return queryset.filter(order_state=order_state).filter(biz_id=biz_id).order_by("-id")

        return Orders.objects.all()

    # 创建工单和子工单
    def create(self, request, *args, **kwargs):

        order_type = request.data['order_type']
        biz_id = request.data['biz_id']
        result = OrderConfigInterface.order_type_get_create_order_auditor(
            order_type, biz_id)
        print(result)
        if self.request.user.__str__() not in result:
            raise PermissionError()

        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()

        if not order_obj:
            raise ParamError(u"参数%s类型未注册" % (order_type))

        result = order_obj.order_type_get_order_config(
            order_obj.order_type, biz_id)
        order_config_id = result.get('id', None)
        process_id = result.get('process_id', None)

        approval_flow_list = order_obj.get_approval_flow_list(process_id)

        if len(approval_flow_list) == 0:
            raise CommonLogicError({"message": u"未生成工单配置", "code": 50000})

        try:
            with transaction.atomic():
                if not hasattr(order_obj, 'create_suborder'):
                    raise CommonLogicError(
                        {"message": u"创建子订单失败", "code": 50000})

                sub_order = order_obj.create_suborder(
                    **request.data['sub_order'])
                current_approval_step = 0
                order_state = 1
                request.data['order_config_id'] = order_config_id
                request.data['submitter'] = request.user.__str__()
                request.data['suborder'] = sub_order
                request.data['current_approval_step'] = current_approval_step
                request.data['order_state'] = order_state

                data = super(OrderViewSet, self).create(request)
                order_id = data.data.get('id', '')

                if hasattr(order_obj, 'create_detail'):
                    order_obj.create_detail(
                        order_id, **request.data['sub_order'])

                for i in list(approval_flow_list):

                    if i['step'] == 0:
                        auditor = request.user.__str__()
                        approval_step_result = 2
                        OrderApprovalRecord.objects.create(
                            auditor=auditor, approval_step=current_approval_step,
                            approval_step_result=approval_step_result,
                            order_id=order_id)
                        continue

                    if i['step_flag'] == 0:
                        break
                    else:
                        auditor = 'administrator'
                        current_approval_step = i['step']
                        approval_step_result = 3

                    OrderApprovalRecord.objects.create(
                        auditor=auditor, approval_step=current_approval_step,
                        approval_step_result=approval_step_result,
                        order_id=order_id)

                order_state = 0 if current_approval_step == len(
                    approval_flow_list) - 1 else order_state

                OrderInterface.update_order_state_current_approval_step(order_id, order_state,
                                                                        current_approval_step)

                if list(approval_flow_list)[0]['task_flag'] == 0:
                    task_id = list(approval_flow_list)[0]['task_id']
                    taskManager = TaskManager(request)

                    task_instance_id = 0
                    jobs_state = 0
                    script_param = None
                    if hasattr(order_obj, 'script_param'):
                        script_param = order_obj.script_param(order_id)
                    try:
                        job_result = taskManager.run_job(
                            request.data['biz_id'], task_id, script_param=script_param
                        )
                        job_data = job_result.get('data', {})
                        if job_data is not None:
                            task_instance_id = job_data.get('task_instance_id', 0)
                        else:
                            jobs_state = 4

                        OrderApprovalRecord.objects.filter(
                            approval_step=0, order_id=order_id
                        ).update(task_instance_id=task_instance_id, jobs_state=jobs_state)
                    except Exception as e:
                        raise CommonLogicError({'message':f'执行任务失败:{e.__str__()}', 'code': -1})

        except Exception as e:
            raise e
        else:
            order_approval_notice.delay(order_id)
        return data

    # 撤销工单
    def update(self, request, *args, **kwargs):

        order_id = request.path_info.split('/')[-2]
        if isinstance(order_id, int) or int(order_id) < 0:
            raise ParamError(u"更新工单未传递order_id")
        request.data.clear()

        result = self.queryset.filter(id=order_id).first()
        if result.get('submitter') != request.user.__str__():
            raise PermissionError(u"撤销工单权限错误")

        if result.get('order_state') != 1:
            raise CommonLogicError({"message": u"工单不是审批状态", "code": 50000})
        request.data['order_config_id'] = result.get('order_config_id')
        request.data['submitter'] = result.get('submitter')
        request.data['biz_id'] = result.get('biz_id')
        request.data['suborder'] = result.get('suborder')
        request.data['order_state'] = 3
        try:
            with transaction.atomic():
                # result = OrderInterface.order_id_get_order_info(order_id)
                order_type = result.get('order_type')
                order_obj = OrderInterfaceManagement(
                    order_type).get_register_order_class()

                if not order_obj:
                    raise ParamError(u"%s类型未注册" % (order_type))

                if hasattr(order_obj, 'cancel_order'):
                    order_obj.cancel_order(order_id)

                data = super(OrderViewSet, self).update(
                    request, *args, **kwargs)

        except Exception as e:
            raise e

        return data


class MyOrderViewSet(OrderViewSet):

    # 获取自己提交工单
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取工单时未传递biz_id或biz_id为负值")

            return queryset.filter(submitter=self.request.user.__str__()).filter(biz_id=biz_id).order_by("-id")


class MyApprovalOrderViewSet(OrderViewSet):

    # 获取自己的审批工单
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取工单时未传递biz_id或biz_id为负值")
            user = self.request.user.__str__()
            sql = (f'SELECT a.id, c.audit_type, c.auditor FROM '
                   f'order_center_order_orders a '
                   f'LEFT JOIN {OrderConfig._meta.db_table} b ON a.order_config_id = b.id '
                   f'LEFT JOIN {ApprovalFlow._meta.db_table} c ON c.process_id = b.process_id '
                   f'WHERE '
                   f'a.current_approval_step + 1 = c.step ')

            user_groups = set()
            order_ids = []
            for g in Group.objects.all():
                try:
                    users = json.loads(g.users)
                    if user in users:
                        user_groups.add(g.id)
                except ...:
                    pass
            for x in queryset.raw(sql):
                if x.audit_type == 1:
                    if user in x.auditor.split(','):
                        order_ids.append(x.id)
                elif x.audit_type == 2:
                    if len(set([int(i) for i in x.auditor.split(',')]) & user_groups) > 0:
                        order_ids.append(x.id)
                pass
            return queryset.filter(id__in=order_ids,
                                   order_state=1, biz_id=biz_id).order_by("-id")


class ExceptionOrderViewSet(OrderViewSet):

    # 获取作业失败工单
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise ParamError(u"获取工单时未传递biz_id或biz_id为负值")

            result_api = LoginAPI.get_batch_user_info(
                self.request, **{"bk_username_list": self.request.user.__str__()})
            if result_api['data'][self.request.user.__str__()]['bk_role'] != 1:
                return queryset.none()

            return queryset.filter(biz_id=biz_id, orderapprovalrecord__jobs_state__gt=3).order_by("-id")


class SearchOrderViewSet(ModelViewSet):
    # 获取搜索工单
    queryset = Orders.objects.annotate(
        order_type=F('order_config__order_type'),
        order_name=F('order_config__order_name'),
        process_steps=F('order_config__process__process_steps'),
    ).values(
        'id', 'order_config_id', 'submitter', 'biz_id', 'suborder', 'order_state',
        'create_time', 'update_time', 'order_config', 'order_name', 'current_approval_step', 'process_steps'
    )
    serializer_class = OrdersSerializer
    pagination_class = OrderSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['$id', '$order_config__order_type',
                     '$order_config__order_name', '$submitter']
    filterset_fields = ['biz_id']
    ordering_fields = ['id']


class SubOrderInfoViewSet(GenericViewSet):
    # 获取子工单信息
    @action(methods=['get'], detail=False, url_path='suborder')
    def get_suborder(self, request):

        order_id = request.GET.get('order_id')
        if order_id is None or int(order_id) < 0:
            raise ParamError(u"获取子工单时未传递order_id或order_id为负值")

        result = OrderInterface.order_id_get_order_info(order_id)
        order_type = result.get('order_type', None)
        suborder_id = result.get('suborder', None)

        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()
        if not order_obj:
            raise ParamError(u"参数%s类型未注册" % (order_type))

        suborder_data = order_obj.get_suborder(
            suborder_id) if hasattr(order_obj, 'get_suborder') else {}

        return Response(suborder_data)


class OrderApprovalRecordViewSet(ModelViewSet):
    queryset = OrderApprovalRecord.objects.all()
    serializer_class = OrderApprovalRecordSerializer

    # 获取我的审批工单记录
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            order_id = self.request.GET.get('order_id')
            if order_id is None or int(order_id) < 0:
                raise ParamError(u"获取工单时未传递order_id或order_id为负值")

            return queryset.filter(order_id=order_id).order_by("id")

    # 工单审批, 创建审批记录, 更新工单状态，生成任务实例
    def create(self, request, *args, **kwargs):

        order_id = request.data.get('order_id', None)
        approval_step_result = request.data.get('approval_step_result', None)
        approval_step_remark = request.data.get('approval_step_remark', '')

        if order_id is None or int(order_id) < 0:
            raise ParamError(u"审批工单未传递order_id")

        if approval_step_result is None or int(approval_step_result) < 0 or int(approval_step_result) > 1:
            raise ParamError(
                u"审批工单未传递approval_step_result或者approval_step_result参数错误")

        result = OrderInterface.order_id_get_order_info(order_id)
        order_type = result.get('order_type', None)
        order_state = result.get('order_state', None)
        current_approval_step = result.get('current_approval_step', None)
        process_id = result.get('order_config__process_id', None)
        biz_id = result.get('biz_id', None)

        if order_state != 1:
            raise CommonLogicError({"message": u"工单不是审批状态", "code": 50000})

        result = ProcessConfigInterface.get_order_next_approval_flow(
            process_id, current_approval_step)
        auditors = get_audit_user(result.get(
            'audit_type', 1), result.get('auditor', ''))
        task_id = result.get('task_id', None)
        task_flag = result.get('task_flag', None)

        if request.user.__str__() not in auditors:
            raise PermissionError()

        taskManager = TaskManager(request)

        # 工单任务之间透传参数， 功能先注释掉
        # job_params = {}
        # for x in OrderInterface.order_id_get_order_approval_record_list(order_id):
        #
        #     if x.task_instance_id:
        #         result = taskManager.get_task_status(x.task_instance_id)
        #
        #         if not result.get('is_finished', False):
        #             raise CommonLogicError({"message": u"工单作业未完成，请查看详情", "code": 50000})
        #         if result.get('status') != 3:
        #             x.jobs_state = result.get('status')
        #             x.save()
        #             raise CommonLogicError({"message": u"工单作业失败，请查看详情", "code": 50000})
        #         else:
        #             def get_task_result(log_content):
        #                 pattern = re.compile(r'{[\'|\"]job_params.*}$')
        #                 res = re.search(pattern, log_content)
        #                 if res:
        #                     return res.group()
        #                 return '{}'
        #
        #             job_params = {
        #                 x['ip']: json.loads(get_task_result(x['log_content']))
        #                 for x in taskManager.get_task_log(x.task_instance_id)[0]['step_results'][0]["ip_logs"]
        #             }
        #             x.task_response, x.jobs_state = job_params, result.get('status')
        #             x.save()
        #
        #         break

        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()

        if not order_obj:
            raise ParamError(u"%s类型未注册" % (order_type))

        script_param = None
        if hasattr(order_obj, 'script_param'):
            script_param = order_obj.script_param(order_id)

            # 工单任务之间透传参数， 功能先注释掉
            # script_param.update({"job": job_params})
            # script_param = json.dumps(script_param, cls=DateEncoder)

        task_instance_id = 0
        jobs_state = 0
        if task_flag == 0 and approval_step_result == 0:
            job_result = taskManager.run_job(
                biz_id, task_id, script_param=script_param)
            job_data = job_result.get('data', {})
            if job_data:
                task_instance_id = job_data.get('task_instance_id', 0)
            else:
                jobs_state = 4

        approval_flow_list = ProcessConfigInterface.get_approval_flow_list(
            process_id)
        if len(approval_flow_list) == 0:
            raise CommonLogicError({"message": u"未生成工单配置", "code": 50000})

        current_approval_step = current_approval_step + 1
        request.data['order'] = order_id
        request.data['auditor'] = request.user.__str__()
        request.data['approval_step'] = current_approval_step
        request.data['approval_step_result'] = approval_step_result
        request.data['approval_step_remark'] = approval_step_remark
        request.data['task_instance_id'] = task_instance_id
        request.data['jobs_state'] = jobs_state
        request.data['task_response'] = '{}'
        try:
            with transaction.atomic():
                if approval_step_result == 0:
                    order_state = 1
                    data = super(OrderApprovalRecordViewSet,
                                 self).create(request)
                    if current_approval_step != len(approval_flow_list) - 1:

                        for i in list(approval_flow_list)[current_approval_step + 1:]:
                            if i['step_flag'] == 0:
                                break
                            else:
                                current_approval_step = i['step']
                                request.data['auditor'] = 'administrator'
                                request.data['approval_step'] = i['step']
                                request.data['approval_step_result'] = 3
                                request.data['approval_step_remark'] = ''
                                request.data['task_instance_id'] = 0

                                data = super(
                                    OrderApprovalRecordViewSet, self).create(request)

                    order_state = 0 if current_approval_step == len(
                        approval_flow_list) - 1 else order_state

                else:
                    order_state = 2
                    data = super(OrderApprovalRecordViewSet,
                                 self).create(request)

                OrderInterface.update_order_state_current_approval_step(
                    order_id, order_state, current_approval_step)

        except Exception as e:
            raise CommonLogicError({"message": e, "code": 50000})
        else:

            order_approval_notice.delay(order_id)

        return data


class OrderApprovalPermissionViewSet(GenericViewSet):
    # 获取下个阶段审批是否有权限
    @action(methods=['get'], detail=False, url_path='approval/permission')
    def get_order_permission_api(self, request):

        order_id = request.GET.get('order_id')
        if order_id is None or int(order_id) < 0:
            raise ParamError(u"获取审批权限未传递order_id")

        result = OrderInterface.order_id_get_order_info(order_id)
        current_approval_step = result.get('current_approval_step', None)
        process_id = result.get('order_config__process_id', None)

        result = ProcessConfigInterface.get_order_next_approval_flow(
            process_id, current_approval_step)

        data = {"permission": False}
        if request.user.__str__() not in result.get('auditor', '').split(','):
            return Response(data)

        data = {"permission": True}
        return Response(data)


class OrderApprovalFlowViewSet(ApprovalFlowViewSet):

    # 获取工单审批流程
    def filter_queryset(self, queryset):
        if self.request.method == 'GET':
            order_id = self.request.GET.get('order_id')
            if order_id is None or int(order_id) < 0:
                raise ParamError(u"获取工单审批流程时未传递order_id或order_id为负值")

            result = OrderInterface.order_id_get_order_config(order_id)
            process_id = result.get('order_config__process_id', None)

            return queryset.filter(process_id=process_id).order_by("step")

        return queryset


class OrderJobReExecuteViewSet(GenericViewSet):
    # 重新执行JOB
    @action(methods=['post'], detail=False, url_path='job/execute')
    def post_job_execute_api(self, request):

        order_id = request.data.get('order_id', None)
        if order_id is None or int(order_id) < 0:
            raise ParamError(u"未传递order_id")

        task_instance_id = request.data.get('task_instance_id', None)
        if task_instance_id is None or int(task_instance_id) < 0:
            raise ParamError(u"未传递task_instance_id")

        result_obj = OrderInterface.order_id_get_order_approval_record_list(
            order_id)

        approval_step = None
        for x in result_obj.order_by('approval_step'):

            if x.task_instance_id == int(task_instance_id):
                approval_step = x.approval_step
                x.jobs_state = 0
                x.save()
                break

        # 工单任务之间透传参数， 功能先注释掉
        # back_task_response = result_obj.filter(
        #     approval_step=approval_step-1).values().first().get('task_response', {}) if approval_step > 0 else {}

        result = OrderInterface.order_id_get_order_info(order_id)
        order_type = result.get('order_type', None)
        process_id = result.get('order_config__process_id', None)
        biz_id = result.get('biz_id', None)

        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()

        if not order_obj:
            raise ParamError(u"%s类型未注册" % (order_type))

        script_param = {}
        if hasattr(order_obj, 'script_param'):
            script_param = order_obj.script_param(order_id)

            # 工单任务之间透传参数， 功能先注释掉
            # script_param.update({"job": back_task_response})
            # script_param = json.dumps(script_param, cls=DateEncoder)

        result = ProcessConfigInterface.get_approval_flow_list(
            process_id).filter(step=approval_step).first()
        task_id = result.get('task_id', None)

        try:
            with transaction.atomic():

                taskManager = TaskManager(request)
                task_instance_id = 0
                jobs_state = 0
                job_result = taskManager.run_job(
                    biz_id, task_id, script_param=script_param
                )
                job_data = job_result.get('data', {})
                if job_data:
                    task_instance_id = job_data.get('task_instance_id', 0)
                else:
                    raise CommonLogicError({'message': job_result.get(
                        'message', ''), 'code': EC_COMMON_LOGIC_ERROR})

                result = result_obj.filter(
                    order_id=order_id, approval_step=approval_step).first()
                result.task_instance_id = task_instance_id
                result.jobs_state = jobs_state
                result.save()

        except Exception as e:
            raise e

        data = {"job": True}
        return Response(data)


class OrderScriptParamViewSet(GenericViewSet):
    # 获取订单参数
    @action(methods=['get'], detail=False, url_path='script/param')
    def get_order_script_param_api(self, request):

        order_id = request.GET.get('order_id')
        if order_id is None or int(order_id) < 0:
            raise ParamError(u"获取审批权限未传递order_id")

        result = OrderInterface.order_id_get_order_info(order_id)

        order_type = result.get('order_type', None)
        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()

        if not order_obj:
            raise ParamError(u"%s类型未注册" % (order_type))

        script_param = order_obj.script_param(
            order_id) if hasattr(order_obj, 'script_param') else {}

        return Response(script_param)


@login_exempt
def script_param(request, pk=None):
    result = OrderInterface.order_id_get_order_info(pk)
    if result:
        order_type = result.get('order_type', None)

        order_obj = OrderInterfaceManagement(
            order_type).get_register_order_class()

        if not order_obj:
            raise ParamError(u"%s类型未注册" % (order_type))

        script_param = order_obj.script_param(pk) if hasattr(
            order_obj, 'script_param') else None

        data = {}

        if script_param:
            data = json.loads(b64decode(script_param.encode()).decode())

        return JsonResponse(data)
    else:
        return JsonResponse({})
