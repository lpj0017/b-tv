# coding=UTF-8
import requests
import sys
import simplejson
from urlparse import urlparse
import urllib
import sys
import os
import time
from models import VideoURL

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
            return None 
    return None 


def make_topic(number = 10):
#url_list = []
#    for i in range(1,number+1):
    data = requests.get('http://localhost:8000/myapp/integrated/%d/' % number )
    content = data.content
    data_list = simplejson.loads(content)
    
    for data in data_list:
        url = data['link']
#        url_list.append(url)
        make_video_link(url)

def store_video_url(url):
    query = VideoURL.objects.filter(url=url)
    if query.count() == 0:
        v = VideoURL(url=url)
#        v.is_saved = True
        v.save()

def make_video_link(url):
#video_list = []
#    for url in url_list:
    o = urlparse(url)
    path = o.path
    if path.startswith('/topic'):
        data_dict = {}
        data_dict['url'] = url
        print u'@26,topic source url is: %s' % (url)
        query = urllib.urlencode(data_dict)

        request_url = 'http://localhost:8000/myapp/topic/?%s' % query
        content = requests.get(request_url).content

        data = simplejson.loads(content)
        
        for dic in data['map']:
            href = dic['href']
            
            if href == None:
                continue

            o = urlparse(href)
            p = o.path

            if p.startswith('/video'):
#                video_list.append(href)
                store_video_url(href)
            elif p.startswith('/sp'):

                param_dict ={}

                if not isinstance(p,str):
                    p = urllib.quote(p.encode('utf8'))
                    href = 'http://%s%s' % (o.netloc,p)
                print '****@71 sp url: %s' % href

                param_dict['url'] = href
                query = urllib.urlencode(param_dict)
                sp_url = 'http://localhost:8000/myapp/sp_detail/?%s' % (query)
                content = requests.get(sp_url).content
                sp_dict = simplejson.loads(content)
                
                video_info = sp_dict.get('video', None)
                page_count = '0'

                if  video_info:
                    page_count = sp_dict['video']['page_count']

                for i in range (1,int(page_count)+1):
                    param_dict['page'] = i
                    query = urllib.urlencode(param_dict)
                    sp_url = 'http://localhost:8000/myapp/sp_detail/?%s' % (query)
                    time.sleep(3)
                    content = requests.get(sp_url).content
                    sp_dict = simplejson.loads(content)
                    sp_video_list = sp_dict['video']['list']

                    for video in sp_video_list:
                        href = video['link']
#                        video_list.append(href)
                        store_video_url(href)
#            res = generate_topic_video(href)

#            if res == None:
#                pass
#            elif res == 'finished':
#                pass
#            else:
#                print '****@62,error!! result is\n %s' % (res)
#                
#                fout = open('error.html','w')
#                fout.write(res)
#                fout.close()

#                sys.exit(1)

#print '@98 finished:list number is %d' % (len(video_list))

#fout = open('result_url.txt','w')
#for line in video_list:
#    if line:
#        line = '%s\n' % line.encode('utf8')
#        fout.write(line)
#fout.close()
