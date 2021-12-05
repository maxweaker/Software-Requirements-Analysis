from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from pattern.models import *


def VerifyEmail(email):
    pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$ '
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
        ret = {"code": 200, "msg": "注册成功"}
        try:
            nickname = request.POST.get("nickname")
            email = request.POST.get("email")
            password = request.POST.get("password")
            has_avatar = int(request.POST.get("has_avatar"))
            exist_user = User.objects.filter(nickname=nickname)
            if len(exist_user) > 0:
                ret["code"] = 202
                ret["msg"] = "该用户名已被占用"
                return JsonResponse(ret)
            exist_user = User.objects.filter(email=email)
            if len(exist_user) > 0:
                ret["code"] = 203
                ret["msg"] = "该邮箱已被占用"
                return JsonResponse(ret)
            if not VerifyEmail(email):
                ret["code"] = 204
                ret["msg"] = "邮箱不合法"
            user = User.objects.create(nickname=nickname, email=email)
            user.password = make_password(password)
            user.date_joined = datetime.now()
            if has_avatar == 1:
                img_src = request.FILES.get("avatar")
                user.avatar = img_src
            user.save()
        except:
            ret["code"] = 201
        return JsonResponse(ret)


class LoginView(View):
    def post(self, request):
        ret = {"code": 200, "msg": "登录成功"}
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
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
