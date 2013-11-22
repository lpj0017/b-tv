# coding=UTF-8
import urllib
import hashlib
import simplejson
import requests

public_key = 'cead0936ae1be654a5ba0e7b1ee2b37b'
app_key = 'b445a8268bac4eed'
app_secret = '3aa29a3f7f43a2a0236582930830bd44'

def md5(s):
    return hashlib.md5(s).hexdigest()

def implode(sep,array):
    li = []
    for k,v in array.items():
        li.append(k)
        li.append(v)
    return sep.join(li)

def rawurlencode(string):
    return urllib.quote(string)

def ksort(d):
    return [(k,d[k]) for k in sorted(d.keys())]

def reset(tmp):
    pass

def get_sign(params,key):
    params = sorted(params.items())
    sign = urllib.urlencode(params)
    return {'sign':md5(sign+key).lower(),'params':sign}

def bangumi_data(btype=None,weekday=None):

    params = {}
    params['type']='json'
    params['appkey'] = app_key 
    
    if btype:
        params['btype'] = btype

    if weekday:
        params['weekday'] = weekday
    
#    sign_dict = get_sign(params,app_secret)


    params['sign'] = get_sign(params,app_secret)['sign'] 
#    query  = sign_dict['params'] + '&sign='+sign_dict['sign'] 
#    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params'] 

    url = 'http://api.bilibili.tv/bangumi'

    content = urllib.urlopen('%s?%s' % (url,query)).read()

    data = simplejson.loads(content)

    return data

def list_data(tid='',page=1,pagesize=30,ver=2,order='default',pinyin='a'):

    params = {}
    params['type'] = 'json'
    params['appkey'] = app_key

#    params['tid'] = tid
    params['page'] = page
    params['pagesize'] = pagesize
#    params['ver'] = ver
    params['order'] = order
#    params['pinyin'] = pinyin

    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params']

    url = 'http://api.bilibili.tv/list'

    content = urllib.urlopen('%s?%s' % (url,query)).read()
    data = simplejson.loads(content)

    return data



def index_data():
    params = {}
    params['type'] = 'json'
    params['appkey'] = app_key

    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params']

    url = 'http://api.bilibili.tv/index'

    content = urllib.urlopen('%s?%s' % (url,query)).read()
#    content = urllib.urlopen(url).read()
    data = simplejson.loads(content)
    return data

def recommend_data(tid=None, page=1,pagesize=30,order='default'):
    params = {}
    params['type'] = 'json'
#    params['appkey'] = app_key

    if tid:
        params['tid'] = tid
    params['page'] = page
    params['pagesize'] = pagesize
    params['order'] = order

    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params']

    url = 'http://api.bilibili.tv/recommend'

    content = urllib.urlopen('%s?%s' % (url,query)).read()

    data = simplejson.loads(content)
    return data

def search_data(keyword='',page=1,pagesize=20,order='default'):
    params={}
#    params['type'] = 'json'
    params['appkey'] = app_key

    if keyword:
        params['keyword'] = keyword.encode('utf8')

#    params['page'] = page
#    params['pagesize'] = pagesize
#    params['order'] = order

    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params']

    url = 'http://api.bilibili.tv/search'

    content = urllib.urlopen('%s?%s' % (url,query)).read()
    data = simplejson.loads(content)
    return data

def view_data(id,page='1'):
    params = {}
    params['appkey'] = app_key

    params['id'] = id
    params['page'] = page

    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params']

    url = 'http://api.bilibili.tv/view?%s' % (query)
    content = requests.get(url).content
    data = simplejson.loads(content)
     
    return data

