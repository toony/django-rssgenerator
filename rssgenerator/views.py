import RssToStream
import LocalStore

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rssgenerator.models import Rss, Links

def rssstream(request, rss_id):
    rssToStream = RssToStream.RssToStream(request, get_object_or_404(Rss, id=rss_id))
    return HttpResponse(rssToStream.display())

def localstoreretrieve(request, rss_id, item_id, link_id):
    localStore = LocalStore.LocalStore(rss_id)
    
    link = get_object_or_404(Links, id=link_id)
    return HttpResponse(localStore.get(item_id, link), localStore.contentType(item_id, link))
