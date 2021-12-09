from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import simplejson
from django.utils.timezone import now

from .models import User
import json
from pattern.multiplexing_operation import *

from elasticsearch import Elasticsearch, helpers
from django.shortcuts import render
from library.time import *

def reladata(request):

    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        users = User.objects.filter(nickname=nickname)
        if not users:
            ret['code'] = 201
            ret['msg'] = 'user不存在'
            return JsonResponse(ret)
        user = users[0]
        ret['userName'] = user.nickname
        ret['userType'] = user.identity
        ret['isQualified'] = user.isqualified
        ret['selfIntroduce'] = user.selfintroduce
        return JsonResponse(ret)

def linechart(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        users = User.objects.filter(nickname=nickname)
        if not users:
            ret['code'] = 201
            ret['msg'] = 'user不存在'
            return JsonResponse(ret)
        user = users[0]
        ret['data'] = {
            'date':user.data,
            'watchNum':user.watchnum,
            'type':user.type,
        }
        return JsonResponse(data)


def userinfor(request):
    if request.method == 'POST':
        req = json.loads(request)
        nickname = req.session['userName']
        users = User.objects.filter(nickname=nickname)
        ret = {"code":200,"msg":"寻找成功","data":[]}
        if not users:
            ret["code"] = 201
            ret["msg"] = "用户不存在"
            return JsonResponse(ret)
        user = users[0]
        data = {
            'userName': user.nickname,
            'userType': user.identity,
            'isQualified': user.isqualified,
            'selfintroduce': user.selfintroduce,
        }
        ret["data"].append(data)
        return HttpResponse(json.dumps(data))
def pieChart(request):
    if request.method == 'GET':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request)
        user = request.user
        #nickname = req.session['nickname']
        nickname = user.nicname
        records = Record.objects.filter(nickname=nickname)
        if not records:
            ret['code'] = 201
            ret['msg'] = '无记录'
            return JsonResponse(ret)
        for record in records:
            if not datecompare(record.datatime, now, days=5):
                continue
            if record.subject in res.keys():
                res[record.subject] += 1
            else:
                res[record.subject] = 1
        return JsonResponse(ret)

def userinfor(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        user = request.user
        print(type(user.nickname))
        ret['userName'] = user.nickname
        ret['userType'] = user.identity
        ret['isQualified'] = user.isqualified
        ret['selfIntroduce'] = user.selfintroduce
        return JsonResponse(ret)
