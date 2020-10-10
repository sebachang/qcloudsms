# -*- coding: utf-8 -*-
import json
from base64 import b64encode

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from blueking.component.shortcuts import get_client_by_request
from mt_apps.base.app_fw.error_code import EC_COMMON_LOGIC_ERROR
from mt_apps.base.app_fw.exceptions import CommonLogicError
from mt_apps.base.system_config.config_define import get_system_config
from .models import JobModel, TaskInstanceModel


class TaskManager:
    def __init__(self, request, user=None, client=None):
        if request is not None:
            self.user = request.user
            self.client = get_client_by_request(request)
        else:
            self.user = user
            self.client = client

    def run_job(self, bk_biz, job_uuid, ip_list=None, script_param=None, script_content=None, run_user=None,
                task_name=None):
        result = {u'message': u'', u'code': -1, u'data': [], 'result': False}

        script_params = {
            "account": '',
            'script_content': '',
            'ip_list': []
        }

        params = {
            'bk_biz_id': int(bk_biz)
        }
        obj = {}
        try:
            obj = JobModel.objects.values('title', 'exec_ip', 'username', 'script', 'callback').get(
                bk_biz=int(bk_biz),
                job_uuid=job_uuid)
        except ObjectDoesNotExist as e:
            raise CommonLogicError({'code': EC_COMMON_LOGIC_ERROR, 'message': f'找不到作业{job_uuid}，请检查作业是否已注册'})

        params["bk_callback_url"] = get_system_config(int(bk_biz), 'task_callback_url')

        params = dict(params, **script_params)

        if run_user:
            params["account"] = run_user
        else:
            params["account"] = obj["username"]

        if script_content:
            try:
                script_content = script_content.encode()
            except ...:
                pass
            script_content = b64encode(script_content).decode()
            params["script_content"] = script_content
        else:
            params["script_content"] = obj["script"]

        if ip_list:
            try:
                params["ip_list"] = json.loads(ip_list)
            except:
                params["ip_list"] = []
                exec_ip_list = ip_list.split(',')
                for ip in exec_ip_list:
                    ip_obj = ip.split(':')
                    if len(ip_obj) == 2:
                        params["ip_list"].append({"bk_cloud_id": ip_obj[0], "ip": ip_obj[1]})
                    else:
                        params["ip_list"].append({"bk_cloud_id": 0, "ip": ip})
        else:
            params["ip_list"] = json.loads(obj["exec_ip"])

        if script_param:
            try:
                script_param = script_param.encode()
            except ...:
                pass
            script_param = b64encode(script_param).decode()
            params["script_param"] = script_param

        if not params['ip_list']:
            raise CommonLogicError({'code': -500, 'message': u"作业<" + job_uuid + " - " + obj['title'] + ">: 执行IP未配置"})

        if not params['account']:
            raise CommonLogicError({'code': -500, 'message': u"作业<" + job_uuid + " - " + obj['title'] + ">: 执行用户未配置"})

        if not params['script_content']:
            raise CommonLogicError({'code': -500, 'message': u"作业<" + job_uuid + " - " + obj['title'] + ">: 执行脚本内容未配置"})

        try:
            result = self.client.job.fast_execute_script(params)
            # else:
            #     params = dict(params, **job_params)
            #     params["bk_job_id"] = obj["bk_job_id"]
            #
            #     result = self.client.job.execute_job(params)

            if result["result"]:
                result_status = self.client.job.get_job_instance_status(
                    {'bk_biz_id': bk_biz, 'job_instance_id': result['data']['job_instance_id']})

                job = TaskInstanceModel(instance=result_status['data']['job_instance']['job_instance_id'],
                                        job=JobModel.objects.get(bk_biz=int(bk_biz), job_uuid=job_uuid),
                                        name=result_status['data']['job_instance']['name'],
                                        user=self.user,
                                        is_finished=result_status['data']['is_finished'],
                                        status=result_status['data']['job_instance']['status'],
                                        create_time=result_status['data']['job_instance']['create_time'],
                                        total_time=result_status['data']['job_instance']['total_time']
                                        )

                if task_name:
                    job.name = task_name

                job.save()

                result['data']['task_instance_id'] = job.id
        except Exception as e:
            result["message"] = str(e)

        return result

    def get_task_log(self, task_instance_id=0):
        instanceObj = TaskInstanceModel.objects.get(id=task_instance_id)

        refresh = get_system_config(
            biz_id=TaskInstanceModel.objects.get(id=task_instance_id).job.bk_biz,
            config_key='task_instance_refresh')

        if refresh == 'true':
            result = instanceObj.result_log
            if result:
                result = json.loads(result)
            else:

                params = {
                    'bk_biz_id': instanceObj.job.bk_biz,
                    "job_instance_id": instanceObj.instance
                }

                result = self.client.job.get_job_instance_log(params)
                result["data"][0]["name"] = instanceObj.job.title
                result = result['data']

            return result
        else:
            result = instanceObj.result_log
            if result:
                result = json.loads(result)
            else:
                result = []
            return result

    def get_task_status(self, task_instance_id=0):
        instanceObj = TaskInstanceModel.objects.get(id=task_instance_id)
        refresh = get_system_config(
            biz_id=TaskInstanceModel.objects.get(id=task_instance_id).job.bk_biz,
            config_key='task_instance_refresh')

        if not instanceObj.is_finished and refresh == 'true':
            params = {
                'bk_biz_id': instanceObj.job.bk_biz,
                "job_instance_id": instanceObj.instance
            }

            data = self.client.job.get_job_instance_status(params)

            if instanceObj.is_finished == False and data["data"]["is_finished"]:
                instanceObj.is_finished = data["data"]["is_finished"]
                instanceObj.status = data["data"]["job_instance"]["status"]
                instanceObj.start_time = ' '.join(data["data"]["job_instance"]["start_time"].split(' ')[0:2])
                instanceObj.end_time = ' '.join(data["data"]["job_instance"]["end_time"].split(' ')[0:2])
                instanceObj.total_time = int(data["data"]["job_instance"]["total_time"])

        return model_to_dict(instanceObj)


# 蓝鲸原生任务接口
class BK_TaskManager:
    def __init__(self, request):
        self.request = request
        self.client = get_client_by_request(request)

    def run_fast_job(self, bk_biz, module, title, ip_list, user_name, script_content, script_param=None,
                     script_timeout=600):
        result = {u'message': u'', u'code': -1, u'data': [], 'result': False}

        script_params = {
            'bk_biz_id': bk_biz,
            "account": user_name,
            'script_content': script_content,
            "script_param": script_param,
            'ip_list': ip_list,
            'script_timeout': script_timeout,
        }

        try:
            result = self.client.job.fast_execute_script(script_params)

        except Exception as e:
            result["message"] = str(e)

        return result

    def fast_push_file(self, biz_id, account, file_target_path, file_source, ip_list=None):
        data = {
            'bk_biz_id': biz_id,
            'account': account,
            'file_target_path': file_target_path,
            'file_source': file_source,
            'ip_list': ip_list,
        }
        result = self.client.job.fast_push_file(data)
        return result

    def get_task_log(self, biz_id, job_instance_id):
        params = {
            'bk_biz_id': biz_id,
            "job_instance_id": job_instance_id
        }

        return self.client.job.get_job_instance_log(params)

    def get_job_status(self, biz_id, job_instance_id):
        data = {
            'bk_biz_id': biz_id,
            'job_instance_id': job_instance_id,
        }

        return self.client.job.get_job_instance_status(data)
