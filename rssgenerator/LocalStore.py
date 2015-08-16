"""LocalStore - Local store manager."""

__name__ = "LocalStore"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from django.conf import settings

import os
import magic
import urllib

class LocalStore:
    def __init__(self,
                 rssId):
        self.storePath = os.path.join(settings.RSSGENERATOR_LOCAL_DATA, str(rssId))
        
    def __getLinkFilePath(self, itemId, link):
        return os.path.join(self.storePath, str(itemId), str(link.id))

    def get(self, itemId, link):
        if not link.storeLocaly:
            return link.link
             
        linkFilePath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkFilePath):
            return link.link
        
        with open(linkFilePath, "rb") as f:
            return f.read()

    def contentType(self, itemId, link):
        linkFilePath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkFilePath):
            return
        
        mime = magic.Magic(mime=True)
        return mime.from_file(linkFilePath)
        
    def delete(self, itemId, link): 
        linkFilePath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkFilePath):
            return
                
        os.remove(linkFilePath)
            
    def store(self, itemId, link):
        if not os.path.exists(os.path.join(self.storePath, str(itemId))):
            os.makedirs(os.path.join(self.storePath, str(itemId)))
            
        linkDownloader = urllib.URLopener()
        linkDownloader.retrieve(link.link, self.__getLinkFilePath(itemId, link))
