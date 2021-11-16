from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django.core import validators
# Create your models here.

class Document(models.Model):
    DOI = models.CharField(primary_key=True,max_length=64)

    firstKeyword = models.ForeignKey('Keyword',on_delete=models.CASCADE,null=True,default=None)
    firstAuthor = models.ForeignKey('Author',on_delete=models.CASCADE,null=True,default=None)

    DocID = models.CharField(max_length=32,unique=True,null=False) #数据源自带字段
    title = models.TextField(null=False,blank=False)
    abstract = models.TextField(blank=True,null=True)
    mainBody = models.FileField(null=True)
    pubYear = models.IntegerField(null=False,default=1900)
    citation = models.IntegerField(default=0)

class User(models.Model):
    nickname = models.CharField(max_length=64,null=False)
    password = models.CharField(max_length=64,null=False)
    email = models.EmailField(null=False)
    def __str__(self):
        return self.nickname

class Mechanism(User):
    mecName = models.CharField(max_length=128,null=False)
    briefIntro = models.TextField(null=True)
    ranking  = models.IntegerField(null=True)

class Expert(User):
    EID= models.CharField(max_length=32,primary_key=True)

    mec = models.ForeignKey('Mechanism',on_delete=models.CASCADE,null=True)
    
    domain = models.CharField(max_length=64)
    realName = models.CharField(max_length=128)
    pubNum  = models.IntegerField(null=True)
    isCertified = models.BooleanField(default=False,null=False)

class Administrators(User):
    realName = models.CharField(max_length=64)

class Keyword(models.Model):
    nextKey = models.ForeignKey('Keyword',on_delete=models.CASCADE,null=True,default=None,blank=True)
    DocID = models.CharField(max_length=64,null=True)

    key = models.CharField(max_length=64,null=False)


class Author(models.Model):
    AID = models.CharField(max_length=32,primary_key=True)
    name = models.CharField(max_length=64,null=False,default='unknow')
    nextAuthor = models.ForeignKey('Author',on_delete=models.CASCADE,null=True)
    DocID = models.CharField(max_length=64,null=True)

class Comment(models.Model):
    nextComment = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True)
    userName = models.CharField(max_length=64)

class Attestation(models.Model):
    applicant = models.ForeignKey('User',on_delete=models.CASCADE)

    mecName = models.CharField(max_length=128,null=False)
    operatorID = models.CharField(max_length=32,null=False)
    certificateFile = models.FileField(null=False)
