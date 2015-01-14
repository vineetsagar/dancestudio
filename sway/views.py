
import datetime
from dateutil.relativedelta import relativedelta
import json
import math

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from sway.events.event_forms_helper import getForm, getEventForm, setFormDefaultCssAndPlaceHolder
from sway.forms import EventsForm
from sway.forms import MemberForm, InstructorForm
from sway.models import Members, Events, EventType, EventCategory, Instructors, Lead, LeadFollowUp, \
    EventMembers, MembersView, EventOccurence
from sway.storeevents import storeevents, updateEvents


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
            print "Delete all three tables event, eventmembers,eventoccurence", deleteEvent
        else:
            print "valid event but event does not belong to logged in user studio"
    return HttpResponseRedirect(reverse("events"))
    
def addevents(request):
    if request.method =='GET':
        form = getForm()
        event_type = EventType.objects.order_by('-id')
        return render_to_response("sway/add_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))

def editevents(request, id=None):
    print "editevents is called"
    if id:
        print "editevents called  for edit id=" ,id
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
    category_type = EventCategory.objects.order_by('-id')
    form = getEventForm(event)
    context_dict = {'eventList':event_type, 'categoryList':category_type , 'form':form, 'event': event}
    return render(request, 'sway/edit_events.html', context_dict)

def loginAuth(request):
    print "request for authenticate"
    data={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (not user is None) and (user.is_active):
            login(request, user)
            data['success'] = "/sway/dashboard"
        else:
            data['error'] = "There was an error logging you in. Please Try again"
        print 'data ', data
        return HttpResponse(json.dumps(data), content_type="application/json")

def viewmembers(request):
    members = Members.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    context_dict = {'membersList': members}
    return render(request, 'sway/members.html', context_dict)

def search_member(request):
    searchStr = request.POST.get('searchStr')
    members = Members.objects.filter((Q(first_name__startswith=searchStr)|Q(last_name__startswith=searchStr)|Q(email__startswith=searchStr)|Q(area__startswith=searchStr)) &Q(studio = request.user.studiouser.studio_id) )
    context_dict = {'membersList': members}
    return render(request, 'sway/members.html', context_dict)

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

def viewevents(request):
    events = Events.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    event_type = EventType.objects.order_by('-id')
    category_type = EventCategory.objects.order_by('-id')
    context_dict = {'eventsList': events, 'eventList':event_type, 'categoryList':category_type}
    return render(request, 'sway/events.html', context_dict)

def home(request):
    return render(request, 'sway/index.html')

def index(request):
    return home(request)


def addmembers(request):
    return render(request, 'sway/add_members.html')

def savemembers(request):
    data = Members()
    data.first_name = request.POST.get("first_name")
    data.last_name = request.POST.get("last_name")
    data.email = request.POST.get("email")
    data.area = request.POST.get("address")
    studio_data=request.user.studiouser.studio_id
    data.studio =studio_data
    Members.save(data)
    #category_list = Members.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    #context_dict = {'membersList': category_list}
    #return render(request, 'sway/members.html', context_dict)
    return HttpResponseRedirect(reverse("members")) 

def saveevents(request):
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            storeevents(request)
        else:
            event_type = EventType.objects.order_by('-id')
            setFormDefaultCssAndPlaceHolder(form)
            return render_to_response("sway/add_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))        
    # now redirect this request to events view
    return HttpResponseRedirect(reverse("events"))


def updateEvent(request):
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            updateEvents(request)
        else:
            event_type = EventType.objects.order_by('-id')
            setFormDefaultCssAndPlaceHolder(form)
            return render_to_response("sway/edit_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))   
    # now redirect this request to events view
    return HttpResponseRedirect(reverse("events"))

def show_instructors(request):
    instructors = Instructors.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')[:10]
    context_dict = {'instructor_list': instructors}
    return render(request, 'sway/instructors.html', context_dict)

def search_instructor(request):
    searchStr = request.POST.get('searchStr')
    instructors = Instructors.objects.filter((Q(first_name__startswith=searchStr)|Q(last_name__startswith=searchStr)|Q(email__startswith=searchStr)|Q(contact_number__startswith=searchStr))&Q(studio = request.user.studiouser.studio_id))
    context_dict = {'instructor_list': instructors}
    return render(request, 'sway/instructors.html', context_dict)


def add_instructor(request):
    return render(request, 'sway/add_instructor.html')

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

def show_dashboard(request):
    'get the event based on the current user'
    'convert it into json fromat required to full calender'
    'render the page now'
    return render(request, 'sway/dashboard.html', None)

def onceEvents(event):
    dct_obj2={}
    id
    dct_obj2["id"]=event.id
    dct_obj2["title"]=event.event_name.encode("ascii", "ignore")
    dct_obj2["start"]=datetime.datetime.combine(event.start_date,event.start_time).strftime("%Y-%m-%d %H:%M")
    dct_obj2["end"]=datetime.datetime.combine(event.end_date, event.start_time).strftime("%Y-%m-%d %H:%M")  
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

def get_events_json(request):
    'it will get the logged in customer events from DB'
    'it will use this data and convert into its equivalent json (keep check for no events)'
    'return the json feed for events'
    paramStartDate =    datetime.datetime.strptime(request.GET.get("start"), "%Y-%m-%d")
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
                    while (todaysDate <= p_end_date):
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
    print "final json is ----------->",events_json
    return HttpResponse(events_json, content_type="application/json")

def view_enquiries(request):
    leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('-id')
    paginator = Paginator(leads, 1,0,True) # Show 10 leads per page
    page = request.GET.get('page')
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        leads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        leads = paginator.page(paginator.num_pages)

    return render_to_response('sway/view_enquiries.html', {"enquiryList": leads})


def add_lead(request):
    return render(request, 'sway/add_enquiry.html', None)

def view_followups(request):
    leadId = request.GET.get('lead')
    followups = LeadFollowUp.objects.filter(lead=leadId)
    context_dict = {'followups': followups,'lead':leadId}
    return render(request, 'sway/view_followups.html', context_dict)    

def save_enquiry(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    contact = request.POST.get('contact') 
    lead = Lead(name=name,mobile=phone,email=email,contact_detail=contact,studio=request.user.studiouser.studio_id)
    lead.save();
    return HttpResponseRedirect("/sway/enquiries")

def followup(request):
    context_dict = {'lead': request.GET.get('lead')}
    return render(request, 'sway/add_followup.html', context_dict)

def save_followup(request):
    notes = request.POST.get('notes')
    lead = Lead.objects.filter(id=request.POST.get('lead'))[0]
    followup = LeadFollowUp(notes=notes,followed_by=request.user,lead=lead)
    followup.save();
    redirectString = '/sway/followups?lead='+request.POST.get('lead')
    return HttpResponseRedirect(redirectString) 

def search_enquiry(request):
    searchStr = request.POST.get('searchStr')
    leads = Lead.objects.filter((Q(name__startswith=searchStr)|Q(contact_detail__startswith=searchStr)|Q(email__startswith=searchStr)|Q(mobile__startswith=searchStr))&Q(studio = request.user.studiouser.studio_id))
    context_dict = {'enquiryList': leads}
    return render(request, 'sway/view_enquiries.html', context_dict)

def member_edit(request, id=None):
    print "member_edit is called"
    if id:
        print "member_edit called  for edit id=" ,id
        member=get_object_or_404(Members,pk=id)
        
    else:
        print "member_edit called  for new member"
        member=Members()
        '''member=Members(user=request.user)'''
    
    print "member_edit"        
    if request.POST:
        print "member_edit POST request"
        form=MemberForm(request.POST,instance=member)
        print form.is_valid(), form.errors, type(form.errors)
        if form.is_valid():
            print "MemberForm is valid"
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.save()
            return HttpResponseRedirect("/sway/members")
        else:
            print "MemberForm is invalid"
    else:
        print "member_edit GET request"
        form=MemberForm(instance=member)
                        
    return render(request, 'sway/add_members.html', {'form': form, 'id':member.id})

def member_delete(request, id):
    print "member_delete is called"
    member_to_delete=get_object_or_404(Members,pk=id)
    member_to_delete.delete()
    return HttpResponseRedirect("/sway/members")
    

def instructor_edit(request, id=None):
    print "instructor_edit is called"
    if id:
        print "instructor_edit called  for edit id=" ,id
        instructor=get_object_or_404(Instructors,pk=id)
        
    else:
        print "instructor_edit called  for new instructor"
        instructor=Instructors()
            
    if request.POST:
        print "instructor_edit POST request"
        form=InstructorForm(request.POST,instance=instructor)
        print form.is_valid(), form.errors, type(form.errors)
        if form.is_valid():
            print "InstructorForm is valid"
            post = form.save(commit=False)
            post.studio = request.user.studiouser.studio_id
            post.save()
            return HttpResponseRedirect("/sway/instructors")
        else:
            print "InstructorForm is invalid"
    else:
        print "instrcutor_edit GET request"
        form=InstructorForm(instance=instructor)
                        
    return render(request, 'sway/add_instructor.html', {'form': form, 'id':instructor.id})

def instructor_delete(request, id):
    print "member_delete is called"
    instructor_to_delete=get_object_or_404(Instructors,pk=id)
    instructor_to_delete.delete()
    return HttpResponseRedirect("/sway/instructors")
    
