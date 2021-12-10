import json
import http.client  # 修改引用的模块
import hashlib  # 修改引用的模块
from urllib import parse
import random

def zhToEn(word):
    return baiDuTrans('zh','en',word)

def enToZh(word):
    return baiDuTrans('en','zh',word)

def baiDuTrans(fromLang,toLang,q):
    appid = '20211208001022635'  # 你的appid
    secretKey = 'xYLaK0eGKpAJzkArjyEr'  # 你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'

    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    dst = None
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        # 转码
        html = response.read().decode('utf-8')
        html = json.loads(html)
        dst = html["trans_result"][0]["dst"]
    except Exception as e:
        return str(e)
    finally:
        if httpClient:
            httpClient.close()
    return dst

def langDistinguish(q):
    appid = '20211208001022693'  # 你的appid
    secretKey = 'eYgkiOKnR8VM2zASjvCS'  # 你的密钥
    httpClient = None
    myurl = 'https://fanyi-api.baidu.com/api/trans/vip/language'

    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    #'https://fanyi-api.baidu.com/api/trans/vip/language?q=hello&salt=12333&sign=xxxxx&appid=123456789'
    myurl = myurl + '?q=' + parse.quote(q) + '&salt=' + str(salt) + '&sign=' + sign +'&appid=' + appid
    print(myurl)
    dst = None
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        # 转码
        html = response.read().decode('utf-8')
        html = json.loads(html)
        dst = html["data"]["src"]
    except Exception as e:
        return str(e)
    finally:
        if httpClient:
            httpClient.close()
    return dst