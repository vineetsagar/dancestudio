from datetime import datetime

from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Members(models.Model):
        first_name = models.CharField(max_length=128)
        last_name = models.CharField(max_length=128)
        email = models.EmailField()
        area = models.TextField()
        def __unicode__(self):
            return self.email

class EventType(models.Model):
        event_type_name = models.CharField(max_length = 128)
        def __unicode__(self):
            return self.event_type_name
        
class EventCategory(models.Model):
        event_category_name = models.CharField(max_length = 128)
        def __unicode__(self):
            return self.event_category_name
    
class Events(models.Model):
        event_name = models.CharField(max_length=128)
        all_day= models.BooleanField(default=False)
        event_category_id = models.ForeignKey(EventCategory)
        event_type_id = models.ForeignKey(EventType)
        
        start_date = models.DateField(default=datetime.now())
        end_date = models.DateField(default=datetime.now())
        
        start_time = models.TimeField(default='00:00')
        end_time = models.TimeField(default='00:00')
        
        def __unicode__(self):
            return self.event_name
        
        
class EventOccurence(models.Model):
    event_id = models.ForeignKey(Events)
    frequency = models.IntegerField(default=0)
    wmd = models.IntegerField(default=0)
    eo_start_date = models.DateField(default=datetime.now())    
    eo_end_date = models.DateField(default=datetime.now())
    
    def __unicode__(self):
            return self.pk
        
class Instructors(models.Model):
    first_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)  
    email = models.CharField(max_length = 128)
    contact_number = models.CharField(max_length = 128)
    def __unicode__(self):
            return self.pk
    
class EventsInstructors(models.Model):
    event_id = models.ForeignKey(Events)
    instructors_id = models.ForeignKey(Instructors)
    def __unicode__(self):
            return self.pk
    
    
        
        
        