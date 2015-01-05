from django.conf.urls import patterns, url

from sway import views


urlpatterns=patterns('',
		 url(r'^$', views.index, name='index'),
		 url(r'^events/$', views.viewevents, name='events'),
		 url(r'^addevents/$', views.addevents, name='add_events'),
		 url(r'^events/editevents/$', views.editevents, name='edit_events'),
		 url(r'^saveevents/$', views.saveevents, name='saveevents'),
		 url(r'^updateevents/$', views.updateEvent, name='updateevents'),
		 url(r'^members/$', views.viewmembers, name='members'),
		 url(r'^addmembers/$', views.addmembers, name='add_members'),
		 url(r'^login/$', 'django.contrib.auth.views.login'),
   		 url(r'^logout/$', 'django.contrib.auth.views.logout' , {'next_page': '/sway/'}),
   		 url(r'^savemembers/$', views.savemembers, name='savemembers'),
   		 url(r'^instructors/$', views.show_instructors, name='instructors'),
   		 url(r'^add_instructor/$', views.add_instructor, name='add_instructor'),
   		 url(r'^save_instructor/$', views.save_instructor, name='save_instructor'),
   		 url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
   		 url(r'^events_json/$', views.get_events_json, name='get_event_json'),
   		 url(r'^loginAuth/$', views.loginAuth, name='loginAuth'),
		)
