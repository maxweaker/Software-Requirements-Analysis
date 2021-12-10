from elasticsearch import Elasticsearch, helpers
from django.core.cache import cache
import json
from .exp_analysis import *
from pattern.models import HotKey
import threading
import copy
from .mutualTranslation import *

aggmap = ('keys.keyword','pubYear','authors','fields')
sortmap = ('pubYear','citation')
typemap = ('doi','title','authors','keys','pubYear','abstract','fields','citation')

_source = ['title', 'pubYear','authors','fields','citation']
original_query = {
            'bool':{'must':
                [
                    {'match_all':{}}
                ],
                    'filter':{}
            }
        }
should_dict = {
    'bool':{
        'should':[]
    }
}
original_dict = {'query':original_query,'_source':_source,'sort':[]}
doc_per_page = 10

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
    languageExtension = searche_body['languageExtension']

    if isAdvanced:
        for data in dataSet:
            #文法分析
            try:
                tl = lexicalAnalysis(data['content'])
            except Exception:
                return {'success':False,'code':201,'msg':'词法分析错误'}
            #构造表达式树
            try:
                tree = syntaxAnalysis(tl)
            except Exception:
                return {'success':False,'code':202,'msg':'语法分析错误'}
            #根据表达式树构造查询字典
            bool_dict = (searchTransfer(tree,data['type'],languageExtension))
            andList.append(bool_dict)
        finalLogic = {'must':andList}
        finalDict = copy.deepcopy(original_dict)
        finalDict['query']['bool'] = finalLogic
        print(finalDict)
        return finalDict
    else:
        data = dataSet[0]
        type = 1
        content = data['content']
        #若检索字段为keyword则更新hotkey表
        if type == 3:
            hotKeyUpdate(content)
        finalDict = copy.deepcopy(original_dict)
        initDict = {'match':{keymap[type]:content}}
        if languageExtension:
            lang = langDistinguish(content)
            extendDict = {}
            if lang == 'en':
                extendDict['match'] = {keymap[type]:enToZh(content)}
            else:
                extendDict['match'] = {keymap[type]: zhToEn(content).lower()}
            shouldList = [initDict,extendDict]
            finalDict['query']['bool']['filter'] = {'bool':{'should':shouldList}}
        else:
            finalDict['query']['bool']['filter'] = initDict
        print(finalDict)
        return finalDict


def getSearchMsg(search_body):
    es = Elasticsearch()
    search_cache = {}  # redis临时保存搜索结果

    query_body = docSearch(search_body)
    if 'success' in query_body:
        if query_body['success'] == False:
            return query_body
    search_cache['query'] = query_body
    res = es.search(index="articles", body=query_body,size = doc_per_page,scroll = '30m')
    print(res['hits']['total'])
    doc_list = res['hits']['hits']
    search_cache['page1'] = doc_list

    sid = res['_scroll_id']  # scroll的id,同时也是检索结果页的主键
    search_cache['id'] = sid

    total = res['hits']['total']
    search_cache['pageNum'] = 1
    cache.set(sid, search_cache, 30 * 60)
    #预加载3页文献(若检索结果大于等于3页)
    preload = Preload(1, 2, sid)
    preload.start()
    preload.join()
    return {"id":sid,"count":total,'success':True}

#构造检索结果统计字典
def docAggTransfer(sid):
    search_cache = cache.get(sid)
    query = search_cache['query']['query']
    aggs = {}
    terms = {'field':'keys.keyword','size':5}
    aggs['terms_count'] = {'terms':terms}
    aggDict = {'size':0,'query':query,'aggs':aggs}
    statistics = {}
    es = Elasticsearch()

    staList = []
    aggDict['aggs']['terms_count']['terms']['field'] = 'pubYear'
    res = es.search(index="articles", body=aggDict)
    for b in res['aggregations']['terms_count']['buckets']:
        staList.append({'count':b['doc_count'],'year':str(b['key'])})
    statistics['years'] = staList

    staList = []
    aggDict['aggs']['terms_count']['terms']['field'] = 'authors'
    res = es.search(index="articles", body=aggDict)
    for b in res['aggregations']['terms_count']['buckets']:
        staList.append({'count': b['doc_count'], 'author': b['key']})
    statistics['authors'] = staList

    staList = []
    aggDict['aggs']['terms_count']['terms']['field'] = 'fields'
    res = es.search(index="articles", body=aggDict)
    for b in res['aggregations']['terms_count']['buckets']:
        staList.append({'count': b['doc_count'], 'field': b['key']})
    statistics['fields'] = staList

    return statistics

