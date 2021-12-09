from django.http import JsonResponse
# Create your views here.
from django.core.cache import cache
from .search_options import *

def searchTest(request):
    if request.method == 'POST':
        dataSet = [{'type': 1, 'content':'computer'}]
        isAdvanced = False
        ret = pagingCacheLV1({'keywords': dataSet,'isAdvanced':isAdvanced})
        docAggTransfer(ret['id'])
    return JsonResponse({"r":True})

def cacheTest(request):
    if request.method == 'POST':
        re = {}
        re['result'] = [1,3,4]
        cache.set('pzt',re,5*60)
        print(cache.get('pzt'))

        a = cache.get('pzt')['result']
        #print(dict)
        #dict.append(5)
        print(cache.get('pzt'))
    return JsonResponse({"r":True})

