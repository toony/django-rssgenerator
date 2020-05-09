from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    path('rssgenerator/', include(('rssgenerator.urls', 'app_name'), namespace='rss')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='rss:index', permanent=False), name='redirect'),
]
