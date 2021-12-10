# Create your views here.
from django.core.cache import cache
from .search_options import *
import simplejson
from .search_options import *
from django.http import JsonResponse


def searchTest(request):
    if request.method == 'POST':
        dataSet = [{'type': 1, 'content':'computer'}]
        dataSet = [{'type': 1, 'content':'shift'}]
        isAdvanced = False
        ret = pagingCacheLV1({'keywords': dataSet,'isAdvanced':isAdvanced})
        docAggTransfer(ret['id'])
    return JsonResponse({"r":True})
        #docAggTransfer(ret['id'])
    return JsonResponse({"ret":ret})

def cacheTest(request):
    if request.method == 'POST':

        cache.set('pzt',re,5*60)
        print(cache.get('pzt'))

        a = cache.get('pzt')['result']
        #print(dict)
        #dict.append(5)
        a = cache.get('pzt')
        a['geg'] = 32
        cache.set('pzt',a,5*60)
        print(cache.get('pzt'))
    return JsonResponse({"r":True})


def getPage(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request.body)
        sid = req['id']
        page = req['page']
        page_dict = get_page(sid=sid,page=page)
        docList = []
        for doc_s in page_dict:
            doc = doc_s['_source']
            doc['id'] = doc_s['_id']
            doc['authors'] = [
                {'name':author,'id':'-1'}
            for author in doc['authors']]
            if doc['fields'] is not None:
                doc['fields'] = [
                    {'field': field}
                    for field in doc['fields']]
            else:
                doc['fields'] = []
            docList.append(doc)

        ret['success'] = True
        ret['list'] = docList
        return JsonResponse(ret)

def sendQuery(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request.body)
        print(req)
        msg = getSearchMsg(req)
        if 'success' in msg:
            if msg['success'] == False:
                ret['success'] = False
                ret['code'] = msg['code']
                ret['msg'] = msg['msg']
                return JsonResponse(ret)
        ret['id'] = msg['id']
        ret['count'] = msg['count']
        ret['success'] = msg['success']
        return JsonResponse(ret)

def getStatistics(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request.body)
        statistics = docAggTransfer(req['id'])
        statistics['success'] = True
        return JsonResponse(statistics)

def sendFilters(request):
    if request.method == 'POST':
        ret = {"code": 200, "msg": "返回成功", "data": []}
        req = simplejson.loads(request.body)
        ret = sortAndFilt(req)
        return JsonResponse(ret)