from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from elasticsearch import Elasticsearch
from pattern.models import *


class HotPapers(View):
    def get(self, request):
        ret = {'code': 0}
        try:
            es = Elasticsearch()
            body = {
                "size": 8,
                "query": {
                    "match_all": {

                    }
                },
                "sort": [
                    {
                        "citation": {
                            "order": "desc"
                        }
                    }
                ]

            }
            res = es.search(index='articles', body=body)
            paperlist = [
                {
                    "papername": article['_source']['title'],
                    "author": article['_source']['authors'],
                    "heat": article['_source']['citation']
                }
                for article in res['hits']['hits']]
            ret['paperlist'] = paperlist
            ret['code'] = 200
        except:
            ret['paperlist'] = []
        return JsonResponse(ret)


class HotExpert(View):
    def get(self, request):
        ret = {"code": 200, "msg": "返回成功", "data": []}
        try:
            # 默认专家数量大于四
            experts = Expert.objects.all().order_by("-pubNum")[:4]
            ret["data"] = [
                {
                    "name": expert.realName,
                    "image": expert.avatar,
                    "introduction": expert.introduction
                }
                for expert in experts]
        except:
            ret["code"] = 201
            ret["msg"] = "专家数量过少"
        return JsonResponse(ret)

class HotKeyWords(View):
    def get(self,request):
        ret = {"code": 200, "msg": "返回成功", "data": []}
        hotKeys = HotKey.objects.all().order_by('-visit')
        ret['data'] = [
            {
                'word':key.content,
                'hot':key.visit
            }
            for key in hotKeys]
        return JsonResponse(ret)