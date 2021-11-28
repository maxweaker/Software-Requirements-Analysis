from .models import *

def legalDocDate(dict):
    if 'doi' in dict and 'authors' in dict and 'keywords' in dict and 'year' in dict:
        if dict['doi'] != None and dict['doi'] != 'null' and dict['keywords'] != None and dict['keywords'] != 'null':
            authors = dict['authors']
            for author in authors:
                if 'name' not in author:
                    return False
            return True
        else:
            return False
    else:
        return False

def docCreate(dict):
    id = dict['id']

    authors = dict['authors']
    keywords = dict['keywords']
    fields = dict['fos'] if 'fos' in dict else None
    refers = dict['references'] if 'references' in dict else None

    doi = dict['doi']
    title = dict['title']
    abstract = dict['abstract'] if 'abstract' in dict else None

    citation = dict['n_citation'] if 'n_citation' in dict else 0
    type = dict['type'] if 'type' in dict else None
    year = dict['year'] if dict['year'] != None else 1900

    firstKeyword = keywordsCreate(keywords)
    firstAuthor = authorsCreate(authors)

    doc = Document.objects.create(DocID=id,DOI=doi,title=title,abstract=abstract,mainBody=None,
                            firstKeyword=firstKeyword,firstAuthor=firstAuthor,pubYear=year,citation=citation)


    doc.firstField = fieldsCreate(fields) if (fields is not None) else None
    doc.firstRefer = refersCreate(refers) if (refers is not None) else None

    doc.save()

def refersCreate(refers):
    refer_ins_list = []
    for refer in refers:
        refer_ins_list.append(Refer.objects.create(DocID=refer))
    firstRefer = refer_ins_list[0]
    for i in range(0, len(refer_ins_list) - 1):
        refer = refer_ins_list[i]
        nextRefer = refer_ins_list[i + 1]
        refer.nextRefer = nextRefer
        refer.save()
    return firstRefer

def fieldsCreate(fields):
    field_ins_list = []
    for field in fields:
        field_ins_list.append(Field.objects.create(fieldName=field))
    firstField = field_ins_list[0]
    for i in range(0, len(field_ins_list) - 1):
        field = field_ins_list[i]
        nextField = field_ins_list[i + 1]
        field.nextField = nextField
        field.save()
    return firstField


def keywordsCreate(keywords):
    key_ins_list = []
    for key in keywords:
        if len(key) > 64:
            key = ' '.join(key.split()[:2])
        key_ins_list.append(Keyword.objects.create(key=key))
    firstKey = key_ins_list[0]
    for i in range(0,len(key_ins_list)-1):
        key = key_ins_list[i]
        nextKey = key_ins_list[i+1]
        key.nextKey = nextKey
        key.save()
    return firstKey

def authorsCreate(authors):
    author_ins_list = []
    for author in authors:
        author_ins_list.append(Author.objects.create(name=author['name']))
    firstAuthor = author_ins_list[0]
    for i in range(0,len(author_ins_list)-1):
        author = author_ins_list[i]
        nextAuthor = author_ins_list[i+1]
        author.nextAuthor = nextAuthor
        author.save()
    return firstAuthor

