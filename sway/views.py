
from datetime import date
import datetime
import json

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from sway.models import Members, Events, EventType, EventCategory, Instructors, EventOccurence
from sway.storeevents import storeevents


def viewmembers(request):
	members = Members.objects.order_by('-id')[:10]
	context_dict = {'membersList': members}
	return render(request, 'sway/members.html', context_dict)

def viewevents(request):
	events = Events.objects.order_by('-id')[:10]
	context_dict = {'eventsList': events}
	return render(request, 'sway/events.html', context_dict)


def home(request):
	return render(request, 'sway/home.html')

def index(request):
	return show_dashboard(request)


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


def addevents(request):
	event_type = EventType.objects.order_by('-id')
	category_type = EventCategory.objects.order_by('-id')
	context_dict = {'eventList':event_type, 'categoryList':category_type}
	return render(request, 'sway/add_events.html', context_dict)

def saveevents(request):
	storeevents(request)
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

def get_events_json(request):
	'it will get the logged in customer events from DB'
	'it will use this data and convert into its equivalent json (keep check for no events)'
	'return the json feed for events'
	paramStartDate =    datetime.datetime.strptime(request.GET.get("start"), "%Y-%m-%d")
   	paramEndDate =    datetime.datetime.strptime(request.GET.get("end"), "%Y-%m-%d")
	lst=[]
	allEvents = Events.objects.order_by('-id')
	
	for event in allEvents:
			if event.event_type_id == 1:
				dct_obj2={}
				dct_obj2["title"]=event.event_name.encode("ascii", "ignore")
				dct_obj2["start"]=datetime.datetime.combine(event.start_date,event.start_time).strftime("%Y-%m-%d %H:%M")
				dct_obj2["end"]=datetime.datetime.combine(event.end_date,event.end_time).strftime("%Y-%m-%d %H:%M")
				lst.append(dct_obj2)
			elif event.event_type_id==2:
				#  we need to handle three cases here of end_date
				# wmd , first bit value should be on i.e wmd ==1
				eventOccurenceValue  = event.eventoccurence
				startDate = datetime.datetime.strptime(str(eventOccurenceValue.eo_start_date), "%Y-%m-%d")
				endDate = datetime.datetime.strptime(str(eventOccurenceValue.eo_end_date), "%Y-%m-%d")
				print(eventOccurenceValue.eo_start_date)
				print(eventOccurenceValue.eo_end_date)
				
				# CASE 1 : if paramstartdate less than event startdate and paramenddate greater than startdate but less than or equal to event enddate
				# which implies it partialy match
				#handling case 1
				
				if (paramStartDate.replace(hour=0, minute=0, second=0, microsecond=0) <= startDate.replace(hour=0, minute=0, second=0, microsecond=0) and paramEndDate.replace(hour=0, minute=0, second=0, microsecond=0) > startDate.replace(hour=0, minute=0, second=0, microsecond=0) and paramEndDate.replace(hour=0, minute=0, second=0, microsecond=0) <= endDate.replace(hour=0, minute=0, second=0, microsecond=0)):
					print("Partial collapse left side")
				# CASE 2: if paramstartdate greater or equal to event startdate  
				elif (paramStartDate.replace(hour=0, minute=0, second=0, microsecond=0) >= startDate.replace(hour=0, minute=0, second=0, microsecond=0) and paramEndDate.replace(hour=0, minute=0, second=0, microsecond=0) <= endDate.replace(hour=0, minute=0, second=0, microsecond=0) ):
					print("Fully collapse or contain within event start-end period")
				elif(paramStartDate.replace(hour=0, minute=0, second=0, microsecond=0) >= startDate.replace(hour=0, minute=0, second=0, microsecond=0) and  paramEndDate.replace(hour=0, minute=0, second=0, microsecond=0) >= endDate.replace(hour=0, minute=0, second=0, microsecond=0)):
					print("Partially collapse right side")
					
			elif event.event_type_id ==3:
				print("Weekly Event")
			elif event.event_type_id ==4:
				print("Monthly Event")
	
	
	
	events_json=json.dumps(lst)
	print "final json is ----------->",events_json
	return HttpResponse(events_json, content_type="application/json")
