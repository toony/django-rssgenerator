from django.conf.urls import url
from django.views.generic import DetailView, ListView
from rssgenerator.models import Rss
from rssgenerator.views import rssSummary, rsslogout, rssStream, rssGallery, searchItem, itemSummary, itemGallery, localStoreRetrieve

urlpatterns = [
    url(r'^$', ListView.as_view(
        queryset=Rss.objects.all(),
        context_object_name='all_rss',
        template_name='rssgenerator/index.html'
        ), name='index'),
    url(r'^(?P<rss_id>\d+)/$', rssSummary, name='rssSummary'),
    url(r'^(?P<rss_id>\d+)/logout$', rsslogout, name='rsslogout'),
    url(r'^(?P<rss_id>\d+)/rss/$', rssStream, name='rssStream'),
    url(r'^(?P<rss_id>\d+)/gallery$', rssGallery, name='rssGallery'),
    url(r'^(?P<rss_id>\d+)/search$', searchItem, name='searchItem'),
    url(r'^(?P<rss_id>\d+)/(?P<item_id>\d+)/summary$', itemSummary, name='itemSummary'),
    url(r'^(?P<rss_id>\d+)/(?P<item_id>\d+)/gallery$', itemGallery, name='itemGallery'),
    url(r'^(?P<rss_id>\d+)/localStore/(?P<item_id>\d+)/(?P<link_id>\d+)/get$', localStoreRetrieve, name='localStoreRetrieve')
]
