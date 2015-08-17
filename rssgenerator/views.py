import json
import RssToStream
import LocalStore

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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
        linkInfos = { 'src': link.link }
        linkInfos.update(localStore.info(item.id, link))
        itemGalleryIndex.append(linkInfos)
    
    return HttpResponse(json.dumps(itemGalleryIndex), content_type="application/json")
