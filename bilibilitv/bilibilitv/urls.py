from django.conf.urls import patterns, include, url
from settings import MEDIA_ROOT,STATIC_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^d-media/(?P<path>.*)$','django.views.static.serve',{'document_root':MEDIA_ROOT}),
    # url(r'^$', 'bilibilitv.views.home', name='home'),
    url(r'^myapp/', include('myapp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
