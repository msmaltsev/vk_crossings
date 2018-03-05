# !usr/env/bin python3
# -*- coding: utf8 -*-

import requests as req
import simplejson as json, time

def vk_makeRequest(method, access_token, **kwargs):
    request = 'https://api.vk.com/method/%s'%method
    if kwargs:
        request += '?'
        for kwarg in kwargs:
            request += '%s=%s&'%(kwarg, kwargs[kwarg])
    request += '&v=5.71&access_token=%s'%access_token
    # print(request)
    return request


def vk_callRequest(request, req_method):
    # print('vk_callRequest req_method %s'%req_method)
    r = eval('req.%s(request)'%req_method)
    t = r.text
    j = json.loads(t)
    return j


def callVkApi(method, access_token, **kwargs):
    request = vk_makeRequest(method, access_token, **kwargs)
    # print(request)
    response = vk_callRequest(request, 'get')

    if 'error' in response:
        if response['error']['error_code'] == 15:
            print('no access to group')
            response = {'count':0,'users':[]}
        else:
            while 'error' in response:
                print(response['error'])
                time.sleep(0.333333)
                print('calling again...')
                response = vk_callRequest(request, 'get')
    try:
        response = response['response']
    except Exception as e:
        # print(e)
        response = response
    # print('response: ', response)
    return response