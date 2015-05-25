from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from sway import views

urlpatterns = patterns('',
                url(r'^$', views.index, name='index'),
    			url(r'^admin/', include(admin.site.urls)),
				url(r'^sway/', include('sway.urls')),
		      )
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )