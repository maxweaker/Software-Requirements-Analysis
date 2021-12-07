from elasticsearch import Elasticsearch, helpers
from django.core.cache import cache
import json
from .exp_analysis import *
from pattern.models import HotKey
import threading
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
    dataSet = searche_body['keywords']
    #dataSet = [{'type':1,'content':'(\'Leptoquarks\'+\'math\')'},{'type':2,'content':'(\'G. Aad\'+-\'T. Gejo\')'}]
    isAdvanced = searche_body['isAdvanced']

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
    query_body = docSearch(search_body)
    search_cache['query'] = query_body
    res = es.search(index="articles", body=query_body,size = doc_per_page,scroll = '10m')
    print(res['hits']['total'])
    doc_list = res['hits']['hits']
    search_cache['page1'] = doc_list

    sid = res['_scroll_id']  # scroll的id,同时也是检索结果页的主键
    search_cache['id'] = sid
    total = res['hits']['total']
    
    #预加载三页文献(若检索结果大于等于三页)
    for i in range(1, 3):
        next_page = es.scroll(scroll_id=sid, scroll='2m')
        doc_list = next_page['hits']['hits']
        if len(doc_list) == 0:
            break
        search_cache['page'+str(i+1)] = doc_list
        search_cache['pageNum'] = i+1

    cache.set(sid, search_cache, 5 * 60)
    #print(cache.get(sid))
    print(cache.get(sid))
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

#构造检索结果统计字典
aggmap = ('keys.keyword','pubYear','authors','fields')
sortmap = ('pubYear','citation')
def docAggTransfer(sid):
    search_cache = cache.get(sid)
    query = search_cache['query']['query']
    aggs = {}
    terms = {'field':'keys.keyword','size':5}
    aggs['terms_count'] = {'terms':terms}
    aggDict = {'size':0,'query':query,'aggs':aggs}
    print(aggDict)
    es = Elasticsearch()
    for i in range(4):
        aggDict['aggs']['terms_count']['terms']['field'] = aggmap[i]
        res = es.search(index="articles", body=aggDict)
        print(res['aggregations']['terms_count']['buckets'])

class Preload (threading.Thread):
    def __init__(self, page, updateNum,sid):
        threading.Thread.__init__(self)
        self.page = page
        self.updateNum = updateNum
        self.sid = sid
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)


def getPage(sid,page):
    search_cache = cache.get(sid)
    pageNum = search_cache['pageNum']
    if page == pageNum:
        pass
    return search_cache['page'+str(page)]
