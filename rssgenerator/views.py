import json
import random, base64

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import formats
from django.templatetags.static import static
from django.db.models import Q
from django.contrib.auth import authenticate

from rssgenerator.LocalStore import LocalStore, ItemNotFound
from rssgenerator.RssToStream import RssToStream

from rssgenerator.models import Rss, Items, Links

def isAuthenticated(request, rss):
    # If private page do basic auth
    if rss.private:
        if request.user.is_authenticated:
            return True;

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1].encode('utf-8')).decode('utf-8').split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        request.user = user
                        return True

        return False
    else:
        return True
        
def needAuthentication(rss):
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="Rss %s need authentication"' % rss.title
    response.content = '<html><script>window.location.href = "/";</script></html>'
    return response

def rssStream(request, rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)
    
    rssToStream = RssToStream(request, rss)
    return HttpResponse(rssToStream.display())

def rssSummary(request, rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)

    return render(request, 'rssgenerator/rssSummary.html', {"rss": rss})

def localStoreRetrieve(request, rss_id, item_id, link_id):
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)
    
    thumb = False
    if request.GET.get('thumb', False) in ['true', 'True']:
        thumb = True

    link = get_object_or_404(Links, id=link_id)
    localStore = LocalStore(rss_id)
    
    try:
        linkContent = localStore.get(item_id, link, thumb)
    except ItemNotFound:
        return HttpResponseNotFound("Link id "
            + str(link.id)
            + " from item "
            + str(item_id)
            + ", rss "
            + str(rss_id)
            + " doesn't exists")

    return HttpResponse(linkContent['content'], linkContent['type'])

def itemGallery(request, rss_id, item_id):
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)
    
    item = get_object_or_404(Items, id=item_id)
    localStore = LocalStore(rss_id)
    
    itemGalleryIndex = []
    for link in item.links_set.all():
        itemGalleryIndex.append(getLinkInfo(rss_id, item.id, link))
    
    return HttpResponse(json.dumps(itemGalleryIndex), content_type="application/json")

def getRssGallery(rss_id, itemsIdList):
    rss = get_object_or_404(Rss, id=rss_id)
    localStore = LocalStore(rss_id)

    rssGalleryIndex = []
    for item in rss.items_set.filter(id__in = itemsIdList):
        for link in item.links_set.all():
            rssGalleryIndex.append(getLinkInfo(rss.id, item.id, link))
            
    return rssGalleryIndex

def getLinkInfo(rssId, itemId, link):
    if not link.storeLocaly \
       or not LocalStore(rssId).isPresentLocaly(itemId, link):
        linkInfos = { 'src': link.link,
                      'h': 200,
                      'w': 200
                    }
    else:
        linkInfos = { 'src': reverse('rss:localStoreRetrieve', args=[rssId, itemId, link.id]),
                      'h': link.height,
                      'w': link.width
                    }

    return linkInfos

def rssGallery(request, rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)
    
    if request.method != 'POST':
        return HttpResponseBadRequest('POST method must be used', content_type="text/plain")

    if 'itemsIdList[]' not in request.POST:
        return HttpResponseBadRequest('missing mandatory parameter \'itemsIdList[]\'', content_type="text/plain")

    rssGalleryIndex = getRssGallery(rss_id, request.POST.getlist('itemsIdList[]'))

    if 'random' in request.POST \
        and request.POST['random'] == 'true':
        random.shuffle(rssGalleryIndex)

    return HttpResponse(json.dumps(rssGalleryIndex), content_type="application/json")

def itemSummary(request, rss_id, item_id):        
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)
    
    item = get_object_or_404(Items, id=item_id)

    itemSummary = {
        'id': item.id,
        'title': item.title,
        'pub_date': formats.date_format(item.pub_date, "DATETIME_FORMAT"),
        'summary': item.summary,
        'totalLinks': item.linksCount(),
    }
    
    if item.links_set.all().count() > 0:
        itemPicPosition = random.random() * item.links_set.all().count()
        link = item.links_set.all()[itemPicPosition:itemPicPosition+1].get()
        
        if not link.storeLocaly \
           or not LocalStore(rss_id).isPresentLocaly(item.id, link):
            itemSummary['pic'] = link.link
        else:
            itemSummary['pic'] = reverse('rss:localStoreRetrieve',
                                         args=[rss.id, item.id, item.links_set.all()[itemPicPosition:itemPicPosition+1].get().id]) \
                                 + "?thumb=True"

        itemSummary['gallery'] = reverse('rss:itemGallery', args=[rss.id, item.id])
    else:
        itemSummary['pic'] = static('noLinks.png')
    
    return HttpResponse(json.dumps(itemSummary), content_type="application/json")

def searchItem(request, rss_id):
    rss = get_object_or_404(Rss, id=rss_id)
    if not isAuthenticated(request, rss):
        return needAuthentication(rss)
        
    query = request.GET.get('q')
    rss = get_object_or_404(Rss, id=rss_id)

    ids = []
    for item in rss.items_set.filter(Q(title__icontains=query) | Q(summary__icontains=query)).values("id").order_by("-pub_date"):
        ids.append(item["id"])

    return HttpResponse(json.dumps(ids), content_type="application/json")
