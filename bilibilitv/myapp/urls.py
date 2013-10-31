from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
        (r'^api/bangumi/$',api_bangumi_view),
        (r'^api/index/$',api_index_view),
        (r'^api/recommend/$',api_recommend_view),
        (r'^api/search/$',api_search_view),
        (r'^api/view/$',api_view_view),

        (r'^integrated/(?P<page>\d+)/$',integrated_view),
        (r'^sp/(?P<page>\d+)/$',list_sp_view),
        (r'^topic/$',topic_view),
        (r'^search/$',search_view),
)
