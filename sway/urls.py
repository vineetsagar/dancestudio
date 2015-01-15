from django.conf.urls import patterns, url
from django.contrib import admin

from sway import views


admin.autodiscover()


urlpatterns=patterns('',
		 url(r'^$', views.index, name='index'),
		 url(r'^events/$', views.viewevents, name='events'),
		 url(r'^updateevents/$', views.updateEvent, name='updateevents'),
		 url(r'^events/editevents/(?P<id>\d+)/$', views.editevents, name='eventevents'),
		 url(r'^events/delete/(?P<id>\d+)/$', views.delete_events, name='delete_events'),
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
         url(r'^search_enquiry/$', views.search_enquiry, name='search_enquiry'),
         url(r'^search_instructor/$', views.search_instructor, name='search_instructor'),
         url(r'^search_events/$', views.search_events, name='search_events'),
         url(r'^search_member/$', views.search_member, name='search_member'),
         url(r'^saveeventsubscribe/$', views.save_eventmembers, name='saveeventsubscribe'),
         url(r'^members/new/$', views.member_edit, name='member_add'),
         url(r'^members/edit/(?P<id>\d+)/$', views.member_edit, name='member_edit'),
         url(r'^members/delete/(?P<id>\d+)/$', views.member_delete, name='member_delete',),
         url(r'^instructors/new/$', views.instructor_edit, name='instructor_add'),
         url(r'^instructors/edit/(?P<id>\d+)/$', views.instructor_edit, name='instructor_edit'),
         url(r'^instructors/delete/(?P<id>\d+)/$', views.instructor_delete, name='instructor_delete'),
         url(r'^events/eventsubscribe/(?P<id>\d+)/$', views.view_eventmembers, name='event_members'),

		)
