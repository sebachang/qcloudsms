import requests

from mt_apps.base.api.components.login import LoginAPI
from mt_apps.base.utils.util_singleton import SingletonType
from ..models import Channel, NotifyRule


def send_dingtalk(token, content=None, json=None):
    if not json:
        json = {'msgtype': 'text', 'text': {'content': content}}
    r = requests.post(f'https://oapi.dingtalk.com/robot/send?access_token={token}', json=json)
    print(r.text)


class NotifyManager(metaclass=SingletonType):
    def __init__(self):
        self.cache = {}
        self.rebuild_cache()

    def send_message(self, biz_id, tag, type, content=None, json=None, at_users=None, at_all=False):
        cache = self.cache.get(biz_id, {})
        tag_ids = cache.get('tag_id', {}).get(tag, [])
        type_ids = cache.get('type_id', {}).get(type.value, [])
        channel_ids = set(tag_ids) & set(type_ids)
        chan_map = cache.get('chan_map', {})
        for id in channel_ids:
            chan = chan_map.get(id, None)
            if chan:
                if not json:
                    json = {'msgtype': 'text', 'text': {'content': content}}

                keyword = chan.get('keyword', '')
                if keyword:
                    if json.get('msgtype', '') == 'text':
                        json['text']['content'] = keyword + json['text']['content']
                    elif json.get('msgtype', '') == 'markdown':
                        json['markdown']['title'] = keyword + json['markdown']['title']

                if at_users or at_all:
                    json.setdefault('at', {})
                if at_users:
                    result_api = LoginAPI.get_batch_user_info(user="admin", **{"bk_username_list": at_users})

                    phone = [v['phone'] for k, v in result_api['data'].items()
                             if k in at_users if v['phone']]
                    at_phone = ['@' + x for x in phone]
                    json['at']['atMobiles'] = at_phone
                if at_all:
                    json['at']['isAtAll'] = True
                send_dingtalk(chan['token'], json=json)
        pass

    def rebuild_cache(self):
        self.cache.clear()
        for rule in NotifyRule.objects.all():
            if rule.biz_id not in self.cache:
                self.cache[rule.biz_id] = {'tag_id': {}, 'type_id': {}, 'chan_map': {}}
            tag_id = self.cache[rule.biz_id]['tag_id']
            destination = [o['id'] for o in rule.destination.values('id')]
            for tag in rule.tags:
                if tag not in tag_id:
                    tag_id[tag] = []
                tag_id[tag] += destination
            type_id = self.cache[rule.biz_id]['type_id']
            for type in rule.types:
                if type not in type_id:
                    type_id[type] = []
                type_id[type] += destination
        for channel in Channel.objects.all():
            if not channel.enabled:
                continue
            if channel.biz_id not in self.cache:
                self.cache[channel.biz_id] = {'tag_id': {}, 'chan_map': {}}
            if channel.type == 'dingtalk':
                chan_map = self.cache[channel.biz_id]['chan_map']
                if channel.id not in chan_map:
                    chan_map[channel.id] = {}
                chan_map[channel.id]['token'] = channel.params.get('token', '')
                chan_map[channel.id]['keyword'] = channel.params.get('keyword', '')
