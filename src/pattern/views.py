from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import simplejson
from django.utils.timezone import now

from .models import User
import json
from pattern.multiplexing_operation import *

from elasticsearch import Elasticsearch, helpers
from django.shortcuts import render
from ..library.time import *


def lineChart(request):
    if request.method == 'GET':
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        records = Record.objects.filter(nickname=nickname)
        if not records:
            return HttpResponse(json.dumps({
                'success': 0,
            }))
        res = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 'success': 1}
        now = timezone.now()
        for i in range(5):
            for record in records:
                if dateCompare(record.datatime, now, days=i + 1):
                    res[i] += 1
                    records.remove(record)
        return HttpResponse(json.dumps(res))


def pieChart(request):
    if request.method == 'GET':
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        records = Record.objects.filter(nickname=nickname)
        if not records:
            return HttpResponse(json.dumps({
                'success': 0,
            }))
        res = {'success': 1}
        for record in records:
            if not dateCompare(record.datatime, now, days=5):
                continue
            if record.subject in res.keys():
                res[record.subject] += 1
            else:
                res[record.subject] = 1
        return res


def linechart(request):
    if request.method == 'GET':
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        users = User.objects.filter(nickname=nickname)
        if not users:
            return HttpResponse(json.dumps({
                'success': 0,
            }))
        user = users[0]
        data = {
            'date':user.data,
            'watchNum':user.watchnum,
            'type':user.type,
        }
        return HttpResponse(json.dumps(data))


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

# Create your views here.
