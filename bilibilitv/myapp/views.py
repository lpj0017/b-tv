# coding=UTF-8
# Create your views here.
from django.views.decorators.cache import cache_page
from common import bangumi_data,index_data,recommend_data,search_data,view_data
import simplejson
from django.http import HttpResponse
from lxml import etree
from lxml.html import fromstring
import urllib
import requests
from api import my_http_response,api_bangumi_view,api_index_view,api_recommend_view,api_search_view,api_view_view
import re
from urlparse import urlparse
from utils import get_aid,get_video_source,get_comment_source,generate_view
from models import Topic,Part,Video
from get_all_topic_worker import make_topic
def save_topic(data_dict):
    topic_list = Topic.objects.filter(title=data_dict['title'])
    
    if topic_list.count() == 0:
        t = Topic(title=data_dict['title'])
        t.image_url = data_dict['image']
        t.link = data_dict['link']
        t.desc = data_dict['desc']
        t.date = data_dict['date']
        t.user = data_dict['user']
        t.clicked=data_dict['clicked']
        t.comments = data_dict['comments']
        t.save()

def integrated_view(request,page):
    url = 'http://www.bilibili.tv/topic/integrated-%s.html' % (page)
#    url = 'http://www.baidu.com'
    content = requests.get(url).content#.decode('utf-8')
    doc = fromstring(content)
    doc.make_links_absolute(base_url='http://www.bilibili.tv')

    node_list = doc.xpath('//div[@class="art_list"]//li')

    art_list = [] 

    for node in node_list:
        data_dict = {}
        data_dict['image'] = node.xpath('a/img')[0].get('src')
        data_dict['link'] = node.xpath('a[@target="_blank"]')[0].get('href')
        data_dict['title'] = node.xpath('h2')[0].text_content()
        data_dict['desc'] = node.xpath('div[@class="info"]')[0].text_content()
#        data_dict['other'] = node.xpath('div[@class="artInfo"]')[0].text_content()
        art_info = node.xpath('div[@class="artInfo"]')[0]
        data_dict['date'] = art_info.xpath('span[@id="p_date"]')[0].text_content()
        data_dict['user'] = art_info.xpath('span[@id="p_user"]')[0].text_content()
        data_dict['clicked'] = art_info.xpath('span[@id="p_click"]')[0].text_content()
        data_dict['comments'] = art_info.xpath('span[@id="p_pl"]')[0].text_content()
        art_list.append(data_dict)
        save_topic(data_dict)
    

    return my_http_response(art_list)

def topic_view(request):
    url = request.GET.get('url','')
    content = requests.get(url).content
    doc = fromstring(content)
    doc.make_links_absolute(base_url='http://www.bilibili.tv')

    images = doc.xpath('//div[@class="z-txt"]/img')
    if len(images) == 0:
        images = doc.xpath('//img[@usemap]')
    
    if len(images)!=0: 
        image = images[0].get('src')
    else:
        image = ''

    maps = doc.xpath('//map/area')


    area_list = []
    for area in maps:
        data_dict = {}
        data_dict['shape'] = 'rect'
        data_dict['coords'] = area.get('coords')
        data_dict['href'] = area.get('href')
        area_list.append(data_dict)

    result = {}
    result['image'] = image
    result['map'] = area_list

    return my_http_response(result)

def search_view(request):
    param_dict={}
    param_dict['keyword'] = request.GET.get('keyword','').encode('utf8')
    param_dict['page'] = request.GET.get('page','1')
    param_dict['pagesize'] = '100'

    url = 'http://www.bilibili.tv/search?%s' % (urllib.urlencode(param_dict))
    
    content = requests.get(url).content
    doc = fromstring(content)
    doc.make_links_absolute(base_url = 'http://www.bilibili.tv')
    
    page_box = doc.xpath('//div[@class="pagelistbox"]/span')[0].text_content().split('/')[0]
    page_count = re.sub(r'[^\d]','',page_box)
    
    results = doc.xpath('//ul[@class="search_result"]/li')

    data_list =  []
    for node in results:
        data_dict = {}
        data_dict['image'] = node.xpath('a/img')[0].get('src')
        data_dict['link'] = node.xpath('a')[0].get('href')
        data_dict['type'] = node.xpath('*/div[@class="t"]/span')[0].text_content()
        data_dict['title'] = node.xpath('*/div[@class="t"]')[0].text_content()
        users = node.xpath('div[@class="info"]/a')
        data_dict['users'] = [] 
        data_dict['other'] = node.xpath('div[@class="info"]')[0].text_content().replace(u'UP主:','')
        for u in users:
            v = u.text_content()
            data_dict['users'].append(v)
            data_dict['other'] = data_dict['other'].replace(v,'')

        data_dict['description'] = node.xpath('div[@class="intro"]')[0].text_content()
        data_dict['tag'] = []
        tag_list = node.xpath('div[@class="s_tag"]/ul/li') 
        for tag in tag_list:
            v = tag.text_content()
            data_dict['tag'].append(v)
        data_list.append(data_dict)

    result={}
    result['page_count'] = page_count
    result['results'] = data_list

    return my_http_response(result)

