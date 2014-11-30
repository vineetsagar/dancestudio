from django.contrib import admin
from rango.models import Category, Page, Members, EventCategory, EventType

# Register your models here.

admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Members)
admin.site.register(EventCategory)
admin.site.register(EventType)