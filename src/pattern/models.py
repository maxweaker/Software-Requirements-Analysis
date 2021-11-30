from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django.core import validators
# Create your models here.

class Document(models.Model):
    DocID = models.CharField(max_length=64,primary_key=True) #数据源自带字段

    firstKeyword = models.ForeignKey('Keyword',on_delete=models.CASCADE,null=False)
    firstAuthor = models.ForeignKey('Author',on_delete=models.CASCADE,null=False)
    firstField = models.ForeignKey('Field',on_delete=models.CASCADE,null=True,default=None)
    firstRefer = models.ForeignKey('Refer',on_delete=models.CASCADE,null=True,default=None)

    DOI = models.CharField(max_length=64,null=False,unique=True)
    type = models.CharField(max_length=20,null=True)

    title = models.TextField(null=False,blank=False)
    abstract = models.TextField(blank=True,null=True)

    mainBody = models.FileField(null=True)

    pubYear = models.IntegerField(null=True,default=1900)
    citation = models.IntegerField(default=0)
    vist = models.IntegerField(default=0)


    def getKeywords(self):
        keys = []
        key = self.firstKeyword

        while True:
            keys.append(key.key)
            key = key.nextKey
            if key is None:
                break
        return keys

    def getAuthors(self):
        authors = []
        author = self.firstAuthor

        while True:
            authors.append(author.name)
            author = author.nextAuthor
            if author is None:
                break
        return authors

    def getFields(self):
        fields = []
        field = self.firstField
        if field is None:
            return None
        while True:
            fields.append(field.fieldName)
            field = field.nextField
            if field is None:
                break
        return fields

    def getRefers(self):
        refers = []
        refer = self.firstRefer
        if refer is None:
            return None
        while True:
            refers.append(refer.DocID)
            refer = refer.nextRefer
            if refer is None:
                break
        return refers

class User(AbstractUser):
    nickname = models.CharField(max_length=64,null=False)
    avatar = models.ImageField(upload_to='image/avatar', default='iamge/default.png', max_length=100)
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
    nextKey = models.ForeignKey('Keyword',on_delete=models.CASCADE,null=True,default=None)
    key = models.CharField(max_length=64,null=False)

class Field(models.Model):
    nextField = models.ForeignKey('Field',on_delete=models.CASCADE,null=True,default=None)
    fieldName = models.CharField(max_length=64,null=False)

class Author(models.Model):
    nextAuthor = models.ForeignKey('Author',on_delete=models.CASCADE,null=True,default=None)
    name = models.CharField(max_length=64,null=False,default='unknow')

class Refer(models.Model):
    nextRefer = models.ForeignKey('Refer',on_delete=models.CASCADE,null=True,default=None)
    DocID = models.CharField(max_length=64,null=True)

class Comment(models.Model):
    nextComment = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True)
    userName = models.CharField(max_length=64)

class Attestation(models.Model):
    applicant = models.ForeignKey('User',on_delete=models.CASCADE)

    mecName = models.CharField(max_length=128,null=False)
    operatorID = models.CharField(max_length=32,null=False)
    certificateFile = models.FileField(null=False)
