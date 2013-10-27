# Create your views here.
from common import test_link
import simplejson
from django.http import HttpResponse

def test_view(request):
    json_data = test_link()
    json_str = simplejson.dumps(json_data,ensure_ascii=False,indent=4,separators=(',\n',':'))    

    return HttpResponse(json_str,content_type='application/json')

