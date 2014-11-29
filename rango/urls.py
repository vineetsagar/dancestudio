from django.conf.urls import patterns, url

from rango import views


urlpatterns=patterns('',
		 url(r'^$', views.home, name='home'),
		 url(r'^members/$', views.index, name='index'),
		 url(r'^addmembers/$', views.addmembers, name='add_members'),
		 url(r'^login/$', 'django.contrib.auth.views.login'),
   		 url(r'^logout/$', 'django.contrib.auth.views.logout' , {'next_page': '/rango/'}),
   		 url(r'^savemembers/$', views.savemembers, name='savemembers'),
		)
