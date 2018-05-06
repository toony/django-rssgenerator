# -*- coding: utf-8 -*-
"""LocalStore - Local store manager."""

__name__ = "LocalStore"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from django.conf import settings
from rssgenerator.models import Links
from rssgenerator.tools import images

import os
import struct
import magic
import urllib2

class LocalStore:
    def __init__(self,
                 rssId):
        self.storePath = os.path.join(settings.RSSGENERATOR_LOCAL_DATA, str(rssId))
        
    def __getItemPath(self, itemId):
        return os.path.join(self.storePath, str(itemId))
        
    def __getLinkFilePath(self, itemId, link):
        return os.path.join(self.__getItemPath(itemId), str(link.id))

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
        
    def __removeItemPath(self, itemId):
        itemPath = self.__getItemPath(itemId)
        
        try:
            os.rmdir(itemPath)
        except OSError:
            pass
        
    def delete(self, itemId, link): 
        linkFilePath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkFilePath):
            self.__removeItemPath(itemId)
            return
                
        os.remove(linkFilePath)
        
        self.__removeItemPath(itemId)
            
    def store(self, itemId, link):
        itemPath = self.__getItemPath(itemId)
        if not os.path.exists(itemPath):
            os.makedirs(itemPath)

        response = urllib2.urlopen(urllib2.Request(link.link,
            None,
            {'User-agent':
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
            })).read()
            
        linkFilePath = self.__getLinkFilePath(itemId, link);
        
        dstFile = open(linkFilePath, 'w')
        dstFile.write(response)
        dstFile.close()

        infos = self.setHeightWidth(itemId, link)
        Links.objects.filter(id = link.id) \
                     .update(height = infos['h'],
                             width = infos['w'])

    def setHeightWidth(self, itemId, link):
        if not link.storeLocaly:
            return {}
             
        linkFilePath = self.__getLinkFilePath(itemId, link)
        return images.getHeightWidth(linkFilePath)
