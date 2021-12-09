import re

string = '''
{'query': {'bool': {'must': [{'bool': {'should': [{'match': {'title': 'Leptoquarks'}}, {'match': {'title': 'math'}}]}}, {'bool': {'must': [{'match':
{'authors': 'G. Aad'}}, {'bool': {'must_not': {'match': {'authors': 'T. Gejo'}}}}]}}]}}}

'''

print(string.replace('\'','\"'))