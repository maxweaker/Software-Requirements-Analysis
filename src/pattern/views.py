from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import simplejson
from .models import User
import json
from pattern.multiplexing_operation import *

from elasticsearch import Elasticsearch, helpers
from django.shortcuts import render


def reladata(request):
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
            'userName': user.nickname,
            'userType': user.usertype,
            'isQualified': user.isqualified,
            'selfIntroduce': user.selfintroduce,
        }
        return HttpResponse(json.dumps(data), status=200)


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



# Create your views here.
