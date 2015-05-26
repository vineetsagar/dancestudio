import datetime
import math

from django.db.models.query_utils import Q

from sway.forms import EventsForm
from sway.models import EventOccurence, EventType, EventCategory


def setFormDefaultCssAndPlaceHolder(form):
    form.fields['event_name'].widget.attrs = {'class':'form-control', 'placeholder':'Enter event name'}
    form.fields['event_category'].widget.attrs = {'class':'form-control'}
    form.fields['event_location'].widget.attrs = {'class':'form-control'}
    form.fields['start_date'].widget.attrs = {'class':'date start'}
    form.fields['end_date'].widget.attrs = {'class':'date start'}
    form.fields['start_time'].widget.attrs = {'class':'time start'}
    form.fields['end_time'].widget.attrs = {'class':'time start'}
    form.fields['event_type'].widget.attrs = {'class':'form-control'}
    form.fields['on'].widget.attrs = {'class':'date start'}
    form.fields['after'].widget.attrs = {'placeholder':'Number of times'}

def getForm(request):
    form = EventsForm(request, initial={'start_date':datetime.datetime.now().strftime("%m/%d/%Y"), 'end_date':datetime.datetime.now().strftime("%m/%d/%Y")})
    setFormDefaultCssAndPlaceHolder(form)
    return form

def weekDaysValue(wmdValue):
    # 0 == Mon
    # 1 == Tue
    # 2 == Wed
    # 3 == Thursday
    # 4 == Friday
    # 5 == Sat
    # 6 == Sun
    lst=[]
    if (wmdValue & int(math.pow( 2, 2 )) ) == (int(math.pow( 2, 2 ))):
        lst.append(0 )
    if(wmdValue & int(math.pow( 2, 3 ) )) == (int(math.pow( 2, 3 ))):
        lst.append(1 )
    if (wmdValue & int(math.pow( 2, 4 )) ) == (int(math.pow( 2, 4 ))):
        lst.append(2 )
    if (wmdValue & int(math.pow( 2, 5) ) ) == (int(math.pow( 2, 5 ))):
        lst.append(3 )
    if (wmdValue & int(math.pow( 2, 6 )) ) == (int(math.pow( 2, 6 ))):
        lst.append(4 )
    if (wmdValue & int(math.pow( 2, 7 )) ) == (int(math.pow( 2, 7 ))):
        lst.append(5 )
    if (wmdValue & int(math.pow( 2, 8 )) ) == (int(math.pow( 2, 8 ))):
        lst.append(6 )
    return lst

def getEventForm(request, event):
    
    eventOccurence = EventOccurence.objects.filter(events = event)

    repeatflag = False;
    if eventOccurence.count() > 0:
        repeatflag = True;

    # find out it it is weekly event
    eventType = event.event_type
    list = [1]
    eventTypeValue = EventType.objects.filter(event_type_name=eventType)
    for et in eventTypeValue:
        if et.event_type_name =='Weekly':
            for v in eventOccurence:
                list =  weekDaysValue(v.wmd)
    
    never_List = 1
    if repeatflag:
        if eventOccurence[0].e_never:
            never_List = 1
        if eventOccurence[0].e_on:
            never_List = 3
        if eventOccurence[0].e_after:
            never_List = 2
        
    form = EventsForm(request, instance=event, initial={'repeat':repeatflag, 'all_day':event.all_day, 'event_type':eventType, 'weeklyRepeat': list, 'never':never_List})
    #form.fields['weeklyRepeat'].widget.attrs = {'checked':'1,2'}
    form.fields['event_name'].widget.attrs = {'class':'form-control', 'placeholder':'Enter event name'}
    form.fields['event_category'].widget.attrs = {'class':'form-control'}
    form.fields['event_location'].widget.attrs = {'class':'form-control'}
    form.fields['start_date'].widget.attrs = {'class':'date start'}
    form.fields['start_time'].widget.attrs = {'class':'time start'}
    form.fields['end_time'].widget.attrs = {'class':'time start'}
    form.fields['event_type'].widget.attrs = {'class':'form-control'}
    form.fields['on'].widget.attrs = {'class':'date start'}
    if repeatflag:
        if eventOccurence[0].e_on:
            form.fields['on'].widget.attrs = {'value':eventOccurence[0].e_on_value.strftime("%m/%d/%Y")}
        if eventOccurence[0].e_after:
            #form.fields['after'].value = eventOccurence[0].e_after_value
            form.fields['after'].widget.attrs = {'value':eventOccurence[0].e_after_value}
    
    return form