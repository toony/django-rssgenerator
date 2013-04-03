import RssToStream

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rssgenerator.models import Rss

def rssstream(request, rss_id):
	rssToStream = RssToStream.RssToStream(get_object_or_404(Rss, id=rss_id), request.build_absolute_uri())
	return HttpResponse(rssToStream.display())