#新建子线程预加载2-3页
class Preload (threading.Thread):
    def __init__(self, page, updateNum,sid):
        threading.Thread.__init__(self)
        self.page = page
        self.updateNum = updateNum
        self.sid = sid
    def run(self):
        search_cache = cache.get(self.sid)
        pageNum = search_cache['pageNum']
        es = Elasticsearch()
        for i in range(pageNum, pageNum+self.updateNum):
            next_page = es.scroll(scroll_id=self.sid, scroll='10m')
            doc_list = next_page['hits']['hits']
            if len(doc_list) == 0:
                break
            search_cache['page' + str(i + 1)] = doc_list
            search_cache['pageNum'] = i + 1

        print('preload to page '+str(search_cache['pageNum']))
        cache.set(self.sid, search_cache, 30 * 60)

def get_page(sid,page):
    search_cache = cache.get(sid)
    pageNum = search_cache['pageNum']
    if page > pageNum:
        preload = Preload(page, page-pageNum+1, sid)
        preload.start()
        preload.join()
    search_cache =  cache.get(sid)
    return search_cache['page'+str(page)]

def sortAndFilt(req):
    # 构造排序字典
    sid = req['id']
    print(req)
    sortDict = {}
    sortField = typemap[req['sort']['type']]
    sortOrder = req['sort']['order']
    if sortOrder == 1:
        sortDict[sortField] = {'order': 'asc'}
    elif sortOrder == -1:
        sortDict[sortField] = {'order': 'desc'}

    #构造过滤字典
    search_cache = cache.get(sid)
    query = search_cache['query']['query']
    mustList = query['bool']['must']
    filters = req['filters']

    #每种相同类型的过滤器之间逻辑关系为OR
    shouldAuthors = []
    shouldYears = []
    shouldFields = []
    for filter in filters:
        if filter['type'] == 2:
            shouldAuthors.append(
                {'term': {
                    typemap[2]: filter['content']
                }}
            )
        elif filter['type'] == 4:
            shouldYears.append(
                {'term': {
                    typemap[4]: int(filter['content'])
                }}
            )
        elif filter['type'] == 6:
            shouldFields.append(
                {'term': {
                    typemap[6]: filter['content']
                }}
            )
    if len(shouldAuthors) > 0:
        mustList.append({'bool':{
            'should':shouldAuthors
        }})
    if len(shouldYears) > 0:
        mustList.append({'bool':{
            'should':shouldYears
        }})

    if len(shouldFields) > 0:
        mustList.append({'bool':{
            'should':shouldFields
        }})

    query['bool']['must'] = mustList
    new_query = {'query': query, '_source': _source, 'sort': [sortDict]}
    #添加条件重新检索
    es = Elasticsearch()
    search_cache = {}
    query_body = new_query
    search_cache['query'] = query_body
    res = es.search(index="articles", body=query_body, size=doc_per_page, scroll='30m')
    print(res['hits']['total'])
    doc_list = res['hits']['hits']
    search_cache['page1'] = doc_list
    sid = res['_scroll_id']  # scroll的id,同时也是检索结果页的主键
    search_cache['id'] = sid
    total = res['hits']['total']
    search_cache['pageNum'] = 1
    cache.set(sid, search_cache, 30 * 60)
    preload = Preload(1, 3, sid)
    preload.start()
    preload.join()
    return {"id": sid, "count": total, 'success': True}