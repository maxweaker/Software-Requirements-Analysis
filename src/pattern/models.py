from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.core import validators
import django.utils.timezone as timezone

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=64,null=False)
    avatar = models.ImageField(upload_to='image/avatar', default='iamge/default.png', max_length=100)
    email = models.EmailField(null=False)
    password = models.TextField(null=False)
    isqualified = models.BooleanField(default=False)
    selfintroduce = models.TextField(default="一名低调的用户")
    #introduction = models.TextField(default="一名低调的用户")
    """
    用整数表示用户身份：
    0：普通用户
    1：机构
    2：专家
    """
    identity = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.nickname


class Record(models.Model):
    """
    用户浏览记录
    """
    neckname = models.CharField(max_length=64, null=False)
    dataTime = models.DateTimeField(null=False)
    DOI = models.CharField(max_length=64, null=False)

    
class Mechanism(User):
    mecName = models.CharField(max_length=128, null=False)
    briefIntro = models.TextField(null=True)
    ranking = models.IntegerField(null=True)


class Expert(User):
    EID = models.CharField(max_length=32, primary_key=True)

    mec = models.ForeignKey('Mechanism', on_delete=models.CASCADE, null=True)

    domain = models.CharField(max_length=64)
    realName = models.CharField(max_length=128)
    pubNum = models.IntegerField(null=True)
    isCertified = models.BooleanField(default=False, null=False)


class Administrators(User):
    realName = models.CharField(max_length=64)


class Comment(models.Model):
    nextComment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    userName = models.CharField(max_length=64)
    commentTime = models.DateTimeField(null=False,default = timezone.now)


class Attestation(models.Model):
    applicant = models.ForeignKey('User', on_delete=models.CASCADE)

    mecName = models.CharField(max_length=128, null=False)
    operatorID = models.CharField(max_length=32, null=False)
    certificateFile = models.FileField(null=False)

class HotKey(models.Model):
    content = models.TextField(null=False)
    visit = models.IntegerField(null=False,default=0)

class emailVerify(models.Model):
    email = models.EmailField(max_length=64,null=False)
    randomCode = models.TextField(null=False)