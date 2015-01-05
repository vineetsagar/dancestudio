
import datetime
from dateutil.relativedelta import relativedelta
import json
import math

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from sway.events.event_forms_helper import getForm, getEventForm, \
	setFormDefaultCssAndPlaceHolder
from sway.forms import EventsForm
from sway.models import Members, Events, EventType, EventCategory, Instructors, Lead, LeadFollowUp
from sway.storeevents import storeevents, updateEvents


def addevents(request):
	if request.method =='GET':
		form = getForm()
		event_type = EventType.objects.order_by('-id')
		return render_to_response("sway/add_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))

def editevents(request):
	pId =  request.GET.get('id')
	event = Events.objects.get(pk=pId)
	#01/02/2015  -> in this format wanted
	#2015-01-06 --> actual
	event.start_date = datetime.datetime.strptime(str(event.start_date), '%Y-%m-%d').strftime('%m/%d/%y')
	event.end_date = datetime.datetime.strptime(str(event.end_date), '%Y-%m-%d').strftime('%m/%d/%y')
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
	members = Members.objects.order_by('-id')[:10]
	context_dict = {'membersList': members}
	return render(request, 'sway/members.html', context_dict)

def viewevents(request):
	events = Events.objects.order_by('-id')[:10]
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
	Members.save(data)
	category_list = Members.objects.order_by('-id')[:10]
	context_dict = {'membersList': category_list}
	return render(request, 'sway/members.html', context_dict)	

def saveevents(request):
	if request.method == "POST":
		form = EventsForm(request.POST)
		if form.is_valid():
			storeevents(request)
		else:
			print "invalid form"	
			event_type = EventType.objects.order_by('-id')
			setFormDefaultCssAndPlaceHolder(form)
			return render_to_response("sway/add_events.html", { "form": form,'eventList':event_type,}, context_instance=RequestContext(request))		
	# now redirect this request to events view
	return HttpResponseRedirect(reverse("events"))


def updateEvent(request):
	updateEvents(request)
	# now redirect this request to events view
	return HttpResponseRedirect(reverse("events"))

def show_instructors(request):
	instructors = Instructors.objects.order_by('-id')[:10]
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
	Instructors.save(data)
	instructor_list = Instructors.objects.order_by('-id')[:5]
	context_dict = {'instructor_list': instructor_list}
	return render(request, 'sway/instructors.html', context_dict)

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
	
	lst=[]
	allEvents = Events.objects.order_by('-id')
	
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
	leads = Lead.objects.order_by('-id')
	context_dict = {'enquiryList': leads}
	return render(request, 'sway/view_enquiries.html', context_dict)

def view_followups(request):
	followups = LeadFollowUp.objects.order_by('followed_date')
	context_dict = {'followups': followups}
	return render(request, 'sway/view_followups.html', context_dict)	

def save_enquiry(request):
		return render(request, 'sway/add_enquiry.html')	

