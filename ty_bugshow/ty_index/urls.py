from django.conf.urls import include, url
from views import *
urlpatterns = [
    url(r'^$', test),
    url(r'^urls/add/post/$', addpost),
    url(r'urls/analy/init/', analyinit),
    url(r'urls/analy/list/', analylist),
    url(r'^urls/analy/$', analy),
    url(r'^urls/del/$', dele),
    url(r'^urls/add/$', add),
    url(r'^urls/', list),
]