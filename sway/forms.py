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
    after = forms.CharField(required = False)
    on = forms.CharField(required = False)
    
    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        # this will filter the event type value, i.e we do not want to render 'once' value on the UI, hence this will filter it
        self.fields['event_type'].queryset = EventType.objects.filter(~Q(id = 1))
        self.fields['event_type'].empty_label = None
    class Meta:
        model = Events
        fields = ['event_name', 'event_category','start_date','start_time', 'end_date','end_time', 'all_day', 'repeat', 'event_type']
    
    def clean_event_name(self):
        cd = self.cleaned_data
        event_name = cd.get("event_name")
        if len(event_name) < 5  : 
            raise forms.ValidationError("Event name should have at-least 5 character")
        return event_name
    
    def clean_weekly_repeat(self):
        cd = self.cleaned_data
        weeklyRepeat = cd.getlist("weeklyRepeat")
        print 'weeklyRepeat', weeklyRepeat
        return weeklyRepeat
    
    def clean_event_type(self):
        cd = self.cleaned_data
        event_type_value = cd.get("event_type")
        repeat_value = cd.get("repeat")
        if repeat_value:
            if event_type_value is None:
                raise forms.ValidationError("Required")
        return event_type_value;
        
    def clean(self):
        cd = self.cleaned_data
        return cd
        
        