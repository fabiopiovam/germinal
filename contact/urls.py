from django.conf.urls import patterns, include, url

urlpatterns = patterns('contact.views',
    url(r'^$', 'contact', name='pages'),
)