from elasticsearch import Elasticsearch, helpers
from django.core.cache import cache
import json

def searchTransfer(searche_body,doc_per_page):
    #TODO
    body = {
        "size": doc_per_page,
        "query": {
            # "match_all": {}
            "bool": {
                "should": [
                    {"bool": {
                        "must": [
                            {"match": {"keys": "complex shape"}},
                            {"match": {"keys": "plane waves"}},
                            {"term": {"pubYear": 2001}}
                        ]
                    }},
                    {"match": {"title": "Synthesis"}}
                ]
            }
        },
    }
    return body

def pagingCache(search_body):
    es = Elasticsearch()
    doc_per_page = 3  # 每页文献数

    search_cache = {}  # redis临时保存搜索结果
    res = es.search(index="articles", body=searchTransfer(search_body,doc_per_page), scroll='10m')
    print(res['hits']['total'])
    search_cache['page0'] = res['hits']['hits']

    sid = res['_scroll_id']  # scroll的id,同时也是检索结果页的主键
    search_cache['id'] = sid

    total = res['hits']['total']
    scroll_size = total if total < 1000 else 1000  # 返回文献数最多为1000

    if scroll_size % doc_per_page == 0:
        max_page = scroll_size // doc_per_page
    else:
        max_page = scroll_size // doc_per_page + 1

    for i in range(1, max_page):
        next_page = es.scroll(scroll_id=sid, scroll='2m')
        search_cache['page' + str(i)] = next_page['hits']['hits']

    cache.set(sid, search_cache, 60 * 60)
    print(cache.get(sid))

    return {"id":sid,"count":total}