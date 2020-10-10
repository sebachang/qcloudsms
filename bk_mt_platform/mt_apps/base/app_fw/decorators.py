import functools

from mt_apps.base.app_fw.exceptions import CommonLogicError


def need_biz_id(func):
    @functools.wraps(func)
    def decorator(self, request, *args, **kwargs):
        biz_id = request.GET.get('biz_id')
        if biz_id is None or int(biz_id) <= 0:
            raise CommonLogicError(
                {'code': 10001, 'message': u"未传递biz_id或biz_id为负值"})
        else:
            kwargs['biz_id'] = int(biz_id)
            return func(self, request, *args, **kwargs)

    return decorator


def filter_biz_id(func):
    @functools.wraps(func)
    def decorator(self, queryset):
        if self.request.method == 'GET' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            biz_id = self.request.GET.get('biz_id')
            if biz_id is None or int(biz_id) < 0:
                raise CommonLogicError(
                    {'code': 10001, 'message': u"未传递biz_id或biz_id为负值"})
            return queryset.filter(biz_id=biz_id)

        return func(self, queryset)

    return decorator
