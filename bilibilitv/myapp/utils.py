# coding=UTF-8
from urlparse import urlparse
from lxml import etree
from lxml.html import fromstring
import requests
import simplejson
from common import view_data
import sys
import urllib2
import os
import time

STATIC_ROOT = os.path.dirname(__file__)
DOWNLOAD_ROOT = os.path.join(STATIC_ROOT,'downloads')

def get_aid(url):
    o = urlparse(url)
    path = o.path
    fragments = path.split('/')
    
    fragments = filter(lambda x:x!='',fragments)
    
    for value in fragments:
        if value.find('av')>=0:
            result = value.replace('av','')
            return result 
    

def get_video_source(cid):
    url = 'http://interface.bilibili.tv/playurl?cid=%s' % (cid)
    
    print '@32',url

    res = requests.get(url)
    content = res.content

    parser = etree.XMLParser(strip_cdata=False)
    doc = etree.fromstring(content,parser)
    result = doc.xpath('//result')[0].text
    
    if result != 'error':
        video = {}
        video['result'] = result
        video['timelength'] = doc.xpath('//timelength')[0].text
        video['framecount'] = doc.xpath('//framecount')[0].text
        video['src'] = doc.xpath('//src')[0].text
        
        video['durl'] = []
        
        durls = doc.xpath('//durl')
        
        for node in durls:
            data = {}
            data['order'] = node.xpath('order')[0].text
            data['length'] = node.xpath('length')[0].text
            data['url'] = node.xpath('url')[0].text
            video['durl'].append(data)

        return video
    
    return simplejson.loads(content)

def get_comment_source(cid):
    url = 'http://comment.bilibili.tv/%s.xml' % (cid)
    content = requests.get(url).content
    doc = fromstring(content)
    
    data_dict = {}
    data_dict['chatserver'] = doc.xpath('//chatserver')[0].text_content()
    data_dict['chatid'] = cid
    data_dict['mission'] = doc.xpath('//mission')[0].text_content()
    data_dict['source'] = doc.xpath('//source')[0].text_content()

    dnode_list = doc.xpath('//d')
    data_dict['d'] = []
    for node in dnode_list:
       node_dict = {}
       node_dict['p'] = node.get('p')
       node_dict['text'] = node.text_content()
       data_dict['d'].append(node_dict)
    
    return data_dict

def download_file(url,sub_dir=''):
    file_name = url.split('/')[-1]
    if file_name.find('?')>=0:
#        fix for sina video
        file_name = file_name.split('?')[0]

    if sub_dir:
        file_name = os.path.join(DOWNLOAD_ROOT,'%s/%s'% (sub_dir,file_name))
    else:
        file_name = os.path.join(DOWNLOAD_ROOT,file_name)

    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

#    check file download complete
    download_size = os.path.getsize(file_name)
    if file_size != download_size:
        download_file(url,sub_dir=sub_dir)

    return file_name

def convert_flv_to_mp4(old_file,new_file):
    os.system('ffmpeg -i "%s" "%s"' % (old_file,new_file))
    return new_file

def merge_files(file_list,new_file):
    fout = file(new_file,'wb')

    for n in file_list:
        fin = file(n,'rb')
        while True:
            data = fin.read(65536)
            if not data:
                break
            fout.write(data)
        fin.close()
    fout.close()

def sort_list_by_order(li):
    new_list = sorted(li,key=lambda k:k['order'])
    return new_list

def get_video(source_json,video_title=''):
    if source_json['result']!='error':

        print '@121',source_json
        print '@122',video_title

        url_list= source_json['durl']
        url_list = sort_list_by_order(url_list)
        file_list = []
        list_txt = os.path.join(DOWNLOAD_ROOT,'%s/list.txt' % (video_title))

        if not os.path.exists(os.path.dirname(list_txt)):
            os.makedirs(os.path.dirname(list_txt))
            
        f = open(list_txt,'wb')
        for d in url_list:
            source_url = d['url']
            file_name = download_file(source_url,video_title)
            file_name = file_name.split('/')[-1]
            file_list.append(file_name)
            
            f.write("file '%s'\n" % (file_name))

        f.close()
        print '@146,download ok.'

        mp4= os.path.join(DOWNLOAD_ROOT,'%s/%s-%s.mp4'%(video_title,aid,cid))
        command = u'ffmpeg -f concat -i %s -c copy %s' % (list_txt,mp4)
        command = command.encode('utf8')
        os.system(command)

if __name__ == '__main__':
#    download the video and megre it to mp4 file then upload to oss
    bilibili_url = sys.argv[1]
    aid = get_aid(bilibili_url)
    
    if not aid:
        print "Sorry,can't get aid"
        sys.exit()
    data_dict = view_data(aid)

    cid,pages = data_dict['cid'],int(data_dict['pages'])

#    source_json = get_video_source(cid)
    
    for i in range(1,pages+1):
        print '@133,read for get video at page %d' % i
        time.sleep(1)
        data_dict = view_data(aid,i)
        cid = data_dict['cid']
        source_json = get_video_source(cid)
        get_video(source_json,data_dict['partname'])


