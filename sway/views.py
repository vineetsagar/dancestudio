
import datetime
from dateutil.relativedelta import relativedelta
import json
import math

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from sway.events.event_forms_helper import getForm, getEventForm, setFormDefaultCssAndPlaceHolder
from sway.forms import EventsForm, EventCategoryForm, EventLocationForm
from sway.forms import MemberForm, InstructorForm, LeadForm, FollowupForm
from sway.models import Members, Events, EventType, EventCategory, Instructors, Lead, LeadFollowUp, \
    EventMembers, MembersView, EventOccurence, ProductContacts, EventLocations
from sway.storeevents import storeevents, updateEvents


@login_required
def delete_events(request, id):
    if request.method =='GET':
        #deleteEvent = get_object_or_404(Events,pk=id)
        deleteEvent = Events.objects.get(pk=id)

        studio_id = request.user.studiouser.studio_id
        if deleteEvent.studio ==studio_id:

            # check that event belong to logged in user only
            EventOccurence.objects.filter(events = deleteEvent).delete()
            EventMembers.objects.filter(event = deleteEvent).delete()
            deleteEvent.delete()
        else:
            print "valid event but event does not belong to logged in user studio"
    return HttpResponseRedirect(reverse("events"))
    
@login_required
def addevents(request):
    if request.method =='GET':
        form = getForm(request)
        event_type = EventType.objects.order_by('-id')
        return render_to_response("sway/add_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))

@login_required
def editevents(request, id=None):
    if id:
        event=get_object_or_404(Events,pk=id)
        print event
    event = Events.objects.get(pk=id)
    #01/02/2015  -> in this format wanted
    #2015-01-06 --> actual
    event.start_date = datetime.datetime.strptime(str(event.start_date), '%Y-%m-%d').strftime('%m/%d/%Y')
    event.end_date = datetime.datetime.strptime(str(event.end_date), '%Y-%m-%d').strftime('%m/%d/%Y')
    event.start_time =event.start_time.strftime('%H:%M')
    event.end_time =event.end_time.strftime('%H:%M')
    
    event_type = EventType.objects.order_by('-id')
    category_type = EventCategory.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')
    if category_type is None:
        context_dict = {'error': 'Looks no category you have not defined any category, please go to settings and create few categories.'}
        return render(request, 'sway/error.html', context_dict)
    form = getEventForm(request, event)
    context_dict = {'eventList':event_type, 'categoryList':category_type , 'form':form, 'event': event}
    return render(request, 'sway/edit_events.html', context_dict)

def loginAuth(request):
    data={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (not user is None) and (user.is_active):
            login(request, user)
            #request.session['alertsCount'] = '1';
            data['success'] = "/sway/dashboard"
        else:
            data['error'] = "There was an error logging you in. Please Try again"
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def viewmembers(request):
    members = Members.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    paginator = Paginator(members, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        members = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        members = paginator.page(paginator.num_pages)
    context_dict = {'membersList': members}
    getAlerts(request)
    return render_to_response('sway/members.html', context_dict, context_instance=RequestContext(request))

def getAlerts(request):
    from datetime import timedelta
    start_date=datetime.date.today();
    end_date = start_date + datetime.timedelta(days=5)
    leads = Lead.objects.filter(studio = request.user.studiouser.studio_id, nextFollowUpDate__gte=start_date,nextFollowUpDate__lte=end_date).count()
    print leads
    request.session['alertsCount'] = leads;

@login_required
def search_member(request):
    searchStr = request.POST.get('searchStr')
    members = Members.objects.filter((Q(first_name__icontains=searchStr)|Q(last_name__icontains=searchStr)|Q(email__icontains=searchStr)|Q(area__icontains=searchStr)) &Q(studio = request.user.studiouser.studio_id) )
    paginator = Paginator(members, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        members = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        members = paginator.page(paginator.num_pages)
    context_dict = {'membersList': members}
    return render(request, 'sway/members.html', context_dict, context_instance=RequestContext(request))

@login_required
def view_eventmembers(request, id = None):
    print "view_eventmembers is called"
    if id:
        print "view_eventmembers called  for edit id=" ,id
        event=get_object_or_404(Events,pk=id)
        print event
    
    eventObj = Events.objects.get(pk=id)
    allMembers = Members.objects.filter(Q(studio = request.user.studiouser.studio_id))
    selected_members = EventMembers.objects.filter(Q(event=eventObj)).prefetch_related('member')
    membersList = []
    for em in selected_members:
        membersList.append(em.member)
        
    toReturn  = []    
    for members in allMembers:
        if members in membersList:
            toSend = MembersView(member = members, selected = True)
            toReturn.append(toSend)
        else:
            toSend = MembersView(member = members, selected = False)
            toReturn.append(toSend)
        
    if allMembers.count() <=0:
        print "exception"
    context_dict = {'allMembers': toReturn, 'event_id':eventObj.id}
    return render(request, 'sway/members_events.html', context_dict)

@login_required
def save_eventmembers(request):
    selected_members_id_arrays = request.POST.getlist("dual_box_name")
    event_id = request.POST.get("event_id")
    #allMembers = Members.objects.filter(Q(studio = request.user.studiouser.studio_id))
    event_object = Events.objects.get(pk=event_id)
    print selected_members_id_arrays , event_id
    for member_id in selected_members_id_arrays:
        members = Members.objects.get(pk=member_id)
        eventMembers = EventMembers(event=event_object, member = members)
        eventMembers.save()
         
    return HttpResponseRedirect(reverse("events"))


@login_required
def view_locations(request):
    locations = EventLocations.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    paginator = Paginator(locations, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        locations = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        locations = paginator.page(paginator.num_pages)
    context_dict = {'locationsList': locations}
    return render_to_response('sway/view_locations.html', context_dict, context_instance=RequestContext(request))

@login_required
def view_categories(request):
    categories = EventCategory.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    paginator = Paginator(categories, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)
    context_dict = {'categoriesList': categories}
    return render_to_response('sway/view_categories.html', context_dict, context_instance=RequestContext(request))

def save_contact(request):
    data={}
    name = request.POST.get("name")
    if name is None or name == 'Your name':
        data['error'] = "Please provide name." 
    email = request.POST.get("email")
    message = request.POST.get("message")
    
    if email is None :
        data['error'] = "Please provide email." 
    elif message is None or message == 'Your message':
        data['error'] = "Please provide message."
    elif len(message) > 1024:
        data['error'] = "Your message length has exceed 1024 character limit."
    
    if len(data) > 0:
        data['error'] = "<li class='fa fa-cross fa-3x' style='color:red'></li>" + data['error'] +" "
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    contacts = ProductContacts()
    contacts.name = name
    contacts.email = email
    contacts.message = message
    contacts.save()
    
    data['success'] = "<li class='fa fa-check-circle fa-3x' style='color:green'></li> Thank you for contact us, we will contact you soon."
    return HttpResponse(json.dumps(data), content_type="application/json")
    

@login_required
def viewevents(request):
    events = Events.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    event_type = EventType.objects.order_by('-id')
    category_type = EventCategory.objects.order_by('-id')
    paginator = Paginator(events, 5,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    context_dict = {'eventsList': events, 'eventList':event_type, 'categoryList':category_type}
    return render_to_response('sway/events.html', context_dict, context_instance=RequestContext(request))

def home(request):
    return render(request, 'sway/index.html')

def index(request):
    return home(request)

@login_required
def addmembers(request):
    return render(request, 'sway/add_members.html')

@login_required
def savemembers(request):
    data = Members()
    data.first_name = request.POST.get("first_name")
    data.last_name = request.POST.get("last_name")
    data.email = request.POST.get("email")
    data.area = request.POST.get("address")
    data.gender = request.POST.get("gender")
    studio_data=request.user.studiouser.studio_id
    data.studio =studio_data
    Members.save(data)
    #category_list = Members.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    #context_dict = {'membersList': category_list}
    #return render(request, 'sway/members.html', context_dict)
    return HttpResponseRedirect(reverse("members")) 

@login_required
def saveevents(request):
    if request.method == "POST":
        form = EventsForm(request, request.POST)
        if form.is_valid():
            storeevents(request)
        else:
            event_type = EventType.objects.order_by('-id')
            setFormDefaultCssAndPlaceHolder(form)
            return render_to_response("sway/add_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))        
    # now redirect this request to events view
    return HttpResponseRedirect(reverse("events"))

@login_required
def updateEvent(request):
    if request.method == "POST":
        form = EventsForm(request, request.POST)
        if form.is_valid():
            updateEvents(request)
        else:
            event_type = EventType.objects.order_by('-id')
            setFormDefaultCssAndPlaceHolder(form)
            return render_to_response("sway/edit_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))   
    # now redirect this request to events view
    return HttpResponseRedirect(reverse("events"))

@login_required
def show_instructors(request):
    instructors = Instructors.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    paginator = Paginator(instructors, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        instructors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        instructors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        instructors = paginator.page(paginator.num_pages)
    context_dict = {'instructor_list': instructors}
    return render_to_response( 'sway/instructors.html', context_dict, context_instance=RequestContext(request))

@login_required
def search_instructor(request):
    searchStr = request.POST.get('searchStr')
    instructors = Instructors.objects.filter((Q(first_name__icontains=searchStr)|Q(last_name__icontains=searchStr)|Q(email__icontains=searchStr)|Q(contact_number__icontains=searchStr))&Q(studio = request.user.studiouser.studio_id))
    paginator = Paginator(instructors, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        instructors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        instructors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        instructors = paginator.page(paginator.num_pages)
    context_dict = {'instructor_list': instructors}
    return render_to_response( 'sway/instructors.html', context_dict, context_instance=RequestContext(request))

@login_required
def search_events(request):
    searchStr = request.POST.get('searchStr')
    events = Events.objects.filter((Q(event_name__icontains=searchStr))&Q(studio = request.user.studiouser.studio_id))
    paginator = Paginator(events, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    
    event_type = EventType.objects.order_by('-id')
    category_type = EventCategory.objects.order_by('-id')
    context_dict = {'eventsList': events, 'eventList':event_type, 'categoryList':category_type}
    return render_to_response( 'sway/events.html', context_dict, context_instance=RequestContext(request))

@login_required
def add_instructor(request):
    return render(request, 'sway/add_instructor.html')

@login_required
def add_edit_locations(request, id=None):
    if id:
        event_location=get_object_or_404(EventLocations,pk=id)
    else:
        event_location=EventLocations()
    if request.POST:
        form = EventLocationForm(request.POST, instance=event_location)
        print form.is_valid()
        if form.is_valid():
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.save()
            return HttpResponseRedirect("/sway/locations")
        else:
            print "Location form is invalid"
    else:
        form=EventLocationForm( instance=event_location)
    return render(request, 'sway/add_locations.html', {'form': form, 'id':event_location.id}, context_instance=RequestContext(request))


@login_required
def add_edit_categories(request, id=None):
    if id:
        event_category=get_object_or_404(EventCategory,pk=id)
    else:
        event_category=EventCategory()
    if request.POST:
        form= EventCategoryForm(request.POST, instance=event_category)
        print form.is_valid()
        if form.is_valid():
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.save()
            return HttpResponseRedirect("/sway/categories")
        else:
            print "Category form is invalid"
    else:
        form=EventCategoryForm( instance= event_category)
    return render(request, 'sway/add_categories.html', {'form': form, 'id':event_category.id}, context_instance=RequestContext(request))

@login_required
def save_instructor(request):
    data = Instructors()
    data.first_name = request.POST.get("first_name")
    data.last_name = request.POST.get("last_name")
    data.email = request.POST.get("email")
    data.contact_number = request.POST.get("contact_number")
    studio_data=request.user.studiouser.studio_id
    data.studio =studio_data
    Instructors.save(data)
    return HttpResponseRedirect(reverse("instructors"))

@login_required
def show_dashboard(request):
    'get the event based on the current user'
    'convert it into json fromat required to full calender'
    'render the page now'
    return render(request, 'sway/dashboard.html', None)
    
    
@login_required
def show_settings(request):
    return HttpResponseRedirect(reverse("view_categories"))

def onceEvents(event):
    dct_obj2={}
    dct_obj2["id"]=event.id
    dct_obj2["title"]=event.event_name.encode("ascii", "ignore")
    dct_obj2["start"]=datetime.datetime.combine(event.start_date,event.start_time).strftime("%Y-%m-%d %H:%M")
    # adding +1 day to end date so that full calender can render this event correctly
    if event.all_day:
        dct_obj2["end"]=(datetime.datetime.combine(event.end_date, event.start_time) + relativedelta(days=1) ).strftime("%Y-%m-%d %H:%M")
    else:
        dct_obj2["end"]=(datetime.datetime.combine(event.end_date, event.start_time) ).strftime("%Y-%m-%d %H:%M")  
    dct_obj2["allDay"]=event.all_day
    return dct_obj2


def otherEvents(event, todaysDate):
    dct_obj2={}
    dct_obj2["id"]=event.id
    dct_obj2["title"]=event.event_name.encode("ascii", "ignore")
    dct_obj2["start"]=datetime.datetime.combine(todaysDate,event.start_time).strftime("%Y-%m-%d %H:%M")
    dct_obj2["end"]=datetime.datetime.combine(todaysDate,event.end_time).strftime("%Y-%m-%d %H:%M")
    dct_obj2["allDay"]=event.all_day
    return dct_obj2


def leftSide(p_start_date, p_end_date, e_start_date, e_end_date):
    return p_start_date < e_start_date and p_end_date > e_start_date and p_end_date < e_end_date


def fullyCollapsed(p_start_date, p_end_date, e_start_date, e_end_date):
    return p_start_date <= e_start_date and p_end_date >= e_end_date


def rightSide(p_start_date, p_end_date, e_start_date, e_end_date):
    return p_start_date > e_start_date and p_end_date > e_end_date


def isEventOnForWeekDay(wmdValue, dayValue):
    # 2 == Mon
    # 3 == Tue
    # 4 == Wed
    # 5 == Thursday
    # 6 == Friday
    # 7 == Sat
    # 8 == Sun
    value = False
    if dayValue == 0:
        value = (wmdValue & int(math.pow( 2, 2 )) ) == (int(math.pow( 2, 2 )))
    if dayValue == 1:
        value = (wmdValue & int(math.pow( 2, 3 ) )) == (int(math.pow( 2, 3 )))
    if dayValue == 2:
        value = (wmdValue & int(math.pow( 2, 4 )) ) == (int(math.pow( 2, 4 )))
    if dayValue == 3:
        value = (wmdValue & int(math.pow( 2, 5) ) ) == (int(math.pow( 2, 5 )))
    if dayValue == 4:
        value = (wmdValue & int(math.pow( 2, 6 )) ) == (int(math.pow( 2, 6 )))
    if dayValue == 5:
        value = (wmdValue & int(math.pow( 2, 7 )) ) == (int(math.pow( 2, 7 )))
    if dayValue == 6:
        value = (wmdValue & int(math.pow( 2, 8 )) ) == (int(math.pow( 2, 8 )))
    return value

@login_required
def get_events_json(request):
    'it will get the logged in customer events from DB'
    'it will use this data and convert into its equivalent json (keep check for no events)'
    'return the json feed for events'
    start = request.GET.get("start")
    paramStartDate =    datetime.datetime.strptime(start, "%Y-%m-%d")
    paramEndDate =    datetime.datetime.strptime(request.GET.get("end"), "%Y-%m-%d")
    p_start_date =  paramStartDate.replace(hour=0, minute=0, second=0, microsecond=0)
    p_end_date =  paramEndDate.replace(hour=0, minute=0, second=0, microsecond=0)
    print "id value" , 
    lst=[]
    allEvents = Events.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')
    print allEvents
    
    # need to change event_type_id direct mapping with id, rather we should equate it on basis of its name
    for event in allEvents:
            # there can be 3 cases 
            #  CASE 1 event partially collapsed (LEFT SIDE) with passed date range
            #  CASE 2 event partially collapsed (RIGHT SIDE) with passed date range
            #  CASE 3 event fully collapsed  with passed date range
                
            if event.event_type_id == 1:
                lst.append(onceEvents(event))
            elif event.event_type_id==2:
                #  we need to handle three cases here of end_date
                # wmd , first bit value should be on i.e wmd ==1
                eventOccurenceValue  = event.eventoccurence
                startDate = datetime.datetime.strptime(str(eventOccurenceValue.eo_start_date), "%Y-%m-%d")
                endDate = datetime.datetime.strptime(str(eventOccurenceValue.eo_end_date), "%Y-%m-%d")
                e_start_date = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
                e_end_date = endDate.replace(hour=0, minute=0, second=0, microsecond=0)
                
                if (leftSide(p_start_date, p_end_date, e_start_date, e_end_date)):
                    # CASE 1
                    todaysDate = e_start_date
                    while (todaysDate <= p_end_date):
                        ## add a event here 
                        lst.append(otherEvents(event, todaysDate))
                        todaysDate = todaysDate+ relativedelta(days=1)
                        print todaysDate
                elif (fullyCollapsed(p_start_date, p_end_date, e_start_date, e_end_date) ):
                    #CASE 3
                    todaysDate = e_start_date
                    while (todaysDate <= e_end_date and todaysDate <= p_end_date):
                        ## add a event here 
                        lst.append(otherEvents(event, todaysDate))
                        todaysDate = todaysDate+ relativedelta(days=1)
                elif(rightSide(p_start_date, p_end_date, e_start_date, e_end_date)):
                    #CASE 2
                    todaysDate = p_start_date
                    while (todaysDate <= e_end_date):
                        ## add a event here 
                        lst.append(otherEvents(event, todaysDate))
                        todaysDate = todaysDate+ relativedelta(days=1)
            elif event.event_type_id ==3:
                eventOccurenceValue  = event.eventoccurence
                event_occ_wmd = eventOccurenceValue.wmd
                startDate = datetime.datetime.strptime(str(eventOccurenceValue.eo_start_date), "%Y-%m-%d")
                endDate = datetime.datetime.strptime(str(eventOccurenceValue.eo_end_date), "%Y-%m-%d")
                e_start_date = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
                e_end_date = endDate.replace(hour=0, minute=0, second=0, microsecond=0)
                
                # we need to find out on which days this event has been on
                # 0 is monday and 6 is sunday
                todaysDate = e_start_date
                if (leftSide(p_start_date, p_end_date, e_start_date, e_end_date)):
                    # CASE 1
                    todaysDate = e_start_date
                    while (todaysDate <= p_end_date):
                        ## add a event here 
                        if(isEventOnForWeekDay(event_occ_wmd, todaysDate.weekday())):
                            lst.append(otherEvents(event, todaysDate))
                        todaysDate = todaysDate+ relativedelta(days=1)
                elif (fullyCollapsed(p_start_date, p_end_date, e_start_date, e_end_date) ):
                    #CASE 3
                    todaysDate = e_start_date
                    while (todaysDate <= e_end_date and todaysDate <= p_end_date):
                        ## add a event here 
                        if(isEventOnForWeekDay(event_occ_wmd, todaysDate.weekday())):
                            lst.append(otherEvents(event, todaysDate))
                        todaysDate = todaysDate+ relativedelta(days=1)
                elif(rightSide(p_start_date, p_end_date, e_start_date, e_end_date)):
                    #CASE 2
                    todaysDate = p_start_date
                    while (todaysDate <= p_end_date):
                        ## add a event here 
                        if(isEventOnForWeekDay(event_occ_wmd, todaysDate.weekday())):
                            lst.append(otherEvents(event, todaysDate))
                        todaysDate = todaysDate+ relativedelta(days=1)
            elif event.event_type_id ==4:
                print("Monthly Event")
    
    
    
    events_json=json.dumps(lst)
    #print "final json is ----------->",events_json
    return HttpResponse(events_json, content_type="application/json")

@login_required
def view_enquiries(request):
    leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id)).exclude(status=1).order_by('-nextFollowUpDate','-status')
    paginator = Paginator(leads, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        leads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        leads = paginator.page(paginator.num_pages)
    print leads

    return render_to_response('sway/view_enquiries.html', {"enquiryList": leads}, context_instance=RequestContext(request))


@login_required
def add_lead(request):
    form = LeadForm()
    return render_to_response('sway/add_enquiry.html', { "form": form}, context_instance=RequestContext(request))

@login_required
def edit_lead(request,id=None):
    print 'In print lead '
    if id:
        lead=get_object_or_404(Lead,pk=id)
        print lead.name
    else:
        lead=Lead()
    if request.POST:
        print lead.created_date
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.created_date=lead.created_date 
            post.save()
            return HttpResponseRedirect("/sway/enquiries")
        else:
            print "Lead form is invalid"
    else:
        form=LeadForm( instance=lead)
    return render(request, 'sway/add_enquiry.html', {'form': form, 'id':lead.id}, context_instance=RequestContext(request))
    

@login_required
def view_followups(request):
    leadId = request.GET.get('lead')
    followups = LeadFollowUp.objects.filter(lead=leadId)
    leadObj = Lead.objects.get(id=request.GET.get('lead'));
    context_dict = {'followups': followups,'lead':leadId,"leadObj":leadObj}
    return render(request, 'sway/view_followups.html', context_dict)    

@login_required
def save_enquiry(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('mobile')
    contact = request.POST.get('contact_detail') 
    inquiryFor = request.POST.get('inquiryFor') 
    short_description = request.POST.get('short_description')
    lead = Lead(name=name,mobile=phone,email=email,contact_detail=contact,inquiryFor=inquiryFor,studio=request.user.studiouser.studio_id, short_description = short_description)
    lead.save();
    return HttpResponseRedirect("/sway/enquiries")

@login_required
def followup(request):
    form = FollowupForm()
    leadObj = Lead.objects.get(id=request.GET.get('lead'));
    return render_to_response('sway/add_followup.html', { "form": form,'lead': request.GET.get('lead'),"leadObj":leadObj}, context_instance=RequestContext(request))
    

@login_required
def save_followup(request):
    notes = request.POST.get('notes')
    lead = Lead.objects.filter(id=request.POST.get('lead'))[0]
    followup = LeadFollowUp(notes=notes,followed_by=request.user,lead=lead)
    followup.save()
    from datetime import datetime
    lead.nextFollowUpDate = datetime.strptime(request.POST.get('nextFollowupDate'),'%m/%d/%Y %H:%M %p')
    lead.save()
    getAlerts(request);
    redirectString = '/sway/followups?lead='+request.POST.get('lead')
    return HttpResponseRedirect(redirectString) 

@login_required
def search_enquiry(request):
    searchStr = request.POST.get('searchStr')
    leads = Lead.objects.filter((Q(name__icontains=searchStr)|Q(contact_detail__icontains=searchStr)|Q(email__icontains=searchStr)|Q(mobile__icontains=searchStr))&Q(studio = request.user.studiouser.studio_id))
    context_dict = {'enquiryList': leads}
    return render(request, 'sway/view_enquiries.html', context_dict, context_instance=RequestContext(request))

@login_required
def member_edit(request, id=None):
    if id:
        member=get_object_or_404(Members,pk=id)
    else:
        member=Members()
    if request.POST:
        form=MemberForm(request.POST,instance=member)
        print form.is_valid(), form.errors, type(form.errors)
        if form.is_valid():
            print "MemberForm is valid"
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.created_by = request.user
            post.modified_by = request.user
            if id:
                post.modified_date = datetime.datetime.now()   
            else:
                post.created_date = datetime.datetime.now()
            post.save()
            return HttpResponseRedirect("/sway/members")
        else:
            print "MemberForm is invalid"
    else:
        print "member_edit GET request"
        form=MemberForm(instance=member)
                        
    return render(request, 'sway/add_members.html', {'form': form, 'id':member.id}, context_instance=RequestContext(request))

@login_required
def member_delete(request, id):
    member_to_delete=get_object_or_404(Members,pk=id)
    member_to_delete.delete()
    return HttpResponseRedirect("/sway/members")

@login_required
def category_delete(request, id):
    member_to_delete=get_object_or_404(EventCategory,pk=id)
    member_to_delete.delete()
    return HttpResponseRedirect("/sway/categories")
    
@login_required
def instructor_edit(request, id=None):
    if id:
        print "instructor_edit called  for edit id=" ,id
        instructor=get_object_or_404(Instructors,pk=id)
        
    else:
        instructor=Instructors()
            
    if request.POST:
        form=InstructorForm(request.POST,instance=instructor)
        print form.is_valid(), form.errors, type(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.save()
            return HttpResponseRedirect("/sway/instructors")
        else:
            print "InstructorForm is invalid"
    else:
        form=InstructorForm(instance=instructor)
                        
    return render(request, 'sway/add_instructor.html', {'form': form, 'id':instructor.id})


@login_required
def instructor_delete(request, id):
    instructor_to_delete=get_object_or_404(Instructors,pk=id)
    instructor_to_delete.delete()
    return HttpResponseRedirect("/sway/instructors")

@login_required
def alerts(request):
    from datetime import timedelta
    start_date=datetime.date.today();
    end_date = start_date + datetime.timedelta(days=5)
    leads = Lead.objects.filter(studio = request.user.studiouser.studio_id, nextFollowUpDate__gte=start_date,nextFollowUpDate__lte=end_date).order_by('nextFollowUpDate')
    paginator = Paginator(leads, 10,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        leads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        leads = paginator.page(paginator.num_pages)

    return render_to_response('sway/view_enquiries.html', {"enquiryList": leads}, context_instance=RequestContext(request))

def forgotpassword(request):   
    return render(request, 'registration/forgotpassword.html', None)

def resetpassword(request):
    from django.core.mail import send_mail
    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import make_password
    user_name = request.POST.get('username')
    print user_name
    tgt_user = User.objects.get(username=user_name)
    if tgt_user is None:
        pass # return error message that user does not exist with username
    if not tgt_user.email:
        pass # return error message that email is not configured for user
    import uuid
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    raw_password = random[0:10]
    password = make_password(random[0:10]) # Return the random string.
    tgt_user.password = password
    tgt_user.save()
    send_mail('Password Reset','Your password is reset to '+raw_password+', use this password to login. Please modify password of your choice.','balwinder.mca@gmail.com',[tgt_user.email]) 
    return HttpResponseRedirect("/sway/login")

def change_password(request):
    from django.core.mail import send_mail
    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import make_password
    password = request.POST.get('password')
    tgt_user = User.objects.get(id=request.user.id)
    password = make_password(password) # Return the random string.
    tgt_user.password = password
    tgt_user.save()
    send_mail('Password Modified','Youhave modified your password to '+password+', use this password to login.','balwinder.mca@gmail.com',[tgt_user.email]) 
    return HttpResponseRedirect("/sway/login")
