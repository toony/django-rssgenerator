from django.contrib import admin
from rssgenerator.models import Rss, Items, Links

class LinksInline(admin.TabularInline):
    model = Links
    extra = 1

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    inlines = [LinksInline]
    search_fields =  ['title', 'summary']
    list_display = ('pub_date', 'title', 'summary')
    list_per_page = 50
    
@admin.register(Rss)
class RssAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
