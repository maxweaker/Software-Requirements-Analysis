from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from elasticsearch import Elasticsearch


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
