from elasticsearch import Elasticsearch, helpers
from django.core.cache import cache
import json
from .exp_analysis import *



def docSearch(searche_body):
    #初步检索，将结果存入一级缓存
    #输入示例
    andList = []
    dataSet =[{'type':1,'content':'(\'Leptoquarks\'+\'math\')'},{'type':2,'content':'(\'G. Aad\'*-\'T. Gejo\')'}]
    for data in dataSet:
        #文法分析
        tl = lexicalAnalysis(data['content'])
        #构造表达式树
        tree = syntaxAnalysis(tl)
        #根据表达式树构造查询字典
        bool_dict = (searchTransfer(tree,data['type']))
        andList.append(bool_dict)
    finalLogic = {'must':andList}
    return {'query':{'bool':finalLogic}}

def pagingCacheLV1(search_body):
    es = Elasticsearch()
    doc_per_page = 10  # 每页文献数

    search_cache = {}  # redis临时保存搜索结果

    res = es.search(index="articles", body=searchTransfer(search_body), scroll='10m')
    print(res['hits']['total'])
    results = res['hits']['hits']

    sid = res['_scroll_id']  # scroll的id,同时也是检索结果页的主键
    search_cache['id'] = sid

    total = res['hits']['total']
    scroll_size = total if total < 1000 else 1000  # 返回文献数最多为1000(待定)

    if scroll_size % doc_per_page == 0:
        max_page = scroll_size // doc_per_page
    else:
        max_page = scroll_size // doc_per_page + 1

    for i in range(1, max_page):
        next_page = es.scroll(scroll_id=sid, scroll='2m')
        results += next_page['hits']['hits']

    search_cache['results'] = results
    cache.set(sid, search_cache, 60 * 60)
    #print(cache.get(sid))

    return {"id":sid,"count":total}

def spagingCacheLV2(sid,sort_type):
    #按不同字段排序，结果存入二级缓存
    original = cache.get(sid)['results']
    if type == 0:
        citation_sorted = sorted(original,key = lambda x:x['_source']['citation'],reverse=True)
        cache.set({'id':sid+'-citation','results':citation_sorted})

