# Create your views here.
from common import bangumi_data,index_data,recommend_data,search_data,view_data
import simplejson
from django.http import HttpResponse

def my_http_response(data):
    json_str = simplejson.dumps(data,ensure_ascii=False,indent=4,separators=(',\n',':'))    
    return HttpResponse(json_str,content_type='application/json;charset=utf-8')

def api_bangumi_view(request):
    json_data = bangumi_data()
    return my_http_response(json_data)

def api_index_view(request):
   json_data = index_data()
   return my_http_response(json_data)

def api_recommend_view(request):
    tid = request.GET.get('tid',None)
    page = request.GET.get('page','1')
    pagesize = request.GET.get('pagesize','30')
    order = request.GET.get('order','default')
    json_data = recommend_data(tid=tid,page=page,pagesize=pagesize,order=order)
    return my_http_response(json_data)

def api_search_view(request):
    keyword = request.GET.get('keyword','')
    page = request.GET.get('page','1')
    pagesize = request.GET.get('pagesize','20')
    order = request.GET.get('order','default')

    json_data = search_data(keyword=keyword,page=page,pagesize=pagesize,order=order)

    return my_http_response(json_data)

def api_view_view(request):
    id = request.GET.get('id','')
    page = request.GET.get('page','1')
    
    if id and page:
        json_data = view_data(id,page)
        return my_http_response(json_data)

    return my_http_response({'error':'need id and page param.'})

