import re

string = '''
{'query': {'bool': {'must': [{'bool': {'should': [{'match': {'title': 'Leptoquarks'}}, {'match': {'title': 'math'}}]}}, {'bool': {'must': [{'match': {'authors': 'G. Aad'}}, {'bool': {'must_not': {'match': {'aut
hors': 'T. Gejo'}}}}]}}]}}}
'''

print(string.replace('\'','\"'))