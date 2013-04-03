from django.contrib import admin
from rssgenerator.models import Rss, Items, Links

class LinksInline(admin.TabularInline):
    model = Links
    extra = 1

class ItemsAdmin(admin.ModelAdmin):
    inlines = [LinksInline]
    
class RssAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(Rss, RssAdmin)
admin.site.register(Items, ItemsAdmin)
