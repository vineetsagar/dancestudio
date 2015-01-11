import datetime

from django import forms
from django.db.models.query_utils import Q
from django.forms.models import ModelForm

from sway.models import Events, EventType


class EventsForm(ModelForm):
    all_day = forms.BooleanField(initial=False, required=False)
    repeat = forms.BooleanField(initial=False, required=False)
    CHOICES = (('1', 'Never',), ('2', 'After',),('3', 'On',))
    WEEKDAY_CHOICES = (('0', 'Mo',), ('1', 'Tu',),('2', 'Wed',),('3', 'Th',), ('4', 'Fri',),('5', 'Sat',),('6', 'Sun',))
    never = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial="1")
    weeklyRepeat = forms.MultipleChoiceField(choices=WEEKDAY_CHOICES, widget=forms.CheckboxSelectMultiple,  initial="1", required = False)
    after = forms.IntegerField(required = False)
    on = forms.CharField(required = False)
    
    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        # this will filter the event type value, i.e we do not want to render 'once' value on the UI, hence this will filter it
        self.fields['event_type'].queryset = EventType.objects.filter(~Q(id = 1))
        self.fields['event_type'].empty_label = None
    class Meta:
        model = Events
        fields = ['event_name', 'event_category','start_date','start_time', 'end_date','end_time', 'all_day', 'repeat', 'event_type']
    def clean_start_time(self):
        return self.cleaned_data.get("start_time")
    def clean_event_name(self):
        cd = self.cleaned_data
        event_name = cd.get("event_name")
        print "length ", len(event_name)
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
                print 'print after', after
                if after <= 0 or after > 10:
                    print 'inside ',after
                    self.add_error('after', "This should be between 1 to 10")
        elif never == '3':
            on = cd.get("on")
            onDate =    datetime.datetime.strptime(on, "%m/%d/%Y")
            if onDate < sDate:
                self.add_error('on', "Please choose date greater than start date")
                        
        return cd
        
        