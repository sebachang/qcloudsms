# -*- coding: utf-8 -*-
from json import dumps

from django.http import HttpResponse


def test_api(request):
    result = {'code': 10, 'message': 'throw exception', 'data': {'k1': 'v1', 'k1': 'value1'}}

    return HttpResponse(dumps(result))
