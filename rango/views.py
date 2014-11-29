from django.shortcuts import render
from rango.models import Members

def index(request):
	category_list = Members.objects.order_by('-id')[:10]
	context_dict = {'membersList': category_list}
	return render(request, 'rango/index.html', context_dict)


def home(request):
	return render(request, 'rango/home.html')

def addmembers(request):
	return render(request, 'rango/add_members.html')

def savemembers(request):
	data = Members()
	data.first_name = request.POST.get("first_name")
	data.last_name = request.POST.get("last_name")
	data.email = request.POST.get("email")
	data.area = request.POST.get("address")
	Members.save(data)
	category_list = Members.objects.order_by('-id')[:5]
	context_dict = {'membersList': category_list}
	return render(request, 'rango/index.html', context_dict)	 