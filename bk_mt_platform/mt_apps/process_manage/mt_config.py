name = 'process_manage'
desc = '进程管理'


def register_config():
    cfg_module_process = {'index': 6, 'name': u'进程管理', 'icon': 'gear.svg'}

    from mt_apps.base.system_config.config_define import set_system_config
    set_system_config(cfg_module_process, 1, u'process_pack_url', u'程序包路径',
                      u'程序包s3路径, 例如: https://ops_pack.s3-us-west-1.amazonaws.com/',
                      default='https://moonton-disk.s3-ap-southeast-1.amazonaws.com/ops_refer_src/process_manage/')
    set_system_config(cfg_module_process, 2, u'process_header', u'额外的请求头', u'如果需要请求头鉴权，请填写，例如 Referer:123456',
                      isNull=True, default='Referer: MKfNEh6ddTpGTd7ga8tSxzPR')
    set_system_config(cfg_module_process, 3, u'aws_s3_bucket', u's3 bucket', u's3 的bucket', default='moonton-disk')
    set_system_config(cfg_module_process, 4, u'aws_s3_path', u's3 路径', u's3 bucket内的路径',
                      default='ops_refer_src/process_manage/')
    set_system_config(cfg_module_process, 5, u'aws_access_key', u's3 access_key', u's3 的access key',
                      default='AKIAWZTIFM57D7NAV2XU')
    set_system_config(cfg_module_process, 6, u'aws_secret_key', u's3 secret_key', u's3 的secret key',
                      default='3fbqmbsCWmBz7ojlQPfJmjQVZi9WtIvazXSzQzG2')


def register_jobs(biz_id):
    global name, desc
    from mt_apps.base.task.job_manager import JobManager
    from .constants import job_uuid
    JobManager.register(biz_id, desc, name, job_uuid)