def list_sp_view(request,page):
    url = 'http://www.bilibili.tv/list/sp-%s.html' % (page)
    content = requests.get(url).content
    doc = fromstring(content)
    doc.make_links_absolute(base_url='http://www.bilibili.tv')

    node_list = doc.xpath('//div[@class="spc_list"]/ul/li')

    results = {}
    page_info= doc.xpath('//div[@class="pagelistbox"]/span')[0].text_content().split('/')[0]
    page_count = re.sub(r'[^\d]','',page_info) 
    results['page_count'] = page_count
    results['list']=[]
    for node in node_list:
        data_dict = {}
        data_dict['link'] = node.xpath('a')[0].get('href')
        data_dict['image'] = node.xpath('a/img')[0].get('src')
        data_dict['title'] = node.xpath('*/div[@class="t"]')[0].text_content()
        data_dict['description'] = node.xpath('div[@class="info"]')[0].text_content()
        data_dict['other'] = node.xpath('div[@class="date"]')[0].text_content()
        
        results['list'].append(data_dict)

    return my_http_response(results)

def sp_view(request):
    url = request.GET.get('url','')
#    type = request.GET.get('type','ad')
#    order = request.GET.get('order','recommend')
    page = request.GET.get('page','1')

    content = requests.get(url).content
    doc = fromstring(content)
    doc.make_links_absolute(base_url='http://www.bilibili.tv')
    
    data_dict = {}
    data_dict['image'] = ''
    data_dict['title'] = ''
    data_dict['description'] = ''
    data_dict['other'] = ''

    image_nodes = doc.xpath('//div[@class="zt-i"]/img')
    if len(image_nodes)>0:
        image_node = image_nodes[0]
        data_dict['image'] = image_node.get('src') 

    title_nodes = doc.xpath('//div[@class="zt-i"]/h1')
    if len(title_nodes)>0:
        title_node = title_nodes[0]
        data_dict['title'] = title_node.text_content() 

    desc_nodes = doc.xpath('//p[@id="info-desc"]')
    if len(desc_nodes)>0:
        desc_node = desc_nodes[0]
        data_dict['description'] = desc_node.text_content() 

    other_nodes = doc.xpath('//div[@class="info"]/p[@class="ai"]')
    if len(other_nodes)>0:
        other_node = other_nodes[0]
        data_dict['other'] = other_node.text_content() 
    
    
    tags = doc.xpath('//div[@class="info"]/p[@class="tag"]')
    data_dict['tag'] = ''
    if len(tags) != 0:
       data_dict['tag'] = tags[0].text_content() 
#    data_dict['tag'] = doc.xpath('//div[@class="info"]/p[@class="tag"]')[0].text_content()

    script_list = doc.xpath('//script')

    spid = ''
    stype = ''
    order = ''
    for script in script_list:
        code = script.text_content()
        if code:
            lines = code.split(';')
            for line in lines:
                if line.find('var')>=0:
                    if line.find('spid')>=0:
                        spid = re.sub(r'[^\d]',r'',line)
                        data_dict['spid'] = spid

                if line.find('#sp_') >=0 and line.find('.click()')>=0:
                    m = re.findall(r'"(.+?)"',line)
                    stype = m[0].split('_')[-1]

            order = doc.xpath('//div[@id="sp_order"]')
            if len(order)>0:
                order = order[0].xpath('a[contains(@class,"on")]')[0].get('id')
                order = order.split('_')[-1]


    if spid:
        video_url = 'http://www.bilibili.tv/sppage/%s-%s-%s-%s.html' %(stype,order,spid,page)
        print '@215',video_url
        video_content = requests.get(video_url).content.decode('utf8')
        video_doc = fromstring(video_content)
        video_doc.make_links_absolute(base_url='http://www.bilibili.tv')
        
        page_count = 1 
        page_count_info = video_doc.xpath('//div[@class="pagelistbox"]/span')
        if len(page_count_info)>0:
            page_count_info = page_count_info[0].text_content().split('/')[0]
            page_count = re.sub(r'[^\d]',r'',page_count_info)

#        video_nodes = video_doc.xpath('//div[@class="po"]')
        video_nodes = video_doc.xpath('//li')
        video_list= []
        data_dict['video'] = {}
        for node  in video_nodes:
            video_dict = {}
            video_dict['image'] = node.xpath('*//img')[0].get('src')
            video_dict['link'] = node.xpath('*//a')[0].get('href')
            video_dict['title'] = node.xpath('*//div[@class="t"]')[0].text_content()
            video_dict['subtitle'] = node.xpath('div')[0].get('subtitle')
            video_dict['txt'] = node.xpath('div')[0].get('txt')
            

            video_list.append(video_dict)

        data_dict['video']['list'] = video_list
        data_dict['video']['page_count'] = page_count 

        for k,v in data_dict.items():
            if isinstance(v,basestring):
                data_dict[k] = v.strip()
    return my_http_response(data_dict)

def comment_view(request):
    url = request.GET.get('url','')
    page = request.GET.get('page','1')
    aid = get_aid(url)
     
#    data = view_data(aid) 

#    pages = int(data['pages'])
    result = {}
#    for i in range(1,pages+1):
    data_dict = view_data(aid,page)
    cid = data_dict['cid']
#    data_dict['video_source'] = get_video_source(cid)
    data_dict['comment_source'] = get_comment_source(cid)
    result['%s' % page] = data_dict

    return my_http_response(result)
    
def video_view(request):
    url = request.GET.get('url','')
    page = request.GET.get('page','1')

    aid = get_aid(url)
    
    data = view_data(aid,page)

    cid = data['cid']

    part_list = Part.objects.filter(cid=cid)
    
    if part_list.count() > 0 :
        return {'url':part.mp4}

def make_video_url_view(request):
    str_number = request.GET.get('number','1')
    number =  int(str_number)

    make_topic(number)

    return HttpResponse('work finished!')
