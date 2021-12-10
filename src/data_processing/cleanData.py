import json
import re
def legalDocDate(dict):
    if 'doi' in dict and 'authors' in dict and 'keywords' in dict and 'year' in dict\
        and 'fos' in dict and 'abstract' in dict and 'doc_type' in dict and 'publisher' in dict :
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

DocNum = 1000000
fw = 'D:\下载目录\clean\\org_final.txt'
fr = 'D:\下载目录\\mag_papers_20.txt'
with open(fw, 'a') as file_to_write:
    with open(fr, 'r') as file_to_read:
        useable = 0
        while (useable<DocNum):
            line = file_to_read.readline()
            if not line:
                break
            json_dict = json.loads(line)
            if legalDocDate(json_dict):
                replace_line  = re.sub('(Abstract)?#((R|N)#+)+',' ',line) #去除abstract中的乱码
                file_to_write.writelines(replace_line)
                useable = useable + 1
                if useable % 1000 == 0:
                    print(format(useable,',')+' docs loaded')
print(str(useable) + ' docs finally loaded')