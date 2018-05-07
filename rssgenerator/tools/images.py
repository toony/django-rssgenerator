# -*- coding: utf-8 -*-
"""RssToStream - Rss stream generator."""
from __future__ import division

__name__ = "RssToStream"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

from PIL import Image

import os

def getHeightWidth(linkFilePath):
    if not os.path.exists(linkFilePath):
        return {}
    
    infos = {}
    im = Image.open(linkFilePath)
    (infos['w'], infos['h']) = im.size

    return infos

def createThumb(linkFilePath, linkFileThumb):
    if not os.path.exists(linkFilePath):
        return

    im = Image.open(linkFilePath)
    thumbHeight = 250
    thumbWidth = int(im.width/(im.height/thumbHeight))
    
    im.thumbnail((thumbWidth, thumbHeight))
    if im.mode == 'RGBA':
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3]) # 3 is the alpha channel
        im.close()
        im = background

    try:
        im = im.convert("RGB")
        im.save(linkFileThumb, format='JPEG', quality=80)
    except IOError as ioerror:
        if os.path.exists(linkFileThumb):
            os.remove(linkFileThumb)

        raise ioerror
