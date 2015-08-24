from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import default

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core import serializers
import json


# A base model that alll other model shall extend
# THis model is abstract since this can't be instantiated an is a mean to keep all the common fields in one class
class BaseModel(models.Model):
    created_date = models.DateTimeField(default=datetime.now(),blank=True)
    created_by =  models.ForeignKey(User,related_name='%(class)s_created_by',null=True,blank=True)
    modified_date = models.DateTimeField(null=True,default=datetime.now(),auto_now=True)
    modified_by =   models.ForeignKey(User,related_name='%(class)s_modified_by',null=True,blank=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        modified_date = datetime.now()
        super(BaseModel, self).save(*args, **kwargs)

#from scipy.special.lambertw import __str__
class Studio(BaseModel):
    name = models.CharField(max_length = 128)
    area = models.CharField(max_length = 512,null=True,blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+91'. Up to 10 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    email_host = models.CharField(max_length=100,null=True,blank=True)
    email_port = models.PositiveIntegerField()
    email_user_name = models.CharField(max_length=512,null=True,blank=True)
    email_password = models.CharField(max_length=512,null=True,blank=True)
    global_email_from = models.EmailField(null=True,blank=True) 
    def __unicode__(self):
            return self.name

class EventCategory(BaseModel):
        event_category_name = models.CharField(max_length = 128)
        studio = models.ForeignKey(Studio)
        def __unicode__(self):
            return self.event_category_name

class Members(BaseModel):
        first_name = models.CharField(max_length=128)
        last_name = models.CharField(max_length=128)
        email = models.EmailField()
        area = models.TextField()
        #birth_date = models.DateField(null=True,blank=True)
        studio = models.ForeignKey(Studio)
        categories = models.ManyToManyField(EventCategory,blank=True,null=True,related_name="members")
        GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'))
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
        def __unicode__(self):
            return self.email

class MembersView(BaseModel):
        selected = models.BooleanField(default = False)
        member = models.OneToOneField(Members)
        class Meta:
            abstract = True
            
class EventType(BaseModel):
        event_type_name = models.CharField(max_length = 128)
        def __unicode__(self):
            return self.event_type_name
        
class EventLocations(BaseModel):
        event_location_name = models.CharField(max_length = 128)
        studio = models.ForeignKey(Studio)
        def __unicode__(self):
            return self.event_location_name
        
class UserActionLogs(BaseModel):
        description = models.CharField(max_length = 200)
        studio = models.ForeignKey(Studio)
        def __unicode__(self):
            return self.description

class Events(BaseModel):
        event_name = models.CharField(max_length=128)
        all_day= models.BooleanField(default=False)
        event_category = models.ForeignKey(EventCategory)
        event_location = models.ForeignKey(EventLocations, null=True)
        event_type = models.ForeignKey(EventType)
        
        start_date = models.DateField(default=datetime.now())
        end_date = models.DateField(default=datetime.now())
        
        start_time = models.TimeField(default='00:00')
        end_time = models.TimeField(default='00:00')
        studio = models.ForeignKey(Studio)
        
        def __unicode__(self):
            return self.event_name
        
        
class EventOccurence(BaseModel):
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

class EventMembers(BaseModel):
    event = models.ForeignKey(Events)
    member = models.ForeignKey(Members)
    def __unicode__(self):
            return u'%s' % (self.pk)
        
class Instructors(BaseModel):
    first_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)  
    email = models.CharField(max_length = 128)
    contact_number = models.CharField(max_length = 128)
    studio = models.ForeignKey(Studio)
    def __unicode__(self):
            return self.pk
    
class EventsInstructors(BaseModel):
    event_id = models.ForeignKey(Events)
    instructors_id = models.ForeignKey(Instructors)
    def __unicode__(self):
            return self.pk
        
class StudioUser(BaseModel):
    user = models.OneToOneField(User)
    studio_id = models.ForeignKey(Studio)    
    def __unicode__(self):
            return str(self.pk)
        
class ProductContacts(BaseModel):
    name = models.CharField(max_length = 128)
    email = models.CharField(max_length = 128)
    message = models.CharField(max_length = 1024)
    def __unicode__(self):
            return str(self.pk)
    

class Lead(BaseModel):    
    name =  models.CharField(max_length = 128)
    contact_detail = models.CharField(max_length = 255)
    email = models.CharField(max_length = 128)
    mobile = models.CharField(max_length = 128)
    nextFollowUpDate = models.DateTimeField(default=None,null=True,blank=True)
    inquiryFor = models.CharField(max_length=255,null=True)
    studio = models.ForeignKey(Studio) 
    status = models.PositiveIntegerField(default=3)
    short_description = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
            return str(self.pk)  
         

class LeadFollowUp(BaseModel):    
    lead = models.ForeignKey(Lead, related_name="followups")
    notes = models.CharField(max_length = 255)
    followed_by = models.ForeignKey(User)
    followed_date = models.DateField(auto_now_add=True) 
    def __unicode__(self):
            return str(self.pk)

class Comments(BaseModel):    
    studio = models.ForeignKey(Studio) 
    comment_notes = models.CharField(max_length = 255)
    comments_type = models.CharField(max_length = 255)
    comment_for = models.CharField(max_length = 255)
    def __unicode__(self):
            return str(self.pk)         


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)