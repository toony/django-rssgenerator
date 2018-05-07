# -*- coding: utf-8 -*-
"""LocalStore - Local store manager."""

__name__ = "LocalStore"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from django.conf import settings
from rssgenerator.models import Links
from rssgenerator.tools import images

from rssgenerator.tasks import storeLink

import os
import magic

class LocalStore:
    def __init__(self,
                 rssId):
        self.storePath = os.path.join(settings.RSSGENERATOR_LOCAL_DATA, str(rssId))
        
    def __getItemPath(self, itemId):
        return os.path.join(self.storePath, str(itemId))
        
    def __getLinkFilePath(self, itemId, link):
        return os.path.join(self.__getItemPath(itemId), str(link.id))

    def __getLinkThumbPath(self, itemId, link):
        linkFilePath = self.__getLinkFilePath(itemId, link)
        return linkFilePath + '.thumb'

    def get(self, itemId, link, thumb=False):
        if not link.storeLocaly:
            return {'content': link.link}

        if thumb:
            linkPath = self.__getLinkThumbPath(itemId, link)
            if not os.path.exists(linkPath):
                # fdf
                print "popop"
            else:
                with open(linkFilePath, "rb") as f:
                    return {'content': f.read(),
                            'type': magic.Magic(mime=True).from_file(linkPath)
                            }

        linkPath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkPath):
            return {'content': link.link}

        with open(linkPath, "rb") as f:
            return {'content': f.read(),
                    'type': magic.Magic(mime=True).from_file(linkPath)
                    }

    def __removeItemPath(self, itemId):
        itemPath = self.__getItemPath(itemId)

        try:
            os.rmdir(itemPath)
        except OSError:
            pass

    def delete(self, itemId, link): 
        linkFilePath = self.__getLinkFilePath(itemId, link)
        if os.path.exists(linkFilePath):
            os.remove(linkFilePath)

        linkFileThumb = self.__getLinkThumbPath(itemId, link)
        if os.path.exists(linkFileThumb):
            os.remove(linkFileThumb)

        self.__removeItemPath(itemId)

    def store(self, itemId, link):
        itemPath = self.__getItemPath(itemId)
        if not os.path.exists(itemPath):
            os.makedirs(itemPath)

        linkFilePath = self.__getLinkFilePath(itemId, link)
        linkFileThumb = self.__getLinkThumbPath(itemId, link)
        storeLink(link.id, link.link, linkFilePath, linkFileThumb)

    def setHeightWidth(self, itemId, link):
        if not link.storeLocaly:
            return {}
             
        linkFilePath = self.__getLinkFilePath(itemId, link)
        return images.getHeightWidth(linkFilePath)

    def isPresentLocaly(self, itemId, link):
        if not link.storeLocaly:
            return False;

        linkFilePath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkFilePath):
            return False

        return True
