from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
    
class Members(models.Model):
        first_name = models.CharField(max_length=128)
        last_name = models.CharField(max_length=128)
        email = models.EmailField()
        area = models.TextField()
        def __unicode__(self):
            return self.pk

class EventType(models.Model):
        name = models.CharField(max_length = 128)
        def __unicode__(self):
            return self.pk
        
class EventCategory(models.Model):
        event_category_name = models.CharField(max_length = 128)
        def __unicode__(self):
            return self.pk
    
class Events(models.Model):
        event_name = models.CharField(max_length=128)
        start_date = models.DateField()
        end_date = models.DateField()
        event_category_id = models.ForeignKey(EventCategory)
        event_type_id = models.ForeignKey(EventType)
        def __unicode__(self):
            return self.pk
        
class Instructors(models.Model):
    first_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)  
    email = models.CharField(max_length = 128)
    contact_number = models.CharField(max_length = 128)
    def __unicode__(self):
            return self.pk

class EventOccurence(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_id = models.ForeignKey(Events)
    meta_info = models.CharField(max_length=200)
    def __unicode__(self):
            return self.pk
    
class EventsInstructors(models.Model):
    event_id = models.ForeignKey(Events)
    instrcutors_id = models.ForeignKey(Instructors)
    def __unicode__(self):
            return self.pk
    
    
        
        
        