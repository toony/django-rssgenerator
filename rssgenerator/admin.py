from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import  mark_safe

from rssgenerator.models import Rss, Items, Links
from rssgenerator.forms import ItemsAdminForm
from rssgenerator.tools import images

from rssgenerator.LocalStore import LocalStore

class LinksInline(admin.TabularInline):
    model = Links
    extra = 1
    fields = ('Preview', 'link', 'storeLocaly')
    readonly_fields = ('Preview',)
    
    def Preview(self, link):
        if link.id is None:
            return "-"
        
        return mark_safe(u'<a href="%s" target="_blank" title="%s"><img src="%s?thumb=true" height="40"/></a>' %
            (
            reverse('rss:localstoreretrieve', args=[link.item.rss.id, link.item.id, link.id]),
            str(link.id),
            reverse('rss:localstoreretrieve', args=[link.item.rss.id, link.item.id, link.id])
            ))

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    inlines = [LinksInline]
    search_fields =  ['title', 'summary']
    list_display = ('title', 'summary', 'rss', 'linksCount', 'pub_date')
    list_per_page = 50
    save_on_top = True
    form = ItemsAdminForm
    list_filter = ('rss',)
    show_full_result_count = True

    def save_model(self, request, item, form, change):
        item.save()

        for afile in request.FILES.getlist('localFiles'):
            infos = images.getHeightWidth(afile.temporary_file_path())
            link = Links.objects.create(item_id=item.id, fromUploadedFile=True, height=infos['h'], width=infos['w'])
            
            LocalStore(item.rss.id).storeFromPath(item.id, link, afile.temporary_file_path())
    
@admin.register(Rss)
class RssAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
