from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^rssgenerator/', include('rssgenerator.urls', namespace="rss")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(pattern_name='rss:index', permanent=False), name='redirect'),
]
