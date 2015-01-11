from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default


#from scipy.special.lambertw import __str__
class Studio(models.Model):
    studio_name = models.CharField(max_length = 128)
    studio_contact = models.CharField(max_length = 255)
    studio_logo = models.CharField(max_length = 255)
    studio_phone = models.CharField(max_length = 128)
    def __unicode__(self):
            return self.studio_name

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
        studio = models.ForeignKey(Studio)
        def __unicode__(self):
            return self.email

class MembersView(models.Model):
        selected = models.BooleanField(default = False)
        member = models.OneToOneField(Members)
        class Meta:
            abstract = True
            
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
        event_category = models.ForeignKey(EventCategory)
        event_type = models.ForeignKey(EventType)
        
        start_date = models.DateField(default=datetime.now())
        end_date = models.DateField(default=datetime.now())
        
        start_time = models.TimeField(default='00:00')
        end_time = models.TimeField(default='00:00')
        studio = models.ForeignKey(Studio)
        
        def __unicode__(self):
            return self.event_name
        
        
class EventOccurence(models.Model):
    events = models.OneToOneField(Events)
    frequency = models.IntegerField(default=0)
    wmd = models.IntegerField(default=0)
    eo_start_date = models.DateField(default=datetime.now())    
    eo_end_date = models.DateField(default=datetime.now())
    
    # adding following colomns for ui
    e_never = models.BooleanField(default=False)
    
    e_after = models.BooleanField(default=False)
    e_after_value = models.IntegerField(default=0)
    
    e_on = models.BooleanField(default=False)
    e_on_value = models.DateField(default=datetime.now())

    def __unicode__(self):
            return str(self.pk)

class EventMembers(models.Model):
    event = models.ForeignKey(Events)
    member = models.ForeignKey(Members)
    def __unicode__(self):
            return u'%s' % (self.pk)
        
class Instructors(models.Model):
    first_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)  
    email = models.CharField(max_length = 128)
    contact_number = models.CharField(max_length = 128)
    studio = models.ForeignKey(Studio)
    def __unicode__(self):
            return self.pk
    
class EventsInstructors(models.Model):
    event_id = models.ForeignKey(Events)
    instructors_id = models.ForeignKey(Instructors)
    def __unicode__(self):
            return self.pk
        
class StudioUser(models.Model):
    user = models.OneToOneField(User)
    studio_id = models.ForeignKey(Studio)    
    def __unicode__(self):
            return str(self.pk)
    

class Lead(models.Model):    
    name =  models.CharField(max_length = 128)
    contact_detail = models.CharField(max_length = 255)
    email = models.CharField(max_length = 128)
    mobile = models.CharField(max_length = 128)
    studio = models.ForeignKey(Studio) 
    def __unicode__(self):
            return self.pk  
         

class LeadFollowUp(models.Model):    
    lead = models.ForeignKey(Lead)
    notes = models.CharField(max_length = 255)
    followed_by = models.ForeignKey(User)
    followed_date = models.DateField(default=datetime.now()) 
    def __unicode__(self):
            return self.pk         
