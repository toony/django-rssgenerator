from django.db import models

# Create your models here.

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
