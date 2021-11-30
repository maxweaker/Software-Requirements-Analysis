from django.shortcuts import render
from django.http import JsonResponse
import simplejson
from .models import ReadingHead
import json
from pattern.multiplexing_operation import *

from elasticsearch import Elasticsearch, helpers
from django.core.cache import cache

# Create your views here.
def clean_data(request):
    if request.method == 'POST':
        r = simplejson.loads(request.body)
        DocNum = r['DocNum']
        fw = 'D:\下载目录\clean\\mag_papers_20.txt'
        fr = 'D:\下载目录\\mag_papers_20.txt'
        with open(fw, 'w') as file_to_write:
            with open(fr, 'r') as file_to_read:
                useable = 0
                while (useable<DocNum):
                    line = file_to_read.readline()
                    json_dict = json.loads(line)
                    if legalDocDate(json_dict):
                        file_to_write.writelines(line)
                        useable = useable + 1
    return JsonResponse({'success':True})

def read_data(request):
    if request.method == 'POST':
        r = simplejson.loads(request.body)
        forder = r['forder']+1
        file_num = r['file_num']
        readingHead = ReadingHead.objects.get(pk=forder)
        print(readingHead)
        fileName = readingHead.fileName
        ptr = readingHead.pointer

        doc_list = []
        with open(fileName, 'r') as file_to_read:
            for i in range(ptr):
                line = file_to_read.readline()

            update = 0
            while (update < file_num):
                print("creating doc No."+str(update))
                line = file_to_read.readline()
                json_dict = json.loads(line)
                readingHead.pointer = readingHead.pointer + 1
                readingHead.save()

                doc_list.append(docCreate(json_dict))
                update = update + 1

        es = Elasticsearch(["http://127.0.0.1:9200"])
        action = [
            {
                "_index": "articles",
                "_type": "doc",
                "_source": {
                    "id": doc['id'],
                    "doi": doc['doi'],
                    "title": doc['title'],
                    "pubYear": doc['year'],
                    "abstract": doc['abstract'],
                    "citation": doc['n_citation'],
                    "type": doc['type'],
                    "keys": doc['keywords'],
                    "authors": doc['authors'],
                    "fields": doc['fos'],
                    "refers": doc['references']
                }
            } for doc in doc_list]
        helpers.bulk(es, action, request_timeout=1000)

        return JsonResponse(r)

def build_index(request):
    if request.method == 'POST':
        es = Elasticsearch()
        config = {
                 "mappings": {
                     "doc": {
                         "properties": {
                             "id":{
                                 "type":"keyword"
                             },
                             "doi": {
                                 "type": "keyword"
                             },
                             "title": {
                                 "type": "text"
                             },
                             "authors": {
                                 "type": "keyword"
                             },
                             "keywords": {
                                 "type": "text"
                             },
                             "fields": {
                                 "type": "keyword"
                             },
                             "refers": {
                                 "type": "keyword"
                             },
                             "type": {
                                 "type": "keyword"
                             },
                             "year": {
                                 "type": "integer"
                             },
                             "abstract": {
                                 "type": "text"
                             },
                             "citation": {
                                 "type": "integer"
                             },
                         }
                     }
                 },
                 "settings": {
                    "number_of_shards": 2,  # 分片数
                     "number_of_replicas": 0  # 副本数
                },
            }
        res1 = es.indices.create(index='articles', body=config)

        return JsonResponse({"success":True})

def import_doc(request):
    if request.method == 'POST':
        return JsonResponse({"success":True})


def test(request):
    if request.method == 'POST':

        return JsonResponse({})
