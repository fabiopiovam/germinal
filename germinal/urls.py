from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^ckeditor/', include('ckeditor.urls')),
    
    (r'^pages/', include('cms.urls')),
    (r'^tags/', include('tags.urls')),
    
    url(r'^$', 'products.views.index', name='home'),
    url(r'^(?P<slug>[\w_-]+)$', 'products.views.details', name='product'),
    url(r'^segment/(?P<slug>[\w_-]+)$', 'products.views.query_by_segment', name='segment'),
)

if settings.LOCAL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)