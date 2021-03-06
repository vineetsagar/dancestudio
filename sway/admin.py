from django.contrib import admin
from sway.models import Members, EventCategory, EventType, Events, \
    EventOccurence, LeadFollowUp, Studio, StudioUser,GlobalCategories


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

class LeadFollowUpInline(admin.StackedInline): 
	model = LeadFollowUp 
	extra = 1
	
class LeadAdmin(admin.ModelAdmin):
	search_fields = ['name','mobile','email']
	inlines = [LeadFollowUpInline]

class LeadFollowUpAdmin(admin.ModelAdmin):
	pass	


						
# Register your models here.
admin.site.register(Members,MembersAdmin)
admin.site.register(EventCategory,EventCategoryAdmin)
admin.site.register(EventType,EventTypeAdmin)
admin.site.register(Events,EventsAdmin)
admin.site.register(EventOccurence,EventOccurenceAdmin)
admin.site.register(Studio)
admin.site.register(StudioUser)
admin.site.register(GlobalCategories)




