import urllib
import hashlib

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

print get_sign({'utk':'xx','time':'xx'},'3aa29a3f7f43a2a0236582930830bd44')
