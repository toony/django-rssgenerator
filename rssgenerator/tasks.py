# -*- coding: utf-8 -*-
"""RssToStream - Rss stream generator."""

__name__ = "RssGeneratorAsyncTasks"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from background_task import background
from rssgenerator.models import Links
from rssgenerator.tools import images

import datetime
import urllib2, ssl

@background(schedule=datetime.datetime.now())
def storeLink(linkId, linkUrl, linkFilePath, linkFileThumb):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib2.urlopen(urllib2.Request(linkUrl,
        None,
        {'User-agent':
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
        }), context=ctx).read()
        
    dstFile = open(linkFilePath, 'w')
    dstFile.write(response)
    dstFile.close()
    
    infos = images.getHeightWidth(linkFilePath)
    Links.objects.filter(id = linkId) \
                 .update(height = infos['h'],
                         width = infos['w'])

    images.createThumb(linkFilePath, linkFileThumb)

@background(schedule=datetime.datetime.now())
def createLinkThumbnail(linkFilePath, linkFileThumb):
    images.createThumb(linkFilePath, linkFileThumb)
