"""RssToStream - Rss stream generator."""

__name__ = "RssToStream"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

import datetime
import PyRSS2Gen as RSS2

from django.template import Context, loader
from rssgenerator.models import Rss
from rssgenerator.SidManager import SidManager

class RssToStream:
    def __init__(self,
                 request,
                 rss):
        self.rootUri = request.build_absolute_uri("/")[:-1]
        self.rssUri = request.build_absolute_uri()
        self.rss = rss
        
    def __toStream(self):
        sid = None
        if self.rss.private:
            sid = SidManager().create()
            
        items = self.__getRssItems(sid, self.rss.items_set.all())
        rssStream = RSS2.RSS2(
                        title = self.rss.title,
                        link = self.rssUri,
                        description = self.rss.description,
                        lastBuildDate = datetime.datetime.now(),
                        items = items)

        return rssStream
        
    def __getRssItems(self, sid, items):
        formatedItems = []
        for item in items:
            template = loader.get_template('rssgenerator/rssItemBody.html')
            context = {
                'sid': sid,
                'rootUri': self.rootUri,
                'description': item.summary,
                'links': item.links_set.all()
            }
            
            formatedItems.append(
                RSS2.RSSItem(
                    title = item.title,
                    description = template.render(context),
                    guid = RSS2.Guid(str(item.id)),
                    pubDate = item.pub_date)
                )

        return formatedItems

    def display(self):
        return self.__toStream().to_xml(encoding = "utf-8")
