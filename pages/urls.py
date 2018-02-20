from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})\/(?P<month>\d{1,2})\/(?P<day>\d{1,2})\/(?P<slug>\S+)$', views.page, name='page'),
    #url('posts/(?P<slug>.*)', views.post, name='post'),
    url(r'^(?:rss(?:\.xml)?)|(?:feed(?:.xml)?)$', views.rss, name='rss'),
    url(r'^$', views.index, name='index'),
]

