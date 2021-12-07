from elasticsearch import Elasticsearch, helpers
from django.core.cache import cache
import json
from .exp_analysis import *
from pattern.models import HotKey

def hotKeyUpdate(content):
    hotKey = HotKey.objects.filter(content=content)

    if len(hotKey) == 1:
        key = hotKey[0]
        key.visit = key.visit + 1
        key.save()
    else:
        newKey = HotKey.objects.create(content=content,visit=1)
        newKey.save()

def docSearch(searche_body):
    #初步检索，将结果存入一级缓存
    #输入示例
    andList = []
    #dataSet =[{'type':1,'content':'\'red\''}]
    dataSet = [{'type': 3, 'content':'free'}]
    #dataSet = [{'type':1,'content':'(\'Leptoquarks\'+\'math\')'},{'type':2,'content':'(\'G. Aad\'+-\'T. Gejo\')'}]
    isAdvanced = False

    if isAdvanced:
        for data in dataSet:
            #文法分析
            tl = lexicalAnalysis(data['content'])
            #构造表达式树
            tree = syntaxAnalysis(tl)
            #根据表达式树构造查询字典
            bool_dict = (searchTransfer(tree,data['type']))
            andList.append(bool_dict)
        finalLogic = {'must':andList}
        print(finalLogic)
        return {'query':{'bool':finalLogic}}
    else:
        data = dataSet[0]
        type = data['type']
        content = data['content']
        #若检索字段为keyword则更新hotkey表
        if type == 3:
            hotKeyUpdate(content)
        finalDict = {}
        finalDict['query'] = {'bool':{'must':[{"match_all": {}}]}}
        finalDict['query']['bool']['filter'] = {'term':{keymap[type]:content}}
        print(finalDict)
        return finalDict

def pagingCacheLV1(search_body):
    doc_per_page = 10
    es = Elasticsearch()
    search_cache = {}  # redis临时保存搜索结果
    body = docSearch(search_body)
    res = es.search(index="articles", body=body,size = doc_per_page,scroll = '10m')
    print(res['hits']['total'])
    results = res['hits']['hits']

    sid = res['_scroll_id']  # scroll的id,同时也是检索结果页的主键
    search_cache['id'] = sid
    total = res['hits']['total']
    #预加载三页文献(若检索结果大于等于三页)
    if doc_per_page < total:
        scroll_size = total

        if scroll_size % doc_per_page == 0:
            max_page = scroll_size // doc_per_page
        else:
            max_page = scroll_size // doc_per_page + 1

        for i in range(1, max_page):
            next_page = es.scroll(scroll_id=sid, scroll='2m')
            list = next_page['hits']['hits']
            for l in list:
                results.append(l)
            #results += next_page['hits']['hits']
            print('results'+str(len(results)))

    search_cache['results'] = results
    print('results' + str(len(results)))

    cache.set(sid, search_cache, 5 * 60)
    #print(cache.get(sid))

    return {"id":sid,"count":total}

def spagingCacheLV2(sid,sort_type):
    #按不同字段排序，结果存入二级缓存
    original = cache.get(sid)['results']
    #print(original)
    print(sort_type)
    if sort_type == 0:

        citation_sorted = sorted(original,key = lambda x:x['_source']['citation'],reverse=True)
        for o in citation_sorted:
            print(o['_source']['citation'])
        cache.set(sid+'-citation',{'results':citation_sorted},5*60)

