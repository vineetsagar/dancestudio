from django.contrib import admin
from rango.models import Members, EventCategory, EventType

# Register your models here.

admin.site.register(Members)
admin.site.register(EventCategory)
admin.site.register(EventType)