import simplejson
import json
from elasticsearch import Elasticsearch, helpers
from pattern.multiplexing_operation import legalDocDate,docCreate

file_num = 200000
fileName = 'D:\下载目录\clean\org4.txt'
ptr = 0

doc_list = []
with open(fileName, 'r') as file_to_read:
    for i in range(ptr):
        line = file_to_read.readline()

    update = 0
    while (update < file_num):
        line = file_to_read.readline()
        if not line:
            break
        json_dict = json.loads(line)
        doc_list.append(docCreate(json_dict))
        update = update + 1
        if update % 1000 == 0:
            print("creating doc No." + format(update, ','))
print('updated '+str(update)+' docs finally')

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
print('over')