import datetime
from dateutil.relativedelta import relativedelta

from sway.models import Events, EventType, EventCategory, EventOccurence, EventLocations


def calculateMonthBitValue(request):
    value = request.POST.get("repeatby")
    if value == 'dm':
        return 2**9 
    else:
        return 2**10

def weeklyBitValue(request):
    # bit operations
    # 0 == Daily
    # 1 == Monthly
    # 2 == Mon
    # 3 == Tue
    # 4 == Wed
    # 5 == Thursday
    # 6 == Friday
    # 7 == Sat
    # 8 == Sun
    # 9 == day of the month
    #10 == day of the week

    value = 0
    weekly_repeat_array = request.POST.getlist("weeklyRepeat")
    for weekly in weekly_repeat_array:
        if (str(weekly) == '0'):
            value = value + 2*2
        if (str(weekly) == '1'):
            value = value + 2*2*2
        if (str(weekly) == '2'):
            value = value + 2*2*2*2
        if (str(weekly) == '3'):
            value = value + 2*2*2*2*2
        if (str(weekly) == '4'):
            value = value + 2*2*2*2*2*2
        if (str(weekly) == '5'):
            value = value + 2*2*2*2*2*2*2   
        if (str(weekly) == '6'):
            value = value + 2*2*2*2*2*2*2*2   
    return value


def add_event_occurence_object(request, db_event_obj, event_type, startDate, repeat):
    if repeat == 'on':
        eventOccurence = EventOccurence()
        eventOccurence.events_id = db_event_obj.id
        never = request.POST.get("never") # as of now we are going to keep the frequency one day
        eventOccurence.frequency = 1
        eventOccurence.eo_start_date = startDate
        eventTypeValue = EventType.objects.get(pk=event_type)
        if (str(never) == '3'): # this mean it is 'On'
            on_value = request.POST.get("on")
            eventOccurence.e_on = True
            eventOccurence.e_on_value = datetime.datetime.strptime(on_value, "%m/%d/%Y")
            # will get a end date here
            eventOccurence.eo_end_date = datetime.datetime.strptime(on_value, "%m/%d/%Y")
            eventOccurence.wmd = 1
            if eventTypeValue.event_type_name == 'Weekly':
                value = weeklyBitValue(request)
                eventOccurence.wmd = value
            elif eventTypeValue.event_type_name == 'Monthly':
                eventOccurence.wmd = calculateMonthBitValue(request)
            else:
                eventOccurence.wmd = 1 # get all the selected days
        elif (str(never) == '2'):
            # need to get the frequency here
            # will get a number of times this event should occurred
            # it is daily, weekly or monthly
            frequency = eventOccurence.frequency
            after_value = request.POST.get("after")
            eventOccurence.e_after = True
            eventOccurence.e_after_value = int(after_value)
            if eventTypeValue.event_type_name == 'Weekly':
                value = weeklyBitValue(request)
                eventOccurence.wmd = value
                eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(weeks=(int(frequency) * int(after_value)))
            elif eventTypeValue.event_type_name == 'Monthly':
                eventOccurence.wmd = calculateMonthBitValue(request)
                eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(months=(int(frequency) * int(after_value)))
            else:
                eventOccurence.wmd = 1
                eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(days=(int(frequency) * int(after_value)))
        else:
            eventOccurence.eo_end_date = eventOccurence.eo_start_date + relativedelta(years=1)
            eventOccurence.e_never = True
            if eventTypeValue.event_type_name == 'Weekly':
                value = weeklyBitValue(request)
                eventOccurence.wmd = value
            elif eventTypeValue.event_type_name == 'Monthly':
                eventOccurence.wmd = calculateMonthBitValue(request)
            else:
                eventOccurence.wmd = 1
        #save event occurrence now
            # never selected by user, hence set the end date to be exactly after a year
        EventOccurence.save(eventOccurence)

def updateEvents(request):
    event_id = request.POST.get("event_id")
    eventQuerySet = Events.objects.filter(pk = event_id)
    if eventQuerySet.count() <= 0:
        return
    db_event_obj  = eventQuerySet[0]
    
    db_event_obj.event_name = request.POST.get("event_name")

    # event category salsa or bachata as of now
    event_category_name = request.POST.get("event_category")
    eventCategory = EventCategory.objects.get(pk=event_category_name)

    db_event_obj.event_category = eventCategory
    
    event_type = request.POST.get("event_type")
    
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    
    startDate =    datetime.datetime.strptime(start_date, "%m/%d/%Y")
    endDate =    datetime.datetime.strptime(end_date, "%m/%d/%Y")
    
    db_event_obj.start_date = startDate
    db_event_obj.end_date = endDate
    
    allDay = request.POST.get("all_day")
    
    if allDay !='on':
        db_event_obj.start_time = datetime.datetime.strptime(start_time, '%H:%M')
        db_event_obj.end_time = datetime.datetime.strptime(end_time, '%H:%M')
    else:
        # no need for else loop here as we going to store default value i.e. midnight to midnight
        db_event_obj.all_day = True
     
        
    repeat = request.POST.get("repeat")
    
    if repeat == 'on':
        db_event_obj.event_type = EventType.objects.get(pk=event_type )
    else:
        db_event_obj.event_type = EventType.objects.get(event_type_name='Once')
     
    Events.save(db_event_obj)    
   
    #  event_id = models.ForeignKey(Events)
    # frequency = models.IntegerField(default=0)
    # wmd = models.IntegerField(default=0)
    # eo_start_date = models.DateField(default=datetime.now())    
    # eo_end_date = models.DateField(default=datetime.now())
    eventOccurenceQuerySet = EventOccurence.objects.filter(events = db_event_obj)
    # first we will delete the occurence object and will re added it
    
    if eventOccurenceQuerySet.count( ) > 0:
        eventOccurenceQuerySet[0].delete()
    add_event_occurence_object(request, db_event_obj, event_type, startDate, repeat) 
        
        
def storeevents(request):
    data= Events()
    data.created_by = request.user
    data.modified_by = request.user
    data.event_name = request.POST.get("event_name")

    # event category salsa or bachata as of now
    event_category_name = request.POST.get("event_category")
    event_location_name = request.POST.get("event_location")
    eventCategory = EventCategory.objects.get(pk=event_category_name)
    eventLocation = EventLocations.objects.get(pk=event_location_name)

    data.event_category = eventCategory
    data.event_location = eventLocation
    
    event_type = request.POST.get("event_type")
    
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
    
    if repeat == 'on':
        data.event_type = EventType.objects.get(pk=event_type )
    else:
        data.event_type = EventType.objects.get(event_type_name='Once')
    studio_data=request.user.studiouser.studio_id
    data.studio =studio_data
    Events.save(data)    
   
    #  event_id = models.ForeignKey(Events)
    # frequency = models.IntegerField(default=0)
    # wmd = models.IntegerField(default=0)
    # eo_start_date = models.DateField(default=datetime.now())    
    # eo_end_date = models.DateField(default=datetime.now())
    add_event_occurence_object(request, data, event_type, startDate, repeat) 