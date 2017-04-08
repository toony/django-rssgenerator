from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from rssgenerator.models import Rss

urlpatterns = [
    url(r'^$', ListView.as_view(
        queryset=Rss.objects.all(),
        context_object_name='all_rss',
        template_name='rssgenerator/index.html'
        ), name='index'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
        model=Rss,
        template_name='rssgenerator/detail.html'
        ), name='detail'),
    url(r'^(?P<rss_id>\d+)/rss/$', 'rssgenerator.views.rssstream', name='rssstream'),
    url(r'^(?P<rss_id>\d+)/gallery$', 'rssgenerator.views.rssgallery', name='rssgallery'),
    url(r'^(?P<rss_id>\d+)/gallery/random$', 'rssgenerator.views.rssgalleryrandom', name='rssgalleryrandom'),
    url(r'^(?P<rss_id>\d+)/(?P<item_id>\d+)/gallery$', 'rssgenerator.views.itemgallery', name='itemgallery'),
    url(r'^(?P<rss_id>\d+)/itemNumber/(?P<item_number>\d*)$', 'rssgenerator.views.itemnumber', name='itemnumber'),
    url(r'^(?P<rss_id>\d+)/localStore/(?P<item_id>\d+)/(?P<link_id>\d+)/get$', 'rssgenerator.views.localstoreretrieve', name='localstoreretrieve')
]
