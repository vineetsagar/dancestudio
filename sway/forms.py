import datetime

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.query_utils import Q
from django.forms.forms import Form
from django.forms.models import ModelForm

from sway.form_validators import validate_name_field, validate_address, validate_phone_number 
from sway.models import Events, EventType, EventCategory, Studio, EventLocations
from sway.models import Members, EventCategory, Instructors, Lead, LeadFollowUp


class EventsForm(ModelForm):
    all_day = forms.BooleanField(initial=False, required=False)
    repeat = forms.BooleanField(initial=False, required=False)
    CHOICES = (('1', 'Never',), ('2', 'After',),('3', 'On',))
    WEEKDAY_CHOICES = (('0', 'Mo',), ('1', 'Tu',),('2', 'Wed',),('3', 'Th',), ('4', 'Fri',),('5', 'Sat',),('6', 'Sun',))
    never = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial="1")
    weeklyRepeat = forms.MultipleChoiceField(choices=WEEKDAY_CHOICES, widget=forms.CheckboxSelectMultiple,  initial="1", required = False)
    after = forms.IntegerField(required = False)
    on = forms.CharField(required = False)
    
    def __init__(self, request, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        # this will filter the event type value, i.e we do not want to render 'once' value on the UI, hence this will filter it
        self.fields['event_type'].queryset = EventType.objects.filter(~Q(id = 1))
        self.fields['event_type'].empty_label = None
        self.fields['event_category'].queryset = EventCategory.objects.filter(Q(studio = request.user.studiouser.studio_id))
    class Meta:
        model = Events
        fields = ['event_name', 'event_category','start_date','start_time', 'end_date','end_time', 'all_day', 'repeat', 'event_type']
        exclude = ('studio','created_date', 'modified_date', 'created_by', 'modified_by')
    def clean_start_time(self):
        return self.cleaned_data.get("start_time")
    def clean_event_name(self):
        cd = self.cleaned_data
        event_name = cd.get("event_name")
        if len(event_name) < 5 or len(event_name) > 100   : 
            raise forms.ValidationError("Event name character length should be in between 5 to 100 characters.")
        return event_name
    
    def clean(self):
        cd = self.cleaned_data
        event_type_value = cd.get("event_type")
        repeat_value = cd.get("repeat")
        if repeat_value:
            if event_type_value is None:
                self.add_error('event_type', "Please select Repeat value")
                
        all_day = cd.get("all_day")
        start_time = cd.get("start_time")
        end_time = cd.get("end_time")
        
        start_date = cd.get("start_date")
        end_date = cd.get("end_date")
        sDate = datetime.datetime.combine(start_date, datetime.time.min) 
        eDate = datetime.datetime.combine(end_date, datetime.time.min)
        if sDate > eDate:
            self.add_error('start_date', "Start date should be less than end date")
            self.add_error('end_date', "End date should be greater than start date")
            
        if not all_day :
            if start_time > end_time:
                self.add_error('start_time', "Start time should be less than end time")
                self.add_error('end_time', "End time should be greater than start time")
        else:
            if 'start_time' not in self.cleaned_data:
                del self._errors["start_time"]
            if 'end_time' not in self.cleaned_data:
                del self._errors["end_time"]
            
        never = cd.get("never")
        if never =='2':
            # that user should provide value of after as well
                after = cd.get("after")
                if after <= 0 or after > 10:
                    self.add_error('after', "This should be between 1 to 10")
        elif never == '3':
            on = cd.get("on")
            onDate =    datetime.datetime.strptime(on, "%m/%d/%Y")
            if onDate < sDate:
                self.add_error('on', "Please choose date greater than start date")
                        
        return cd

class MemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField()
    area = forms.CharField(max_length=128)
        
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True
    
    class Meta:
        model = Members
        exclude = ('studio','created_date', 'modified_date', 'created_by', 'modified_by')
        
        
    def clean(self):
        cleaned_data=super(MemberForm, self).clean()
        print cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email =cleaned_data.get("email")
        addr=cleaned_data.get("area")
        
        msg_invalid_name=u"Invalid name."
       
        if validate_name_field(first_name):
            print "Correct name",first_name;
        else:
            print "Invalid chars in first_name",first_name;
            self.add_error('first_name',msg_invalid_name)
        
        if validate_name_field(last_name):
            print "Correct name",last_name;
        else:
            print "Invalid chars in last_name",last_name;
            self.add_error('last_name',msg_invalid_name)
               
        if validate_address(addr):
            print "Valid addr",addr;
        else:
            print "Invalid address=",addr;
            self.add_error('area',u"Invalid address.")    
    
class InstructorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField()
    contact_number = forms.CharField(max_length=128)
        
    def __init__(self, *args, **kwargs):
        super(InstructorForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True
            
    
    class Meta:
        model = Instructors
        exclude = ('studio','created_date', 'modified_date', 'created_by', 'modified_by')
        
    def clean(self):
        cleaned_data=super(InstructorForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email =cleaned_data.get("email")
        contact_number=cleaned_data.get("contact_number")
        
        msg_invalid_name=u"Invalid name."
       
        if validate_name_field(first_name):
            print "Correct name",first_name;
        else:
            print "Invalid chars in first_name",first_name;
            self.add_error('first_name',msg_invalid_name)
        
        if validate_name_field(last_name):
            print "Correct name",last_name;
        else:
            print "Invalid chars in last_name",last_name;
            self.add_error('last_name',msg_invalid_name)
               
        if validate_phone_number(contact_number):
            print "Valid contact no",contact_number;
        else:
            print "Invalid contact no=",contact_number;
            self.add_error('contact_number',u"Invalid contact number.")    
        
class LeadForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    contact_detail = forms.CharField(max_length=255)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=128)
    inquiryFor = forms.CharField(max_length=255)
        
    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True
    
    class Meta:
        model = Lead
        exclude = ('studio',)
        
    def clean(self):
        cleaned_data=super(LeadForm, self).clean()
        name = cleaned_data.get("name")
        contact_detail = cleaned_data.get("contact_detail")
        email =cleaned_data.get("email")
        mobile=cleaned_data.get("mobile")
        inquiryFor=cleaned_data.get("inquiryFor")
        
        msg_invalid_name=u"Invalid name."
       
        if validate_name_field(name):
            print "Correct name",name;
        else:
            print "Invalid chars in name",name;
            self.add_error('name',msg_invalid_name)
        
        if validate_name_field(contact_detail):
            print "Correct name",contact_detail;
        else:
            print "Invalid chars in contact_detail",contact_detail;
            self.add_error('contact_detail',msg_invalid_name)
               
        if validate_phone_number(mobile):
            print "Valid contact no",mobile;
        else:
            print "Invalid contact no=",mobile;
            self.add_error('mobile',u"Invalid contact number.")        


class EventLocationForm(forms.ModelForm):
    event_location_name = forms.CharField(max_length=128)
    class Meta:
        model = EventLocations
        exclude = ('studio','created_date', 'modified_date', 'created_by', 'modified_by')
    def __init__(self,  *args, **kwargs):
        super(EventLocationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True    
    def clean(self):
        print "*******inside self method*********"
        cleaned_data=super(EventLocationForm, self).clean()
        event_location_name = cleaned_data.get("event_location_name")
        msg_invalid_name=u"Invalid location name."
        if validate_address(event_location_name):
            print "location name",event_location_name;
        else:
            print "Invalid chars in location name",event_location_name;
            self.add_error('event_location_name',msg_invalid_name)
        return cleaned_data
    
class EventCategoryForm(forms.ModelForm):
    event_category_name = forms.CharField(max_length=128)
    class Meta:
        model = EventCategory
        exclude = ('studio','created_date', 'modified_date', 'created_by', 'modified_by')
    def __init__(self,  *args, **kwargs):
        super(EventCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True    
    def clean(self):
        print "*******inside self method*********"
        cleaned_data=super(EventCategoryForm, self).clean()
        event_category_name = cleaned_data.get("event_category_name")
        msg_invalid_name=u"Invalid category name."
        if validate_name_field(event_category_name):
            print "Category name",event_category_name;
        else:
            print "Invalid chars in category name",event_category_name;
            self.add_error('name',msg_invalid_name)
        return cleaned_data
        
class FollowupForm(forms.ModelForm):
    notes = forms.CharField(max_length=128,required=True)
    nextFollowupDate = forms.DateTimeField(required=False)
        
    def __init__(self, *args, **kwargs):
        super(FollowupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    
    class Meta:
        model = LeadFollowUp
        exclude = ('studio','created_date', 'modified_date', 'created_by', 'modified_by')
    def clean(self):
        cleaned_data=super(FollowupForm, self).clean()
        notes = cleaned_data.get("notes")
        nextFollowupDate = cleaned_data.get("nextFollowupDate")
        
               
        