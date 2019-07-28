from django.conf.urls import url
from django.views.generic import DetailView, ListView
from rssgenerator.models import Rss
from rssgenerator.views import rssstream, rssdetails, rssgallery, searchItem, itemsummary, itemgallery, localstoreretrieve

urlpatterns = [
    url(r'^$', ListView.as_view(
        queryset=Rss.objects.all(),
        context_object_name='all_rss',
        template_name='rssgenerator/index.html'
        ), name='index'),
    url(r'^(?P<rss_id>\d+)/$', rssdetails, name='detail'),
    url(r'^(?P<rss_id>\d+)/rss/$', rssstream, name='rssstream'),
    url(r'^(?P<rss_id>\d+)/gallery$', rssgallery, name='rssgallery'),
    url(r'^(?P<rss_id>\d+)/search$', searchItem, name='searchitem'),
    url(r'^(?P<rss_id>\d+)/(?P<item_id>\d+)/summary$', itemsummary, name='itemsummary'),
    url(r'^(?P<rss_id>\d+)/(?P<item_id>\d+)/gallery$', itemgallery, name='itemgallery'),
    url(r'^(?P<rss_id>\d+)/localStore/(?P<item_id>\d+)/(?P<link_id>\d+)/get$', localstoreretrieve, name='localstoreretrieve')
]
