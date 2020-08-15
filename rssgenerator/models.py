from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

class Rss(models.Model):
    title = models.CharField(max_length=256, null=False)
    description = models.CharField(max_length=256, null=False)
    private = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Items(models.Model):
    rss = models.ForeignKey(Rss, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    link = models.URLField(max_length=1024, null=True, blank=True)
    pub_date = models.DateTimeField('date published', null=False)
    summary = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ["-pub_date"]
        
    def __str__(self):
        return self.title
        
    def linksCount(self):
        return self.links_set.all().count()
    
class Links(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    link = models.URLField(max_length=1024, null=True, blank=True)
    height = models.IntegerField(null=True, editable=False)
    width = models.IntegerField(null=True, editable=False)
    storeLocaly = models.BooleanField(default=True)
    fromUploadedFile = models.BooleanField(default=False, editable=False)
    
    def clean(self):
        if self.fromUploadedFile is True:
            self.storeLocaly = True
            self.link = None
            
    def __str__(self):
        return F"({self.id}) {self.width}*{self.height}"

class Sid(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sid = models.CharField(max_length=256, null=False, unique=True)
    
    def __str__(self):
        return F"{self.created} {self.sid}"

from rssgenerator.LocalStore import LocalStore

@receiver(pre_save, sender=Items)
def __updateItemRss(sender, instance, **kwargs):
    item = instance

    try:
        oldItem = Items.objects.get(pk=item.id)
        LocalStore(item.rss.id).storeFromLocalStore(LocalStore(oldItem.rss.id), item.id)
    except Items.DoesNotExist:
        pass

@receiver(post_save, sender=Links)
def __storeLink(sender, instance, **kwargs):
    link = instance

    item = link.item
    if not link.storeLocaly:
        LocalStore(item.rss.id).delete(item.id, link)
        return

    LocalStore(item.rss.id).storeFromLink(item.id, link)
    
@receiver(post_delete, sender=Links)
def __deleteLink(sender, instance, **kwargs):
    link = instance
    item = link.item
    LocalStore(item.rss.id).delete(item.id, link)
