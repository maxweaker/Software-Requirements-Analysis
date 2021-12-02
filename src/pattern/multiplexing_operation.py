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

    if 'abstract' not in dict:
        dict['abstract'] = None

    if 'n_citation' not in dict:
        dict['n_citation'] = 0

    if 'type' not in dict:
        dict['type'] = None

    if 'year' not in dict:
        dict['year'] = None

    if 'references' not in dict:
        dict['references'] = None

    if 'fos' not in dict:
        dict['fos'] = None

    authors = []
    for author in dict['authors']:
        authors.append(author['name'])
    dict['authors'] = authors

    return dict
