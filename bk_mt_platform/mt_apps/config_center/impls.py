from jinja2 import BaseLoader

from .models import ConfigTemplate, ConfigKV


class DBTemplateLoader(BaseLoader):
    def __init__(self, biz_id):
        self.biz_id = biz_id

    def get_source(self, environment, template):
        content = ConfigTemplate.objects.get(biz_id=self.biz_id, name=template).content
        return content, template, lambda: True


def get_all_kv(biz_id):
    data = {}
    for record in ConfigKV.objects.filter(biz_id=biz_id):
        data[record.key] = record.value
    return data


def render_config(biz_id, name, data):
    from jinja2 import Environment
    env = Environment(loader=DBTemplateLoader(biz_id))

    kv = get_all_kv(biz_id)

    for k, v in kv.items():
        if k not in data:
            data[k] = v

    template = env.get_template(name)
    res = template.render(data)
    return res
