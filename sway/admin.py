from django.contrib import admin

from sway.models import Members, EventCategory, EventType, Events, \
    EventOccurence

class MembersAdmin(admin.ModelAdmin):
	search_fields = ['first_name','last_name','email',]

class EventCategoryAdmin(admin.ModelAdmin):
	search_fields = ['event_category_name']

class EventTypeAdmin(admin.ModelAdmin):
	search_fields = ['event_type_name']

class EventsAdmin(admin.ModelAdmin):
	search_fields = ['event_name']

class EventOccurenceAdmin(admin.ModelAdmin):
	pass
					
# Register your models here.
admin.site.register(Members,MembersAdmin)
admin.site.register(EventCategory,EventCategoryAdmin)
admin.site.register(EventType,EventTypeAdmin)
admin.site.register(Events,EventsAdmin)
admin.site.register(EventOccurence,EventOccurenceAdmin)