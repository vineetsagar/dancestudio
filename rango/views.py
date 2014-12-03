from django.shortcuts import render
from rango.models import Members, Events, EventType, Category, EventCategory, Instructors
from datetime import datetime

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
	data = Events()
	data.event_name = request.POST.get("event_name")
	event_type_name = request.POST.get("event_type_selected")
	eventType = EventType.objects.get(event_type_name=event_type_name )
	event_category_name = request.POST.get("event_category")
	eventCategory = EventCategory.objects.get(event_category_name=event_category_name )
	data.event_type_id =eventType
	data.event_category_id = eventCategory
	data.start_date = datetime.now()
	data.end_date= datetime.now()
	Events.save(data)
	events = Events.objects.order_by('-id')[:10]
	context_dict = {'eventsList': events}
	return render(request, 'rango/events.html', context_dict)	 

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