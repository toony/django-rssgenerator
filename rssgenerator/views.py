import json
import RssToStream
import LocalStore
import random

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import formats
from django.templatetags.static import static
from django.db.models import Q

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
        itemGalleryIndex.append(getLinkInfo(rss_id, item.id, link))
    
    return HttpResponse(json.dumps(itemGalleryIndex), content_type="application/json")

def getRssgallery(rss_id, itemsIdList):
    rss = get_object_or_404(Rss, id=rss_id)
    localStore = LocalStore.LocalStore(rss_id)

    rssGalleryIndex = []
    for item in rss.items_set.filter(id__in = itemsIdList):
        for link in item.links_set.all():
            rssGalleryIndex.append(getLinkInfo(rss.id, item.id, link))
            
    return rssGalleryIndex

def getLinkInfo(rssId, itemId, link):
    linkInfos = { 'src': reverse('rss:localstoreretrieve', args=[rssId, itemId, link.id]),
                  'h': link.height,
                  'w': link.width
                }

    return linkInfos

def rssgallery(request, rss_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST method must be used', content_type="text/plain")

    if 'itemsIdList[]' not in request.POST:
        return HttpResponseBadRequest('missing mandatory parameter \'itemsIdList[]\'', content_type="text/plain")

    rssGalleryIndex = getRssgallery(rss_id, request.POST.getlist('itemsIdList[]'))

    if 'random' in request.POST \
        and request.POST['random'] == 'true':
        random.shuffle(rssGalleryIndex)

    return HttpResponse(json.dumps(rssGalleryIndex), content_type="application/json")

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

def searchItem(request, rss_id):
    query = request.GET.get('q')
    rss = get_object_or_404(Rss, id=rss_id)

    ids = []
    for item in rss.items_set.filter(Q(title__icontains=query) | Q(summary__icontains=query)).values("id").order_by("-pub_date"):
        ids.append(item["id"])

    return HttpResponse(json.dumps(ids), content_type="application/json")
