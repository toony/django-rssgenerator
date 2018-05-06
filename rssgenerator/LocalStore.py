# -*- coding: utf-8 -*-
"""LocalStore - Local store manager."""

__name__ = "LocalStore"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from django.conf import settings
from rssgenerator.models import Links

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

        infos = self.getHeightWidth(itemId, link)
        Links.objects.filter(id = link.id) \
                     .update(height = infos['h'],
                             width = infos['w'])


    def getHeightWidth(self, itemId, link):
        if not link.storeLocaly:
            return {}
             
        linkFilePath = self.__getLinkFilePath(itemId, link)
        if not os.path.exists(linkFilePath):
            return {}
        
        infos = {}
        (infos['w'], infos['h']) = get_image_size(linkFilePath)
        return infos
        

#-------------------------------------------------------------------------------
# Name:        get_image_size
# Purpose:     extract image dimensions given a file path using just
#              core modules
#
# Author:      Paulo Scardine (based on code from Emmanuel VAÏSSE)
#
# Created:     26/09/2013
# Copyright:   (c) Paulo Scardine 2013
# Licence:     MIT
#-------------------------------------------------------------------------------
class UnknownImageFormat(Exception):
    pass

def get_image_size(file_path):
    """
    Return (width, height) for a given img file content - no external
    dependencies except the os and struct modules from core
    """
    size = os.path.getsize(file_path)

    with open(file_path) as input:
        height = -1
        width = -1
        data = input.read(25)

        if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
            # GIFs
            w, h = struct.unpack("<HH", data[6:10])
            width = int(w)
            height = int(h)
        elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
              and (data[12:16] == 'IHDR')):
            # PNGs
            w, h = struct.unpack(">LL", data[16:24])
            width = int(w)
            height = int(h)
        elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
            # older PNGs?
            w, h = struct.unpack(">LL", data[8:16])
            width = int(w)
            height = int(h)
        elif (size >= 2) and data.startswith('\377\330'):
            # JPEG
            msg = " raised while trying to decode as JPEG."
            input.seek(0)
            input.read(2)
            b = input.read(1)
            try:
                while (b and ord(b) != 0xDA):
                    while (ord(b) != 0xFF): b = input.read(1)
                    while (ord(b) == 0xFF): b = input.read(1)
                    if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                        input.read(3)
                        h, w = struct.unpack(">HH", input.read(4))
                        break
                    else:
                        input.read(int(struct.unpack(">H", input.read(2))[0])-2)
                    b = input.read(1)
                width = int(w)
                height = int(h)
            except struct.error:
                raise UnknownImageFormat("StructError" + msg)
            except ValueError:
                raise UnknownImageFormat("ValueError" + msg)
            except Exception as e:
                raise UnknownImageFormat(e.__class__.__name__ + msg)
        else:
            raise UnknownImageFormat(
                "Sorry, don't know how to get information from this file."
            )

    return width, height
