
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from rango.models import Members, Events, EventType, EventCategory, Instructors
from rango.storeevents import storeevents


def viewmembers(request):
	members = Members.objects.order_by('-id')[:10]
	context_dict = {'membersList': members}
	return render(request, 'rango/members.html', context_dict)

def viewevents(request):
	events = Events.objects.order_by('-id')[:10]
	context_dict = {'eventsList': events}
	return render(request, 'rango/events.html', context_dict)



def home(request):
	return render(request, 'rango/home.html')

def index(request):
	return render(request, 'rango/index.html')


def addmembers(request):
	return render(request, 'rango/add_members.html')

def savemembers(request):
	data = Members()
	data.first_name = request.POST.get("first_name")
	data.last_name = request.POST.get("last_name")
	data.email = request.POST.get("email")
	data.area = request.POST.get("address")
	Members.save(data)
	category_list = Members.objects.order_by('-id')[:10]
	context_dict = {'membersList': category_list}
	return render(request, 'rango/members.html', context_dict)	


def addevents(request):
	event_type = EventType.objects.order_by('-id')
	category_type = EventCategory.objects.order_by('-id')
	context_dict = {'eventList':event_type, 'categoryList':category_type}
	return render(request, 'rango/add_events.html', context_dict)

def saveevents(request):
	storeevents(request)
	# now redirect this request to events view
	return HttpResponseRedirect(reverse("events"))

def show_instructors(request):
	instructors = Instructors.objects.order_by('-id')[:10]
	context_dict = {'instructor_list': instructors}
	return render(request, 'rango/instructors.html', context_dict)

def add_instructor(request):
	return render(request, 'rango/add_instructor.html')

def save_instructor(request):
	data = Instructors()
	data.first_name = request.POST.get("first_name")
	data.last_name = request.POST.get("last_name")
	data.email = request.POST.get("email")
	data.contact_number = request.POST.get("contact_number")
	Instructors.save(data)
	instructor_list = Instructors.objects.order_by('-id')[:5]
	context_dict = {'instructor_list': instructor_list}
	return render(request, 'rango/instructors.html', context_dict)

def show_dashboard(request):
	'get the event based on the current user'
	'convert it into json fromat required to full calender'
	'render the page now'
	return render(request, 'rango/dashboard.html', None)

def get_events_json(request):
	'it will get the logged in customer events from DB'
	'it will use this data and convert into its equivalent json (keep check for no events)'
	'return the json feed for events'

	str_json='''[
					{
						"title": "All Day Event",
						"start": "new Date(y, m, 1)"
					},
					{
						"title": "Long Event",
						"start": "new Date(y, m, d-5)",
						"end": "new Date(y, m, d-2)"
					},
					{
						"id": "999",
						"title": "Repeating Event",
						"start": "new Date(y, m, d-3, 16, 0)",
						"allDay": "false"
					}
					]
				'''
	str_json_new='''[
  {
    "title": "Ceramics",
    "id": "821",
    "start": "2014-12-06 09:00:00",
    "end": "2014-11-06 10:30:00"
  },
  {
    "title": "Zippy",
    "id": "822",
    "start": "2014-11-13 10:00:00",
    "end": "2014-11-13 11:30:00"
  }
]'''
	lstEvents=list()
	json_data=json.dumps(str_json,ensure_ascii=False)
	json_data_new=json.dumps(str_json_new)
	print json_data
	'print str_json'
	print json_data_new
	'return HttpResponse(json_data, content_type="application/json")'
	return HttpResponse(json_data_new, content_type="application/json")
	'return HttpResponse(str_json, content_type="text/plain")'
