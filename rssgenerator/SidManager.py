"""SidManager - SID manager."""

__name__ = "SidManager"
__version__ = (1, 1, 0)
__author__ = "Anthony Prades <toony.github@chezouam.net>"

_generator_name = __name__ + "-" + ".".join(map(str, __version__))

import uuid

from django.utils import timezone
import pytz

from datetime import timedelta

from django.db import models
from django.db.models import Q
from rssgenerator.models import Sid
from django.core.exceptions import ObjectDoesNotExist

class SidManager:
    # SID lifetime in hours
    sidLifetime = 2
    
    def create(self):
        self.purge()
        
        sid = Sid()
        sid.sid = uuid.uuid4()
        sid.save()

        return sid.sid

    def delete(self, sid):
        try:
            Sid.objects.get(sid=sid).delete()
        except ObjectDoesNotExist:
            pass

    def purge(self):
        for sid in Sid.objects.filter(created__lt=timezone.now() - timedelta(hours=self.sidLifetime)):
            self.delete(sid.sid)

    def isValid(self, sid):
        if sid is None:
            return False
        
        sids = Sid.objects.filter(Q(created__gt=timezone.now() - timedelta(hours=self.sidLifetime)) & Q(sid=sid))
        if len(sids) == 1:
            return True

        return False
