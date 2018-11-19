# !usr/env/bin python3
# -*- coding: utf8 -*-

from vkApiAccess import *

import datetime, time, json, sys
import requests as req
import os

def loadVkCode(f):
    code = open(f, encoding='utf8').read()
    code = code.replace('+', '%20%2B')
    return code


def loadListFromFile(f):
    a = open(f, encoding='utf8').read().split('\n')
    a = [i for i in a if i != '']
    return a


def writeFile(data, f='groupMembers.json'):
    try:
        print('trying to write into existing file')
        a = open(f, 'a', encoding='utf8')
        print('success')
    except:
        print('making new result file: %s'%f)
        a = open(f, 'w', encoding='utf8')
    print(data, file=a)
    a.close()


def collectFromList(list_of_lists):
    ## берет на вход список списков
    ## возвращает сумму этих списков
    result = []
    for i in list_of_lists:
        if type(i) == list:
            result += collectFromList(i)
        else:
            result.append(i)
    return result


def getGroupUsers(groupid, access_token):
    # print('\n%s'%groupid)
    ## берет на вход id группы вк
    ## возвращает список id пользователей этой группы
    members_gl = []
    offset = 0 
    g = callVkApi('groups.getMembers', access_token, group_id=groupid, offset=offset)
    # print(g)
    g = g['count']
    strt = datetime.datetime.now()
    if g == 0:
        print('api method returned no users. perhaps group is blocked\n')
        return []
    else:
        while offset < g + 25000:
            code = loadVkCode('getAllUsersFromOneGroup.vkcode')
            code = code%(offset, groupid)
            returned = callVkApi('execute', access_token, code='%s'%code)
            offset_ = returned[0]
            members = returned[1]
            members = [i['items'] for i in members if i['items'] != []]
            members = collectFromList(members)
            members_gl += members
            offset = offset_
            time.sleep(0.3333333)
            # sys.stdout.write('\rfrom group %s collected %s users out of %s'%(groupid, len(collectFromList(members_gl)), g))
            # sys.stdout.flush()
        fnsh = datetime.datetime.now()
        # print('\nspent time: %s\n'%(fnsh-strt))
        return collectFromList(members_gl)


def getGroupNumId(screen_names_list, access_token):
    group_ids = ','.join(screen_names_list)
    res = callVkApi('groups.getById', access_token, group_ids=group_ids)
    # print(res)
    d = [i['id'] for i in res]
    return d


def main():

    access_token = open('access_token', 'r', encoding='utf8').read()
    group_lists = os.listdir(os.getcwd() + '/themes')
    group_lists = [os.getcwd() + '/themes/' + i for i in group_lists]
    for gl in group_lists:
        print(gl.split('/')[-1])
        gusers_sets = []
        group_urls = loadListFromFile(gl)
        group_screennames = [i.split('/')[-1] for i in group_urls]
        group_ids = getGroupNumId(group_screennames, access_token)
        for gid in group_ids:
            sys.stdout.write('\r%s...'%gid)
            gusers = getGroupUsers(gid, access_token)
            gusers_sets.append(set(gusers))
            sys.stdout.flush()
        intersections = set.intersection(*map(set, gusers_sets))
        print(len(intersections))
        print('')


if __name__ == '__main__':
    access_token = open('access_token', 'r', encoding='utf8').read()
    groups_dict = {}
    gid = ['club123275393']
    u = getGroupNumId(gid, access_token)
    for a in range(len(gid)):
        groups_dict[u[a]] = gid[a]
    for i in groups_dict.keys():
        f = open('%s.txt'%groups_dict[i], 'w', encoding='utf8')
        users = getGroupUsers(i, access_token)
        for uid in users:
            print('https://vk.com/id%s'%uid, file=f)
        f.close()

    # main()
    
