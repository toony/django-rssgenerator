"""LocalStore - Local store manager."""

__name__ = "LocalStore"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from django.conf import settings

import os
import magic
import urllib

class LocalStoreRetriever:
    def __init__(self,
                 rssId,
                 itemId,
                 link):
        self.rssId = rssId
        self.link = link
        
        self.linkFile = os.path.join(settings.RSSGENERATOR_LOCAL_DATA, str(rssId))
        self.storePath = os.path.join(self.linkFile, str(itemId))
        self.linkFile = os.path.join(self.storePath, str(link.id))

    def get(self):
        if not os.path.exists(self.linkFile):
            return self.link.link
        
        try:
            with open(self.linkFile, "rb") as f:
                return f.read()
        except IOError:
            red = Image.new('RGBA', (1, 1), (255,0,0,0))
            return self.link.link

    def mime(self):
        if not os.path.exists(self.linkFile):
            return
        
        mime = magic.Magic(mime=True)
        mime.from_file(self.linkFile)
        
    def delete(self):
        print "Deleting: "+self.linkFile
        if os.path.exists(self.linkFile):
            os.remove(self.linkFile)
            
    def store(self):
        if not os.path.exists(self.storePath):
            os.makedirs(self.storePath)
            
        linkDownloader = urllib.URLopener()
        linkDownloader.retrieve(self.link.link, self.linkFile)
