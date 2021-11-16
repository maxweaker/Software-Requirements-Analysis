from .models import *

def legalDocDate(dict):
    if 'doi' in dict and 'authors' in dict and 'keywords' in dict and 'year' in dict:
        if dict['doi'] != None and dict['doi'] != 'null' and dict['keywords'] != None:
            authors = dict['authors']
            for author in authors:
                if 'id' not in author or 'name' not in author:
                    return False
            return True
        else:
            return False
    else:
        return False

def docCreate(dict):
    id = dict['id']
    doi = dict['doi']
    authors = dict['authors']
    keywords = dict['keywords']
    title = dict['title']
    year = dict['year'] if dict['year'] != None else 1900
    citation = dict['n_citation'] if 'n_citation' in dict else 0
    abstract = dict['abstract'] if 'abstract' in dict else None

    doc = Document.objects.create(DocID=id,DOI=doi,title=title,abstract=abstract,mainBody=None,
                            firstKeyword=None,firstAuthor=None,pubYear=year,citation=citation)
    firstKey = keywordsCreate(keywords,id)
    firstAuthor = authorsCreate(authors,id)
    doc.firstKeyword = firstKey
    doc.firstAuthor = firstAuthor
    doc.save()

def keywordsCreate(keywords,DocID):
    key_ins_list = []
    for key in keywords:
        if len(key) > 64:
            key = ' '.join(key.split()[:2])
        key_ins_list.append(Keyword.objects.create(key=key,DocID=DocID))
    firstKey = key_ins_list[0]
    for i in range(0,len(key_ins_list)-1):
        key = key_ins_list[i]
        nextKey = key_ins_list[i+1]
        key.nextKey = nextKey
        key.save()
    return firstKey

def authorsCreate(authors,DocID):
    author_ins_list = []
    for author in authors:
        author_ins_list.append(Author.objects.create(AID=author['id'],name=author['name'],DocID=DocID))
    firstAuthor = author_ins_list[0]
    for i in range(0,len(author_ins_list)-1):
        author = author_ins_list[i]
        nextAuthor = author_ins_list[i+1]
        author.nextAuthor = nextAuthor
        author.save()
    return firstAuthor