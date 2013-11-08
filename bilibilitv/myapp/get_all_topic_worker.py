import requests
import sys
import simplejson
from urlparse import urlparse
import urllib
import sys
import os
import time
def generate_topic_video(href):
    if href:
        o = urlparse(href)
        path = o.path

        if path.startswith('/video'):
            data_dict = {}
            data_dict['url'] = href
            query = urllib.urlencode(data_dict)

            url = 'http://localhost:8000/myapp/generate/?%s' % query
            time.sleep(5)
            content = requests.get(url).content
            
            return content
        else:
            print '********@28,error href is:%s' % (href)

            return None 
    return None 

url_list = []
for i in range(1,218):
    data = requests.get('http://localhost:8000/myapp/integrated/%d/' % i )
    content = data.content
    data_list = simplejson.loads(content)
    
    for data in data_list:
        url = data['link']
        url_list.append(url)

for url in url_list:
    o = urlparse(url)
    path = o.path
    if path.startswith('/topic'):
        data_dict = {}
        data_dict['url'] = url
        print '@26,topic source url is: %s' % (url)
        query = urllib.urlencode(data_dict)

        request_url = 'http://localhost:8000/myapp/topic/?%s' % query
        content = requests.get(request_url).content

        data = simplejson.loads(content)
        
        for dic in data['map']:
            href = dic['href']
            print '****@36,video href is: %s' % (href)
            res = generate_topic_video(href)

            if res == None:
                pass
            elif res == 'finished':
                pass
            else:
                print '****@62,error!! result is\n %s' % (res)
                
                fout = open('error.html','w')
                fout.write(res)
                fout.close()

                sys.exit(1)



