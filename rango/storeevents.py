from datetime import datetime

from rango.models import Events, EventType, EventCategory, EventOccurence


def storeevents(request):
    print(request)
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
    
    startDate =    datetime.strptime(start_date, "%m/%d/%Y")
    endDate =    datetime.strptime(end_date, "%m/%d/%Y")
    
    data.start_date = startDate
    data.end_date = endDate
    
    allDay = request.POST.get("all_day")
    
    if allDay =='true':
        data.start_time = datetime.time(0, 0, 0)
        data.end_time = datetime.time(24, 0, 0)
    else:
        data.start_time = datetime.strptime(start_time, '%H:%M')
        data.end_time = datetime.strptime(end_time, '%H:%M')
        
    repeat = request.POST.get("repeat")
    
    never_ends = request.POST.get("neverEnds")
    
    occurrencesEnds = request.POST.get("occurrencesEnds")
    occurrencesEndsValue = request.POST.get("occurrencesEndsValue")
    
    endsOn = request.POST.get("endsOn")
    endsOnValue = request.POST.get("endsOnValue")
    
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
                
            
            
        
        
    
 
    
    
    
    
    
    