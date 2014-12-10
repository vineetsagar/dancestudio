import datetime
from dateutil.relativedelta import relativedelta

from rango.models import Events, EventType, EventCategory, EventOccurence


def calculateMonthBitValue(request):
    value = request.POST.get("repeatby")
    if value == 'dm':
        return 2**9 
    else:
        return 2**10

def weeklyBitValue(request):
    # 0 == Daily
    # 1 == Monthly
    # 2 == Mon
    # 3 == Tue
    # 4 == Wed
    # 5 == Thursday
    # 6 == Friday
    # 7 == Sat
    # 8 == Sun

    mondayOn = request.POST.get("MO")
    tuesdayOn = request.POST.get("TU")
    wednesdayOn = request.POST.get("WE")
    thursdayOn = request.POST.get("TH")
    fridayOn = request.POST.get("FR")
    saturdayOn = request.POST.get("SA")
    sundayOn = request.POST.get("SU")
    
    value = 0
    if mondayOn == 'on':
        value = value + 2*2
    if tuesdayOn == 'on':
        value = value + 2*2*2
    if wednesdayOn == 'on':
        value = value + 2*2*2*2
    if thursdayOn == 'on':
        value = value + 2*2*2*2*2
    if fridayOn == 'on':
        value = value + 2*2*2*2*2*2
    if saturdayOn == 'on':
        value = value + 2*2*2*2*2*2*2   
    if sundayOn == 'on':
        value = value + 2*2*2*2*2*2*2*2   

    return value

def storeevents(request):
    
    data= Events()
    data.event_name = request.POST.get("event_name")

    # event category salsa or bachata as of now
    event_category_name = request.POST.get("event_category")
    eventCategory = EventCategory.objects.get(event_category_name=event_category_name )
    data.event_category = eventCategory
    
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
    else:
        # no need for else loop here as we going to store default value i.e. midnight to midnight
        data.all_day = True
     
        
    repeat = request.POST.get("repeat")
    if repeat !='on':
        data.event_type = EventType.objects.get(event_type_name='Once' )
    else:  
        data.event_type = EventType.objects.get(event_type_name=event_type )
     
    print("before saving event  now") 
    Events.save(data)    
    print("saving event  now")
    eventOccurence = EventOccurence()
    eventOccurence.event_id = data
    #  event_id = models.ForeignKey(Events)
    # frequency = models.IntegerField(default=0)
    # wmd = models.IntegerField(default=0)
    # eo_start_date = models.DateField(default=datetime.now())    
    # eo_end_date = models.DateField(default=datetime.now())
    
    if repeat=='on':
        endTimeRadioGroup = request.POST.get("endTimeGroup")
        eventOccurence.frequency = request.POST.get("frequency")
        eventOccurence.eo_start_date = startDate
        eventTypeValue = EventType.objects.get(event_type_name=event_type )
        
        if endTimeRadioGroup == 'on':
            endsOnValue = request.POST.get("endsOnValue")
            # will get a end date here
            eventOccurence.eo_end_date = datetime.datetime.strptime(endsOnValue, "%m/%d/%Y")
            eventOccurence.wmd=1
            if eventTypeValue.event_type_name =='Weekly':
                value =  weeklyBitValue(request)
                eventOccurence.wmd=value
            elif eventTypeValue.event_type_name =='Monthly':
                eventOccurence.wmd = calculateMonthBitValue(request)
            else:
                # get all the selected days
                eventOccurence.wmd=1
        else:
            if endTimeRadioGroup == 'after':
                # need to get the frequency here
                # will get a number of times this event should occurred
                # it is daily, weekly or monthly
                frequency = eventOccurence.frequency
                occurrencesEndsValue = request.POST.get("occurrencesEndsValue")
                print(occurrencesEndsValue)
                if eventTypeValue.event_type_name =='Weekly':
                    value =  weeklyBitValue(request)
                    eventOccurence.wmd=value
                    eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(weeks=(int(frequency) * int(occurrencesEndsValue) ))
                elif eventTypeValue.event_type_name =='Monthly':
                    eventOccurence.wmd=calculateMonthBitValue(request)
                    eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(months=(int(frequency) * int(occurrencesEndsValue)))
                else:
                    eventOccurence.wmd=1
                    eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(days=( int(frequency) * int(occurrencesEndsValue)))
            else:
                # never selected by user, hence set the end date to be exactly after a year
                eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(years=1)
                if eventTypeValue.event_type_name =='Weekly':
                    value =  weeklyBitValue(request)
                    eventOccurence.wmd=value
                elif eventTypeValue.event_type_name =='Monthly':
                    eventOccurence.wmd=calculateMonthBitValue(request)
                else:
                    eventOccurence.wmd=1
 
    #save event occurrence now            
    EventOccurence.save(eventOccurence)       
            
    
    
    
    
    
    