from django.conf.urls import patterns, include, url

from surlex.dj import surl

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from newsletter_custom.views import UpdateSubscriptionViev

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^ckeditor/', include('ckeditor.urls')),
    
    #newsletter with customization
    surl('^newsletter/<newsletter_slug:s>/subscription/<email=[-_a-zA-Z0-9@\.\+~]+>/'
         '<action=subscribe|update|unsubscribe>/activate/<activation_code:s>/$',
         UpdateSubscriptionViev.as_view(), name='newsletter_update_activate'),
    (r'^newsletter/', include('newsletter.urls')),
    
    
    (r'^pages/', include('cms.urls')),
    (r'^tags/', include('tags.urls')),
    (r'^contact/', include('contact.urls')),
    
    url(r'^$', 'products.views.index', name='home'),
    url(r'^(?P<slug>[\w_-]+)$', 'products.views.details', name='product'),
    url(r'^products/(?P<slug>[\w_-]+)$', 'products.views.query_by_segment', name='segment'),
    url(r'^products/$', 'products.views.products_list', name='products'),
)

if settings.LOCAL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)