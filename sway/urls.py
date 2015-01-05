from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from sway import views


urlpatterns=patterns('',
		 url(r'^$', views.index, name='index'),
		 url(r'^events/$', views.viewevents, name='events'),
		 url(r'^addevents/$', views.addevents, name='add_events'),
		 url(r'^saveevents/$', views.saveevents, name='saveevents'),
		 url(r'^members/$', views.viewmembers, name='members'),
		 url(r'^addmembers/$', views.addmembers, name='add_members'),
	 	    url(r'^logout/$', 'django.contrib.auth.views.logout' , {'next_page': '/sway/'}),
		 url(r'^savemembers/$', views.savemembers, name='savemembers'),
		 url(r'^instructors/$', views.show_instructors, name='instructors'),
		 url(r'^add_instructor/$', views.add_instructor, name='add_instructor'),
		 url(r'^save_instructor/$', views.save_instructor, name='save_instructor'),
		 url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
		 url(r'^events_json/$', views.get_events_json, name='get_event_json'),
		 url(r'^loginAuth/$', views.loginAuth, name='loginAuth'),
		 url(r'^enquiries/$', views.view_enquiries, name='enquiries'),
       url(r'^enquire/$', views.add_lead, name='addLead'),
		 url(r'^followups/$', views.view_followups, name='followups'),
       url(r'^save_enquiry/$', views.save_enquiry, name='save_enquiry'),
       url(r'^followup/$', views.followup, name='followup'),
       url(r'^save_followup/$', views.save_followup, name='save_followup'),
		)
