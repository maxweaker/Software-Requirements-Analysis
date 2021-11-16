from django.db import models

# Create your models here.
class ReadingHead(models.Model):
    fileName = models.TextField(default='D:\下载目录\\aminer_papers_0.txt')
    pointer = models.IntegerField(default=0)