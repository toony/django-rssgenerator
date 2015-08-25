import json
import RssToStream
import LocalStore

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

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

def getItem(request, rss_id, itemPosition):
    print rss.items_set.all()[5:6].get().pub_date
