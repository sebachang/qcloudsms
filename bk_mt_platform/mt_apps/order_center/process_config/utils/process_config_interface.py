from enum import Enum, unique

from mt_apps.base.task.job_manager import JobManager
from ..models import ProcessConfig as processConfig, ApprovalFlow

'''
流程枚举类型, 保证唯一
    ProcessType.module_1.name = "module_1"
    ProcessType.module_1.value = 1
'''


@unique
class ProcessType(Enum):
    deliver = 1
    release = 2
    clearance = 3
    domain = 4


class ProcessConfigInterface(object):
    # 其他业务使用接口
    @classmethod
    def register(cls, biz_id, process_type, process_name, process_steps, job_type, job_title):
        # 检查是否已存在, 基于biz_id, process_type
        result = processConfig.objects.filter(biz_id=biz_id, process_type=process_type).first()
        if result is None:
            result = processConfig.objects.create(biz_id=biz_id, process_type=process_type, process_name=process_name,
                                                  process_steps=process_steps)

        # 执行流程步骤
        cls.exec_approval_flow(biz_id, result.id, process_steps, job_type, job_title)
        return result.id

    # 基于传进来的step个数, 增删表格记录和对应task记录
    @classmethod
    def exec_approval_flow(cls, biz_id, process_id, process_steps, job_type, job_title):
        begin = ApprovalFlow.objects.filter(process_id=process_id).count()
        if begin == 0:
            ApprovalFlow.objects.create(
                process_id=process_id,
                step=0,
                step_name='工单提交',
                audit_type=1,
                auditor='',
                step_flag=0,
                description='',
                task_id=JobManager.register(biz_id, job_title + " - 提单", job_type)
            )
        for i in range(begin + 1, process_steps + 1):
            ApprovalFlow.objects.create(
                process_id=process_id,
                step=i,
                step_name='',
                audit_type=1,
                auditor='',
                step_flag=0,
                description='',
                task_id=JobManager.register(biz_id, job_title + " - 步骤" + str(i), job_type)
            )

    @classmethod
    def get_approval_flow_list(cls, process_id):
        result = ApprovalFlow.objects.filter(process_id=process_id).values().order_by('step')
        return result

    @classmethod
    def get_order_next_approval_flow(cls, process_id, current_approval_step):
        result = ApprovalFlow.objects.filter(
            process_id=process_id,
            step=current_approval_step + 1).values().first()
        result = {} if result is None else result
        return result
