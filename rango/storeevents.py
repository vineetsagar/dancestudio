import datetime

from rango.models import Events, EventType, EventCategory, EventOccurence
from dateutil.relativedelta import relativedelta

def storeevents(request):
    data= Events()
    
    data.event_name = request.POST.get("event_name")

    # event category salsa or bachata as of now
    event_category_name = request.POST.get("event_category")
    eventCategory = EventCategory.objects.get(event_category_name=event_category_name )
    data.event_category_id = eventCategory
    
    event_type = request.POST.get("eventType")
    
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    
    startDate =    datetime.datetime.strptime(start_date, "%m/%d/%Y")
    endDate =    datetime.datetime.strptime(end_date, "%m/%d/%Y")
    
    data.start_date = startDate
    data.end_date = endDate
    
    allDay = request.POST.get("all_day")
    
    if allDay !='on':
        data.start_time = datetime.datetime.strptime(start_time, '%H:%M')
        data.end_time = datetime.datetime.strptime(end_time, '%H:%M')
        # no need for else loop here as we going to store default value i.e. midnight to midnight
        
    repeat = request.POST.get("repeat")

    eventOccurence = EventOccurence()
    
    if repeat=='on':
        endTimeRadioGroup = request.POST.get("endTimeGroup")
        eventOccurence.frequency = request.Post.get("frequency")
        eventOccurence.eo_start_date = startDate
        if endTimeRadioGroup == 'on':
            endsOnValue = request.POST.get("endsOnValue")
            # will get a end date here
            eventOccurence.eo_end_date = datetime.datetime.strptime(endsOnValue, "%m/%d/%Y")
        else:
            if endTimeRadioGroup == 'after':
                occurrencesEndsValue = request.POST.get("occurrencesEndsValue")
                # need to get the frequency here
                # will get a number of times this event should occurred
            else:
                # never selected by user, hence set the end date to be exactly after a year
                eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(years=1)
        
                
    if (repeat != 'true'  and allDay !='true' ):
            event_type_name = 'Once'
            eventType = EventType.objects.get(event_type_name=event_type_name )
            data.event_type_id =eventType
            Events.save(data) # its a normal event
    else:
        if (repeat == 'true' and all == 'true'):
            eventType = EventType.objects.get(event_type_name=event_type )
            data.event_type_id = eventType
            #Events.save(data) # repeat and all day event
        else:
            if(repeat =='true'):
                eventType = EventType.objects.get(event_type_name=event_type )
                data.event_type_id = eventType
                #Events.save(data) # repeat event
            else:
                eventOccurence = EventOccurence()
                event_type_name = 'Once'
                eventType = EventType.objects.get(event_type_name=event_type_name )
                #Events.save(data) # all day event
                
            
            
        
        
    
 
    
    
    
    
    
    