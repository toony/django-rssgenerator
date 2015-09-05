import json
import RssToStream
import LocalStore
import random

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import formats
from django.templatetags.static import static

from rssgenerator.models import Rss, Items, Links

def rssstream(request, rss_id):
    rssToStream = RssToStream.RssToStream(request, get_object_or_404(Rss, id=rss_id))
    return HttpResponse(rssToStream.display())

def localstoreretrieve(request, rss_id, item_id, link_id):
    link = get_object_or_404(Links, id=link_id)
    localStore = LocalStore.LocalStore(rss_id)
    return HttpResponse(localStore.get(item_id, link), localStore.contentType(item_id, link))

def itemgallery(request, rss_id, item_id):
    item = get_object_or_404(Items, id=item_id)
    localStore = LocalStore.LocalStore(rss_id)
    
    itemGalleryIndex = []
    for link in item.links_set.all():
        linkInfos = { 'src': reverse('rss:localstoreretrieve', args=[rss_id, item.id, link.id]) }
        linkInfos.update(localStore.info(item.id, link))
        itemGalleryIndex.append(linkInfos)
    
    return HttpResponse(json.dumps(itemGalleryIndex), content_type="application/json")

def rssgallery(request, rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    localStore = LocalStore.LocalStore(rss_id)

    rssGalleryIndex = []
    for item in rss.items_set.all():
        for link in item.links_set.all():
            linkInfos = { 'src': reverse('rss:localstoreretrieve', args=[rss.id, item.id, link.id]) }
            linkInfos.update(localStore.info(item.id, link))
            rssGalleryIndex.append(linkInfos)

    return HttpResponse(json.dumps(rssGalleryIndex), content_type="application/json")

def itemnumber(request, rss_id, item_number):
    if item_number == "":
        raise Http404("Undefined item position")
    
    rss = get_object_or_404(Rss, id=rss_id)
    item_number = int(item_number)

    if item_number < 0 or item_number > rss.items_set.all().count():
        raise Http404("Invalid item position: " + item_number)

    item = rss.items_set.all()[item_number:item_number+1].get()
    itemSummary = {
        'number': item_number,
        'title': item.title,
        'pub_date': formats.date_format(item.pub_date, "DATETIME_FORMAT"),
        'summary': item.summary,
        'totalLinks': item.links_set.all().count(),
    }
    
    if item.links_set.all().count() > 0:
        itemPicPosition = random.random() * item.links_set.all().count()
        itemSummary['pic'] = reverse('rss:localstoreretrieve', args=[rss.id, item.id, item.links_set.all()[itemPicPosition:itemPicPosition+1].get().id])
        itemSummary['gallery'] = reverse('rss:itemgallery', args=[rss.id, item.id])
    else:
        itemSummary['pic'] = static('noLinks.png')
    
    return HttpResponse(json.dumps(itemSummary), content_type="application/json")
