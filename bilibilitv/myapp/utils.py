# coding=UTF-8
from django.core.files import File
from models import Video,Part
from django.http import HttpResponse
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
#from django.core.management import setup_environ
#from bilibilitv import settings
from bilibilitv.settings import MEDIA_ROOT 
from django.core.files.base import ContentFile

#STATIC_ROOT = os.path.dirname(__file__)
#DOWNLOAD_ROOT = os.path.join(MEDIA_ROOT,'downloads')

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
    
    print '@32,video source url \n',url

    video = {}
    req = requests.get(url)
    result = 'error'
    if req.headers['content-type'].startswith('text/xml'):
        content = req.content
        parser = etree.XMLParser(strip_cdata=False)
        doc = etree.XML(content, parser)
        node = doc.xpath('//result')
        if len(node) > 0 :
            result = node[0].text
    
    if result != 'error':
        video['result'] = result
        video['timelength'] = doc.xpath('//timelength')[0].text
#        video['framecount'] = doc.xpath('//framecount')[0].text
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
    else:
        return {'result':result}
    

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
        file_name = os.path.join(MEDIA_ROOT,'%s/%s'% (sub_dir,file_name))
    else:
        file_name = os.path.join(MEDIA_ROOT,file_name)
    
    size = 0
    if os.path.exists(file_name):
        size = os.path.getsize(file_name)


    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
#    don't repeatly download the same file
    if file_size == size:
        return file_name

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

def save_convert_flv_to_mp4(txt_file_path,mp4_file_path):
    temp_file = os.path.join(os.path.dirname(txt_file_path),'temp.flv')
    # merge flv files to one first
    code = os.system((u'ffmpeg -f concat -i "%s" -c copy "%s" 2> /var/tmp/ffmpeg.log' % (txt_file_path,temp_file)).encode('utf8'))
    # then convert flv to mp4 file 
    # this worked,but slow
    if code == 0:
        code = os.system((u'ffmpeg -i "%s" "%s" 2> /var/tmp/ffmpeg.log' % (temp_file,mp4_file_path)).encode('utf8'))
    
    return code


def convert_flv_to_mp4(old_file,new_file):
    os.system('ffmpeg -i "%s" "%s" 2> /var/tmp/ffmpeg.log' % (old_file,new_file))
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
    list_txt = os.path.join(MEDIA_ROOT,'%s/list.txt' % (video_title))
    status_txt = os.path.join(os.path.dirname(list_txt),'finished.txt')
    mp4= os.path.join(MEDIA_ROOT,'%s/%s.mp4'%(video_title,video_title))
    
    if os.path.exists(status_txt):
        return 0, mp4


    if source_json['result']!='error':
        url_list= source_json['durl']
        url_list = sort_list_by_order(url_list)
        file_list = []
        
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

        command = u'ffmpeg -f concat -i "%s" -c copy "%s"' % (list_txt,mp4)
        command = command.encode('utf8')
        code = os.system(command)
        print code,command,'@203'
        if code != 0:
            if os.path.exists(mp4):
                os.remove(mp4)
            print code,'@207'
            code = save_convert_flv_to_mp4(list_txt,mp4)
            if code != 0:
                return code,None
        command = (u'echo "ok" > "%s"' % (status_txt)).encode('utf8') 
        os.system(command)
        print code ,'@212'
        return code,mp4
    else:
        return None,None

def save_part(data_dict, video,file_path):
    part_list = Part.objects.filter(cid=data_dict['cid'])

    f = open(file_path)
    if part_list.count() == 0:
        part = Part(cid=data_dict['cid'])
        part.name = data_dict['partname']
        if part.name == '':
            part.name = data_dict['title']
        part.desc = data_dict['description']
        part.video = video
        part.mp4.save('%s.mp4' % part.name, File(f))
        part.save()
    else:
        part = part_list[0]
        if not part.mp4:
            part.mp4.save('%s.mp4' % part.name, File(f))
            part.save()
    f.close()

def generate_view(request):

    bilibili_url = request.GET.get('url','') #sys.argv[1]
    aid = get_aid(bilibili_url)
    
    if not aid:
        sys.exit()
    data_dict = view_data(aid)
    error = data_dict.get('error','')

    if error:
#        remove the data which have problem
        print '@253', error
        return HttpResponse('finished')

    cid,pages = data_dict['cid'],int(data_dict['pages'])

#    source_json = get_video_source(cid)
    video_list = Video.objects.filter(aid = aid)
    
    if len(video_list) == 0:
        v = Video(aid=aid)
        v.title = data_dict['title']
        v.pic_url = data_dict['pic']
        v.save()
    else:
        v = video_list[0]

    for i in range(1,pages+1):
        time.sleep(5)
        data_dict = view_data(aid,i)
        cid = data_dict['cid']
        source_json = get_video_source(cid)
#        print '@267',source_json

        code,path = get_video(source_json,'%s' % (data_dict['title']))
        print '@267',code,path
        if code == 0 and path: 
            save_part(data_dict,v,path)

    return HttpResponse('finished')

