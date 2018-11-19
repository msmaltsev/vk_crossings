# !usr/env/bin python3
# -*- coding: utf8 -*-

import requests as req
import json

def vk_makeRequest(method, access_token, **kwargs):
    request = 'https://api.vk.com/method/%s'%method
    if kwargs:
        request += '?'
        for kwarg in kwargs:
            request += '%s=%s&'%(kwarg, kwargs[kwarg])
    request += 'access_token=%s'%access_token
    return request + '&v=5.80'


def vk_callRequest(request, req_method):
    # print('vk_callRequest req_method %s'%req_method)
    r = eval('req.%s(request)'%req_method)
    t = r.text
    j = json.loads(t)
    return j


def callVkApi(method, access_token, req_method = 'get', **kwargs):
    request = vk_makeRequest(method, access_token, **kwargs)
    # print(req_method.upper(), request)
    response = vk_callRequest(request, req_method)
    try:
        response = response['response']
    except:
        pass
    return response