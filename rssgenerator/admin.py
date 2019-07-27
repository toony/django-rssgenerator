from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import  mark_safe

from rssgenerator.models import Rss, Items, Links
from rssgenerator.forms import ItemsAdminForm
from rssgenerator.tools import images

import LocalStore

class LinksInline(admin.TabularInline):
    model = Links
    extra = 1
    fields = ('Preview', 'link', 'storeLocaly')
    readonly_fields = ('Preview',)
    
    def Preview(self, link):
        if link.id is None:
            return "-"
        
        return mark_safe(u'<a href="'
            + reverse('rss:localstoreretrieve', args=[link.item.rss.id, link.item.id, link.id])
            + '" target="_blank" title="'
            + str(link.id)
            + '">'
            + '<img src="'
            + reverse('rss:localstoreretrieve', args=[link.item.rss.id, link.item.id, link.id])
            + '?thumb=true" height="40"/>'
            + '</a>')

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    inlines = [LinksInline]
    search_fields =  ['title', 'summary']
    list_display = ('title', 'summary', 'linksCount', 'pub_date')
    list_per_page = 50
    save_on_top = True
    form = ItemsAdminForm

    def save_model(self, request, item, form, change):
        print("save_model")
        item.save()

        for afile in request.FILES.getlist('localFiles'):
            print(afile.temporary_file_path())
            print(item.id)
            infos = images.getHeightWidth(afile.temporary_file_path())
            link = Links.objects.create(item_id=item.id, fromUploadedFile=True, height=infos['h'], width=infos['w'])
            
            print(link.id)
            LocalStore.LocalStore(item.rss.id).storeFromPath(item.id, link, afile.temporary_file_path())
    
@admin.register(Rss)
class RssAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
