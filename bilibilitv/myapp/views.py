# Create your views here.
from common import bangumi_data,index_data,recommend_data,search_data
import simplejson
from django.http import HttpResponse
from lxml import etree
from lxml.html import fromstring
import urllib
import requests
from api import my_http_response,api_bangumi_view,api_index_view,api_recommend_view,api_search_view,api_view_view
import re

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
        data_dict['description'] = node.xpath('div[@class="info"]')[0].text_content()
        data_dict['other'] = node.xpath('div[@class="artInfo"]')[0].text_content()
        art_list.append(data_dict)
    

    return my_http_response(art_list)

def topic_view(request):
    url = request.GET.get('url','')
    content = requests.get(url).content
    doc = fromstring(content)
    doc.make_links_absolute(base_url='http://www.bilibili.tv')

    image = doc.xpath('//div[@class="z-txt"]/img')[0].get('src')
    maps = doc.xpath('//div[@class="z-txt"]/map/area')

    area_list = []
    for area in maps:
        data_dict = {}
        data_dict['shape'] = 'rect'
        data_dict['coords'] = area.get('coords')
        data_dict['href'] = area.get('href')
        art_list.append(data_dict)

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
        data_dict['other'] = node.xpath('div[@class="info"]')[0].text_content()
        data_dict['description'] = node.xpath('div[@class="intro"]')[0].text_content()
        data_dict['tag'] = []
        tag_list = node.xpath('ul[@class="tag"]/li')
        for tag in tag_list:
            data_dict['tag'].append(tag.text_content())
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
    content = requests.get(url).content
    doc = fromstring(content)
    doc.make_links_absolute(base_url='http://www.bilibili.tv')
    

