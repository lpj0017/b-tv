from django.conf.urls.defaults import *
from views import test_view

urlpatterns = patterns('',
        (r'^test/$',test_view),
        )
