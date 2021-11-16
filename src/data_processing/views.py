from django.shortcuts import render
from django.http import JsonResponse
import simplejson
from .models import ReadingHead
import json
from pattern.multiplexing_operation import *

# Create your views here.
def clean_data(request):
    if request.method == 'POST':
        r = simplejson.loads(request.body)
        DocNum = r['DocNum']
        fw = 'D:\下载目录\clean\\aminer_papers_1.txt'
        fr = 'D:\下载目录\\aminer_papers_1.txt'
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
                try:
                    docCreate(json_dict)
                    update = update + 1
                except :
                    print("doc No."+str(update)+" failed")
                    pass

        return JsonResponse(r)

def clear_data(request):
    if request.method == 'POST':
        docs = Document.objects.all()
        for doc in docs:
            author = doc.firstAuthor
            if(author != None):
                while (author.nextAuthor != None):
                    nextauthor = author.nextAuthor
                    author.delete()
                    author = nextauthor
                author.delete()
            key = doc.firstKeyword
            if(key != None):
                while (key.nextKey != None):
                    nextkey = key.nextKey
                    key.delete()
                    key = nextkey
                key.delete()
        docs.delete()
    return JsonResponse({'success':True})


