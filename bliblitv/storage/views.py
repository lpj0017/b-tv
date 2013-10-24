# Create your views here.
from django.shortcuts import render_to_response
from django.forms import ModelForm
from storages.models import MyStorage 
from django.template import Context,RequestContext

class MyStorageForm(ModelForm):
    class Meta:
        model = MyStorage


def test_view(request):
    form = MyStorageForm()    
    if request.POST:
        form = MyStorageForm(request.POST, request.FILES)
        form.save()
    return render_to_response('test.html' ,{'form':form},context_instance=RequestContext(request))
