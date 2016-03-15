from django.conf.urls import patterns, url,include
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from sway import views
from sway.api import api_view
from sway.api import api_helper


admin.autodiscover()


urlpatterns=patterns('',

		url(r'^$', views.index, name='index'),
            url(r'^dancehub$', views.danceHub, name='hub'),
            url(r'^signup$', views.signup, name='signup'),
		url(r'^locations/search$', api_view.get_models_within_25, name='get_models_within_25'),
            url(r'^locations/$', views.view_locations, name='view_locations'),
            url(r'^gallery/$', views.profile_gallery, name='profile_gallery'),
		url(r'^locations/delete/(?P<id>\d+)/$', views.locaton_delete, name='locaton_delete',),
            url(r'^locations/new/$', views.add_edit_locations, name='location_add'),
		 url(r'^locations/edit/(?P<id>\d+)/$', views.add_edit_locations, name='location_edit'),
		 url(r'^categories/$', views.view_categories, name='view_categories'),
		 url(r'^categories/new/$', views.add_edit_categories, name='category_add'),
		 url(r'^categories/edit/(?P<id>\d+)/$', views.add_edit_categories, name='category_edit'),
		 url(r'^categories/delete/(?P<id>\d+)/$', views.category_delete, name='category_delete',),
		 url(r'^contact/$', views.save_contact, name='save_contact'),
		 url(r'^events/$', views.viewevents, name='events'),
		 url(r'^updateevents/$', views.updateEvent, name='updateevents'),
		 url(r'^events/editevents/(?P<id>\d+)/$', views.editevents, name='eventevents'),
		 url(r'^events/delete/(?P<id>\d+)/$', views.delete_events, name='delete_events'),
		 url(r'^addevents/$', views.addevents, name='add_events'),
		 url(r'^saveevents/$', views.saveevents, name='saveevents'),
		 url(r'^members/$', views.viewmembers, name='members'),
		 url(r'^addmembers/$', views.addmembers, name='add_members'),
	 	 url(r'^login/$', 'django.contrib.auth.views.login' , name='login'),
	 	 url(r'^logout/$', 'django.contrib.auth.views.logout' , {'next_page': '/sway/'}),
		 url(r'^savemembers/$', views.savemembers, name='savemembers'),
		 url(r'^instructors/$', views.show_instructors, name='instructors'),
		 url(r'^add_instructor/$', views.add_instructor, name='add_instructor'),
		 url(r'^save_instructor/$', views.save_instructor, name='save_instructor'),
		 url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
		 url(r'^settings/$', views.show_settings, name='show_settings'),
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
       url(r'^savecategories/$', views.save_studiocategories, name='savecategories'),
       url(r'^members/new/(?P<lead>\d+)/$', views.lead_to_member, name='lead_to_member'),
       url(r'^members/new/$', views.member_edit, name='member_add'),
       url(r'^members/edit/(?P<id>\d+)/$', views.member_edit, name='member_edit'),
       url(r'^members/delete/(?P<id>\d+)/$', views.member_delete, name='member_delete',),
       url(r'^instructors/new/$', views.instructor_edit, name='instructor_add'),
       url(r'^instructors/edit/(?P<id>\d+)/$', views.instructor_edit, name='instructor_edit'),
       url(r'^instructors/delete/(?P<id>\d+)/$', views.instructor_delete, name='instructor_delete'),
       url(r'^events/eventsubscribe/(?P<id>\d+)/$', views.view_eventmembers, name='event_members'),
       url(r'^lead/edit/(?P<id>\d+)/$', views.edit_lead, name='edit_lead'),
       url(r'^alerts/$', views.alerts, name='alerts'),
       url(r'^newmembers/$', views.new_members, name='new_members'),
       url(r'^newleads/$', views.new_leads, name='new_leads'),
       url(r'^newevents/$', views.new_events, name='new_events'),
       #url(r'^forgotpassword/$', views.forgotpassword, name='forgotpassword'),
       #url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
       url(r'^changepassword/$', views.change_password, name='changepassword'),
       url(r'^lead/convert/(?P<id>\d+)/$', views.convert_lead, name='convert_lead'),
       url(r'^api-token-auth/', obtain_auth_token),
       url(r'^loginApp/$', api_view.api_app_login, name='loginApp'),
       url(r'^validateToken/$', api_view.api_validate_token, name='validateToken'),
       url(r'^getleads/$', api_view.api_lead_list, name='getleads'),
       url(r'^getleadfollowups/$', api_view.api_single_lead, name='api_single_lead'),
       url(r'^getleadsCount/$', api_view.api_lead_count_view, name='getleadsCount'),
       url(r'^api_add_lead/$', api_view.api_add_lead, name='api_add_lead'),
       url(r'^api_add_followup/$', api_view.api_add_followup, name='api_add_followup'),
       url(r'^registration/$', api_view.registration, name='registration'),
       url(r'^user/password/reset/$','django.contrib.auth.views.password_reset',{'post_reset_redirect' : '/sway/user/password/reset/done/'},name="password_reset"),
       url(r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done'),
       url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$','django.contrib.auth.views.password_reset_confirm',{'post_reset_redirect' : '/sway/user/password/done/'},name="reset_confirm"),
       url(r'^user/password/done/$','django.contrib.auth.views.password_reset_complete'),
       url(r'^member/comments/(?P<Id>\d+)/$', views.member_comment, name='member_comment'),
       url(r'^member/comment/add/(?P<Id>\d+)/$', views.add_member_comment, name='add_member_comment'),
       url(r'^member/comment/save/$', views.save_member_comment, name='save_member_comment'),
       #url('^', include('django.contrib.auth.urls')),
       url('', include('social.apps.django_app.urls', namespace='social')),
       url('', include('django.contrib.auth.urls', namespace='auth')),
		)


