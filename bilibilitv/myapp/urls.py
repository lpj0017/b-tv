from django.conf.urls import patterns, include, url
from views import *
from django.views.decorators.cache import cache_page

TIME_OUT = 60*60*8

urlpatterns = patterns('',
        (r'^api/bangumi/$',cache_page(TIME_OUT)(api_bangumi_view)),
        (r'^api/index/$',cache_page(TIME_OUT)(api_index_view)),
        (r'^api/recommend/$',cache_page(TIME_OUT)(api_recommend_view)),
        (r'^api/search/$',cache_page(TIME_OUT)(api_search_view)),
        (r'^api/view/$',cache_page(TIME_OUT)(api_view_view)),

        (r'^integrated/(?P<page>\d+)/$',cache_page(TIME_OUT)(integrated_view)),
        (r'^sp/(?P<page>\d+)/$',cache_page(TIME_OUT)(list_sp_view)),
        (r'^topic/$',cache_page(TIME_OUT)(topic_view)),
        (r'^search/$',cache_page(TIME_OUT)(search_view)),
        (r'^sp_detail/$',cache_page(TIME_OUT)(sp_view)),
        (r'^comment/$',cache_page(TIME_OUT)(comment_view)),

        (r'^generate/$',generate_view),

)
