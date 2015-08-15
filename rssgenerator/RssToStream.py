"""RssToStream - Rss stream generator."""

__name__ = "RssToStream"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

import datetime
import PyRSS2Gen as RSS2

from django.template import Context, loader
from rssgenerator.models import Rss

class RssToStream:
    def __init__(self,
                 request,
                 rss):
        self.rootUri = self.__getRootUri(request)
        self.rssUri = self.rootUri + "/" + request.build_absolute_uri()
        self.rss = rss
        
    def __toStream(self):
        items = self.__getRssItems(self.rss.items_set.all())
        rssStream = RSS2.RSS2(
                        title = self.rss.title,
                        link = self.rssUri,
                        description = self.rss.description,
                        lastBuildDate = datetime.datetime.now(),
                        items = items)
        return rssStream
        
    def __getRssItems(self, items):
        formatedItems = []
        for item in items:
            template = loader.get_template('rssgenerator/rssItemBody.html')
            context = Context({
				'rootUri' : self.rootUri,
                'description': item.summary,
                'links': item.links_set.all()
            })
            
            formatedItems.append(
                RSS2.RSSItem(
                    title = item.title,
                    link = item.link,
                    description = template.render(context),
                    guid = RSS2.Guid(item.link),
                    pubDate = item.pub_date)
                )

        return formatedItems

    def display(self):
        return self.__toStream().to_xml(encoding = "utf-8")

    def __getRootUri(self, request):
        if  'HTTP_X_SCHEME' in request.META and 'HTTP_X_HOST' in request.META:
            return request.META['HTTP_X_SCHEME'] + "://" + request.META['HTTP_X_HOST']
            
        return request.build_absolute_uri("/")[:-1]
