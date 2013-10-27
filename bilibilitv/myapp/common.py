import urllib
import hashlib
import simplejson


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
#    return tmp[0]
    pass

def get_sign(params,key):
    data = {} 
    ksort(params)
    reset(params)
#    for k,v in params.items():
#        data[k] = rawurlencode(v)
    data = urllib.urlencode(params)
    print 31,data
    sign = data 

    return {'sign':md5(sign+key).lower(),'params':sign}

def test_link():
    public_key = 'cead0936ae1be654a5ba0e7b1ee2b37b'
    app_key = 'b445a8268bac4eed'
    app_secret = '3aa29a3f7f43a2a0236582930830bd44'

    params = {}
    params['type']='json'
    params['appkey'] = app_key 

    params['sign'] = get_sign(params,app_secret)['sign']
    query = get_sign(params,app_secret)['params'] 
    print 47,query

    url = 'http://api.bilibili.tv/bangumi'

    content = urllib.urlopen('%s?%s' % (url,query)).read()

    data = simplejson.loads(content)

    return data



