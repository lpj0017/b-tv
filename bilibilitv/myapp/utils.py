from urlparse import urlparse
from lxml import etree
from lxml.html import fromstring
import requests
import simplejson
from common import view_data
import sys
import urllib2
import os


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
    url = 'http://interface.bilibili.tv/playurl?otype=json&cid=%s' % (cid)
    
    res = requests.get(url)
    content = res.content
    if res.headers['content-type'].find('text/xml')>=0:
        doc = fromstring(content)
        result = doc.xpath('//result')[0].text_content()
        return {'result':result}
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

def download_file(url):
    file_name = url.split('/')[-1]
    if file_name.find('?')>=0:
#        fix for sina video
        file_name = file_name.split('?')[0]

    if os.path.isfile(file_name):
        print '@58,',os.path.isfile(file_name)
        return file_name
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
    return file_name

def convert_flv_to_mp4(old_file,new_file):
    os.system('ffmpeg -i "%s" "%s" 2> /dev/null' % (old_file,new_file))
    
    return new_file
if __name__ == '__main__':
#    download the video and megre it to mp4 file then upload to oss
    bilibili_url = sys.argv[1]

    aid = get_aid(bilibili_url)
    
    if not aid:
        print "Sorry,can't get aid"
        sys.exit()
    data_dict = view_data(aid)

    cid,pages = data_dict['cid'],data_dict['pages']

    source_json = get_video_source(cid)
    if source_json['result']!='error':
        url_list= source_json['durl']
        print '@104,',url_list
        for d in url_list:
            source_url = d['url']
            file_name = download_file(source_url)
            new_file = file_name + '.mp4'
            convert_flv_to_mp4(file_name,new_file)
