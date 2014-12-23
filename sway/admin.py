from django.contrib import admin

from sway.models import Members, EventCategory, EventType, Events, \
    EventOccurence


# Register your models here.
admin.site.register(Members)
admin.site.register(EventCategory)
admin.site.register(EventType)
admin.site.register(Events)
admin.site.register(EventOccurence)