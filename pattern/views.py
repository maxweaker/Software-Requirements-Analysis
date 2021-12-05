from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import simplejson
from .models import User
import json
from pattern.multiplexing_operation import *

from elasticsearch import Elasticsearch, helpers
from django.shortcuts import render


def reladata(request):
    if request.method == 'POST':
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        users = User.objects.filter(nickname=nickname)
        if not users:
            return JsonResponse(json.dumps({
                'success': 0,
            }))
        user = users[0]
        data = {
            'userName': user.nickname,
            'userType': user.usertype,
            'isQualified': user.isqualified,
            'selfIntroduce': user.selfintroduce,
        }
        return JsonResponse(json.dumps(data), status=200)


def linechart(request):
    if request.method == 'POST':
        req = simplejson.loads(request)
        nickname = req.session['nickname']
        users = User.objects.filter(nickname=nickname)
        if not users:
            return JsonResponse(json.dumps({
                'success': 0,
            }))
        user = users[0]
        data = {
            'date':user.data,
            'watchNum':user.watchnum,
            'type':user.type,
        }
        return JsonResponse(json.dumps(data))


def userinfor(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        nickname = req['userName']
        users = User.objects.filter(nickname=nickname)
        if not users:
            return JsonResponse({'success': 0})
        user = users[0]
        data = {
            'userName': user.nickname,
            'userType': user.identity,
            'isQualified': user.isqualified,
            'selfIntroduce': user.selfintroduce,
        }
        return JsonResponse((data))

# Create your views here.
