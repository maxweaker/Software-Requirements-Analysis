from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .send_email import *
from pattern.models import *


import simplejson
from  datetime import *

def VerifyEmail(email):
    pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(pattern, email) is not None:
        return True
    return False


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            user = User.objects.get(email=username)

            # django的后台中密码加密：所以不能password==password
            # User继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def post(self, request):
        req = simplejson.loads(request.body)
        ret = {"code": 200, "msg": "注册成功"}
        # try:
        nickname = req['nickname']
        email = req['email']
        password = req['password']
        has_avatar = req['has_avatar']
        print(nickname)
        print(email)
        print(password)
        exist_user = User.objects.filter(nickname=nickname)
        if len(exist_user) > 0:
            ret["code"] = 202
            ret["msg"] = "该用户名已被占用"
            return JsonResponse(ret)
        #为注册用户做样例，暂时注释掉邮箱验证
        # = req['auth_code']
        #a_res = emailVerify.objects.filter(email=email, randomCode=auth_code)
        #if not a_res.exists():
        #    ret["code"] = 203
        #    ret["msg"] = "验证码错误"
        #    return JsonResponse(ret)
        #a_res.delete()
        user = User.objects.create(nickname=nickname, email=email)
        user.password = make_password(password)
        user.username = email
        user.date_joined = datetime.now()
        if has_avatar == 1:
            img_src = request.FILES.get("avatar")
            user.avatar = img_src
        user.save()
        # except:
        #    ret["code"] = 201
        return JsonResponse(ret)


class LoginView(View):
    def post(self, request):
        req = simplejson.loads(request.body)
        ret = {"code": 200, "msg": "登录成功"}
        try:
            email = req['email']
            password = req['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
            else:
                ret["code"] = 202
                ret["msg"] = "邮箱或密码错误"
        except:
            ret["code"] = 201
            ret["msg"] = "信息不全"
        return JsonResponse(ret)


class LogoutView(View):
    def post(self, request):
        ret = {"code": 200, "msg": "退出登录"}
        logout(request)
        return JsonResponse(ret)


def lineChart(request):
    #为方便测试，暂时传进nickname做参数,pieChart同样
    ret = {"code": 200, "msg": "返回成功", "data": []}
    req = simplejson.loads(request.body)
    print(req)
    nickname = req['nickname']
    user = User.objects.get(nickname = nickname)
    #user  = request.user
    now = datetime.now()
    print(now)
    retList = []
    #初始化两组五天内的记录
    for i in range(5):
        retList.append({'date':(now-timedelta(days=i)).strftime("%Y-%m-%d") ,'watchNum':0,'type':'Journal'})
    for i in range(5):
        retList.append({'date':(now-timedelta(days=i)).strftime("%Y-%m-%d"),'watchNum':0,'type':'Conference'})
    recods = BrowseRecord.objects.filter(nickname=user.nickname,browseTime__gt=now-timedelta(days=5))
    for record in recods:
        if record.docType == 'Journal':
            subscript = (now - record.browseTime).days
            retList[subscript]['watchNum'] = retList[subscript]['watchNum'] + 1
        else:
            subscript = (now - record.browseTime).days+5
            retList[subscript]['watchNum'] = retList[subscript]['watchNum'] + 1
    ret['chartLine'] = retList
    return JsonResponse(ret)


def pieChart(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request.body)
        print(req)
        nickname = req['nickname']
        user = User.objects.get(nickname=nickname)
        # user  = request.user
        now = datetime.now()
        print(now)
        records = BrowseRecord.objects.filter(nickname=user.nickname,browseTime__gt=now-timedelta(days=5))
        total = len(records)
        fields = {}
        for record in records:
            if record.docField in fields:
                fields[record.docField] = fields[record.docField] + 1
            else:
                fields[record.docField] = 1
        retList = []
        for key in fields.keys():
            retList.append({'subject':key,'ratio':fields[key]/total})
        ret['chartPie'] = retList
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


class authen_email(View):
    def post(self, request):
        ret = {"code": 200, "msg": "返回成功"}
        req = simplejson.loads(request.body)
        email = req['email']
        if User.objects.filter(email=email).exists():
            ret["msg"] = "此邮箱已被占用"
            ret["code"] = 201
            return JsonResponse(ret)
        if not VerifyEmail(email):
            ret["msg"] = "邮箱不合法"
            ret["code"] = 202
            return JsonResponse(ret)
        emailVerify.objects.filter(email=email).delete()
        res = send_my_email(email)
        if res != 1:
            ret["code"] = 203
            ret["msg"] = "发送失败，请您稍后重试"
        return JsonResponse(ret)


def mecTest(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功"}
        #req = simplejson.loads(request.body)
        req = {}
        mec = Mechanism.objects.all()
        for m in mec:
            print(m.pk)
        return JsonResponse(ret)