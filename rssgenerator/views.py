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

def getRssgallery(rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    localStore = LocalStore.LocalStore(rss_id)

    rssGalleryIndex = []
    for item in rss.items_set.all():
        for link in item.links_set.all():
            linkInfos = { 'src': reverse('rss:localstoreretrieve', args=[rss.id, item.id, link.id]) }
            linkInfos.update(localStore.info(item.id, link))
            rssGalleryIndex.append(linkInfos)
            
    return rssGalleryIndex

def rssgallery(request, rss_id):
    rssGalleryIndex = getRssgallery(rss_id)

    return HttpResponse(json.dumps(rssGalleryIndex), content_type="application/json")

def rssgalleryrandom(request, rss_id):
    rssGalleryIndex = getRssgallery(rss_id)
    random.shuffle(rssGalleryIndex)
    
    return HttpResponse(json.dumps(rssGalleryIndex), content_type="application/json")

def allitemsid(request, rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    
    ids = []
    for itemId in rss.items_set.values("id").order_by("id"):
        ids.append(itemId["id"])
        
    return HttpResponse(json.dumps(ids), content_type="application/json")

def itemsummary(request, rss_id, item_id):        
    rss = get_object_or_404(Rss, id=rss_id)
    item = get_object_or_404(Items, id=item_id)

    itemSummary = {
        'id': item.id,
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
