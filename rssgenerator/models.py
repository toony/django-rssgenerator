from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import LocalStore


class Rss(models.Model):
    title = models.CharField(max_length=256, null=False)
    description = models.CharField(max_length=256, null=False)
    def __unicode__(self):
        return self.title
    
class Items(models.Model):
    rss = models.ForeignKey(Rss)
    title = models.CharField(max_length=256, null=False)
    link = models.URLField(max_length=1024, null=False)
    pub_date = models.DateTimeField('date published', null=False)
    summary = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ["-pub_date"]
        
    def __unicode__(self):
        return self.title
    
class Links(models.Model):
    item = models.ForeignKey(Items)
    link = models.URLField(max_length=1024, null=False)
    storeLocaly = models.BooleanField(default=True)

@receiver(post_save, sender=Links)
def __storeLink(sender, instance, **kwargs):
    link = instance
    item = link.item
    print "popop"
    if not link.storeLocaly:
		LocalStore.LocalStore(item.rss.id, item.id, link).delete()
		return
        
    LocalStore.LocalStore(item.rss.id, item.id, link).store()
    
@receiver(post_delete, sender=Links)
def __deleteLink(sender, instance, **kwargs):
    link = instance
    item = link.item
    LocalStore.LocalStore(item.rss.id, item.id, link).delete()
