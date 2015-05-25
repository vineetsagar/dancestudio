from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from sway import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = patterns('',
                url(r'^$', views.index, name='index'),
    			url(r'^admin/', include(admin.site.urls)),
				url(r'^sway/', include('sway.urls')),
				 url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
		      )
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )