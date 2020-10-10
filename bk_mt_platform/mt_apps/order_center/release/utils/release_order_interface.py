from ..models import ReleaseOrder
from ....order_center.order.utils.order_interface import OrderInterface
from ....order_center.order_config.utils.order_config_interface import OrderType, OrderConfigInterface
from ....order_center.process_config.utils.process_config_interface import ProcessConfigInterface


class ReleaserOrderInterface(OrderInterface, OrderConfigInterface, ProcessConfigInterface):
    order_type = OrderType.release.name

    @classmethod
    def create_suborder(cls, **kwargs):
        result = ReleaseOrder.objects.create(
            release_id=kwargs.get('release_id'),
            release_version=kwargs.get('release_version'), svn_version=kwargs.get('svn_version'),
            contact_user=kwargs.get('contact_user'), desc=kwargs.get('desc'),
            reason=kwargs.get('reason'), level=kwargs.get('level'),
            servers=kwargs.get('servers'), server_list=kwargs.get('server_list'),
            remark=kwargs.get('remark'), release_flag=kwargs.get('release_flag')
        )
        return result.release_id

    @classmethod
    def get_suborder(cls, suborder_id):
        result = ReleaseOrder.objects.all().filter(release_id=suborder_id).values(
            'release_id', 'env', 'release_version', 'svn_version',
            'release_flag', 'state', 'enable', 'contact_user', 'desc', 'reason',
            'level', 'servers', 'server_list', 'remark',
        ).first()

        data = {
            "环境": result['env'],
            "发布版本": result['release_version'],
            "svn版本": str(result['svn_version']) if result['svn_version'] != 0 else '/',
            "gm": "Yes" if result['release_flag'].split(':')[0] == '1' else 'No',
            "log": "Yes" if result['release_flag'].split(':')[1] == '1' else 'No',
            "是否回滚": "Yes" if result['release_flag'].split(':')[2] == '1' else 'No',
            "db脚本": result['desc'] if result['desc'] != '0' else '无',
            "更新原因": result['reason'],
            "内容提供人": result['contact_user'],
            "更新服务": result['servers'] if result['servers'] != '0' else '无',
            "更新服务列表": result['server_list'].replace(';', '\n') if result['server_list'] != '0' else '无',
            "特殊说明": result['remark'],
        }
        return data

    @classmethod
    def ding_massage(cls, **order_info):
        sub_data = ''
        for k, v in cls.get_suborder(order_info['suborder']).items():
            sub_data = sub_data + ">" + k + ": " + v + "\n\n"

        return sub_data

    @classmethod
    def script_param(cls, order_id):
        order = super(ReleaserOrderInterface, cls).order_id_get_order_info(order_id)
        sub_order = ReleaseOrder.objects.all().filter(release_id=order['suborder']).values(
            'release_id', 'env', 'release_version', 'svn_version', 'release_flag', 'contact_user', 'servers',
            'server_list', 'reason', 'desc'
        ).first()

        param = str(sub_order['release_id']) + ' ' + sub_order['env'] + ' ' + sub_order['release_version'] \
                + ' ' + str(sub_order['svn_version']) + ' ' + sub_order['release_flag'] + ' ' + order[
                    'submitter'] + ' "' + sub_order['servers'] + '" "' + sub_order['server_list'] + '" "' + sub_order[
                    'reason'] + '" "' + sub_order['desc'] + '" "' + sub_order['contact_user'] + '" ' + str(order_id)
        return param
