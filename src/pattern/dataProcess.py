import json
filename = 'D:\下载目录\\aminer_papers_0.txt'
with open(filename, 'r') as file_to_read:
    for i in range(10):
        line = file_to_read.readline()
        json_dict = json.loads(line)
        print(json_dict)