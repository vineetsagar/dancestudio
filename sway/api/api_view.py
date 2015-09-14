import datetime
from dateutil.relativedelta import relativedelta
import json
import math
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import http
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from sway.api.api_helper import get_token,byteify
from sway.api.api_helper import TokenAuthenticator
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from sway.api.serializers import LeadSerializer,FollowUpSerializer,UserSerializer,StudioSerializer,StudioUserSerializer
from django.db.transaction import commit
from sway.api.api_helper import JSONResponse
from sway.events.event_forms_helper import getForm, getEventForm, setFormDefaultCssAndPlaceHolder
from sway.forms import EventsForm, EventCategoryForm, EventLocationForm
from sway.forms import MemberForm, InstructorForm, LeadForm, FollowupForm
from sway.models import Members, Events, EventType, EventCategory, Instructors, Lead, LeadFollowUp, \
    EventMembers, MembersView, EventOccurence, ProductContacts, EventLocations
from sway.storeevents import storeevents, updateEvents
from push_notifications.models import GCMDevice


#REST API for mobile app
def api_app_login(request):
    print "loginApp is called", request.method
    if request.method == 'POST':
        msg=request.body;
        string_msg=msg.decode("utf-8")
        json_data=json.loads(string_msg);
        print "json_data=",json_data
        data=byteify(json_data)
        id = data["username"]
        pwd = data["password"]
        print "id=",id + "pwd=",pwd
        #user = authenticate(username="imran", password="welcome")
        user = authenticate(username=id, password=pwd)
        #objTokenAuth=TokenAuthentication()
        #user=objTokenAuth.authenticate(request)
        print "user=", user
        if (not user is None) and (user.is_active):
            token=get_token(user);
            print "token=",token
            #create json data with token response
            response_dict=dict();
            response_dict["token"]=token
            print "studio studio_id " ,user.studiouser.studio_id.id
            id=user.studiouser.studio_id.id
            print "stidio_id=",id
            response_dict["studio_id"]=id
            response_json=json.dumps(response_dict);
            response=http. HttpResponse(response_json, content_type="application/json")

        else:
            print "authentication failed";
            response=HttpResponseForbidden()

        return response;
        
@api_view(['GET',])
@authentication_classes((TokenAuthenticator,))
def api_validate_token(request):
    print "validateToken is called. Token is valid"
    response = http.HttpResponse("OK")
    return response;
   
@api_view(['GET'])
@authentication_classes((TokenAuthenticator,))
def api_lead_count_view(request, format=None):
    """
    A view that returns the count of active users in JSON.
    """
    print " api_lead_count_view search value", request.GET.get('search')
    searchStr = request.GET.get('search')
    lead_count = 0
    if searchStr is None or searchStr == 'null':
		lead_count = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id)).count()
    else:
    	lead_count = Lead.objects.filter((Q(name__icontains=searchStr)|Q(contact_detail__icontains=searchStr)|Q(email__icontains=searchStr)|Q(mobile__icontains=searchStr)|Q(inquiryFor__icontains=searchStr)) &Q(studio = request.user.studiouser.studio_id)).count()
    content = {'lead_count': lead_count}
    return Response(content)
    
@api_view(['GET',])
@authentication_classes((TokenAuthenticator,))
def api_single_lead(request):
    print "in request for getting lead followup data"
    if request.method =='GET':
        forLead = request.GET.get('lead_id')
        print "found for lead value " , forLead
        if forLead is not None:
            foundLead = get_object_or_404(Lead,pk=forLead)
            serializer = LeadSerializer(foundLead, many=False)
            return JSONResponse(serializer.data)


@api_view(['GET',])
@authentication_classes((TokenAuthenticator,))
def api_lead_list(request):
    print "in request for getting lead data search value", request.GET.get('search')
    print "_hot ", request.GET.get('hot')
    print "_warm ", request.GET.get('warm')
    print "_cold ", request.GET.get('cold')
    print "_dFilter ", request.GET.get('dFilter')
    if request.method == 'GET':
        searchStr = request.GET.get('search')
        hot = request.GET.get('hot')
        warm = request.GET.get('warm')
        cold = request.GET.get('cold')
        dFilter = request.GET.get('dFilter')

        if searchStr is None or searchStr == 'null' or searchStr =='':      
            leadList = []
            if hot is not None  and hot =='true': 
                # 3 cold, 4 warm ,5 hot
                leadList.append(5)
            if warm is not None and warm == 'true': 
                # 3 cold, 4 warm ,5 hot
                leadList.append(4)
            if cold is not None and cold =='true':
                # 3 cold, 4 warm ,5 hot
                leadList.append(3)
            end_date = ""
            if dFilter is not None and dFilter !='':
                 from datetime import timedelta
                 start_date=django.utils.timezone.now()
                 if dFilter == '2':
                    print "dfiler 2 get called"
                    end_date = start_date - datetime.timedelta(days=7)
                    print "after setting the value"
                 if dFilter == '3':
                    end_date = start_date - datetime.timedelta(days=14)
            if end_date !="":
                if len(leadList) > 0:
                    print "going to get the data now"
                    leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id) & Q(status__in=leadList) & Q(nextfollowupdate__gte=end_date)).order_by('nextfollowupdate')
                    print "after to get the data now"
                    serializer = LeadSerializer(leads, many=True)
                    return JSONResponse(serializer.data)    
                else:
                    print "before getting data"
                    leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id) & Q(nextfollowupdate__gte=end_date)).order_by('nextfollowupdate')
                    print "after getting data"
                    serializer = LeadSerializer(leads, many=True)
                    return JSONResponse(serializer.data)
            else:
                 if len(leadList) > 0:
                    leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id) & Q(status__in=leadList)).order_by('nextfollowupdate')
                    serializer = LeadSerializer(leads, many=True)
                    return JSONResponse(serializer.data)    
                 else:
                    leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('nextfollowupdate')
                    serializer = LeadSerializer(leads, many=True)
                    return JSONResponse(serializer.data)
           
        else:
            leads = Lead.objects.filter((Q(name__icontains=searchStr)|Q(contact_detail__icontains=searchStr)|Q(email__icontains=searchStr)|Q(mobile__icontains=searchStr)|Q(inquiryFor__icontains=searchStr)) &Q(studio = request.user.studiouser.studio_id)).order_by('nextfollowupdate')
            serializer = LeadSerializer(leads, many=True)
            return JSONResponse(serializer.data)

@api_view(['GET',])
@authentication_classes((TokenAuthenticator,))
def api_lead_list_temp(request):
    print "in request for getting lead data page value", request.GET.get('page')
    print "in request for getting lead data search value", request.GET.get('search')
    if request.method == 'GET':
    	searchStr = request.GET.get('search')
    	if searchStr is None or searchStr == 'null' or searchStr =='':
            leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id)).order_by('nextfollowupdate')
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
            serializer = LeadSerializer(leads, many=True)
            return JSONResponse(serializer.data)
    	else:
            leads = Lead.objects.filter((Q(name__icontains=searchStr)|Q(contact_detail__icontains=searchStr)|Q(email__icontains=searchStr)|Q(mobile__icontains=searchStr)|Q(inquiryFor__icontains=searchStr)) &Q(studio = request.user.studiouser.studio_id)).order_by('nextfollowupdate')
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
            serializer = LeadSerializer(leads, many=True)
            return JSONResponse(serializer.data)

def registration(request):
    data = JSONParser().parse(request)
    id = data["username"]
    print "username request", id
    # need to search that username is already exist
    userExist = User.objects.filter(Q(username=id))
    print "user found value is ", userExist
    if userExist is not None and len(userExist) != 0:
        # need to retrun a reponse that user already exist here
        print "User already exist hence returning the json response", id
        return JSONResponse("User " + id + " already exist " , status=422)
    if request.method == 'POST':
        print "inside registration"
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            print "inside valid user data"
            createdUser = serializer.save()
            studioName = data["first_name"] + " " +data["last_name"]
            studioData = {}
            studioData['name'] = studioName
            studioData["email"]= data["email"]
            studioData["mobile"] = data["mobile"]
            studioData["email_port"] = 0
            studioSerializer = StudioSerializer(data=studioData)
            if studioSerializer.is_valid():
                print "inside valid studio data"
                createdStudio = studioSerializer.save();
                ## now create mapping of studio and user
                studioUserData = {}
                studioUserData["user"] = createdUser.id
                studioUserData["studio_id"] = createdStudio.id
                print "studio user data value is", studioUserData
                studioUserSerializer = StudioUserSerializer(data=studioUserData)
                if studioUserSerializer.is_valid():
                    print "studio user data is valid"
                    studioUserSerializer.save();
                else:
                    print "invalid"
            # here we have to create a studio object
            # here we have to create a studio user mapping also
            return JSONResponse(serializer.data, status=200)
    return JSONResponse(serializer.errors, status=400) 

@api_view(['POST',])
@authentication_classes((TokenAuthenticator,))
def api_add_lead(request):
	data = JSONParser().parse(request)
	data['studio']=request.user.studiouser.studio_id.id
	serializer = LeadSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		return JSONResponse(serializer.data, status=200)
	return JSONResponse(serializer.errors, status=400)

@api_view(['POST',])
@authentication_classes((TokenAuthenticator,))
def api_edit_lead(request):
    data = JSONParser().parse(request)
    data['studio']=request.user.studiouser.studio_id.id
    id = data['id']
    print "id value is ", id , data['status']
    leadObject = Lead.objects.get(pk=id)
    print "lead object value is ", leadObject
    if leadObject is not None:
        serializer = LeadSerializer(leadObject, data=data)
        if serializer.is_valid():
            serializer.save()
            print serializer
            return JSONResponse(serializer.data, status=200)
    return JSONResponse(serializer.errors, status=400)

@api_view(['GET',])
@authentication_classes((TokenAuthenticator,))
def api_lead_delete(request, id):
    print "api_lead_delete is called"
    lead_to_delete=get_object_or_404(Lead,pk=id)
    lead_to_delete.delete()
    response = http.HttpResponse("OK")
    return response;

    
@api_view(['POST',])
@authentication_classes((TokenAuthenticator,))
def api_add_followup(request):
    data = JSONParser().parse(request)
    data['followed_by'] = request.user.id
    serializer = FollowUpSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # not we need to update the followeup_date for lead object
        lead = Lead.objects.filter(id=data["lead"])[0]
        from datetime import datetime
        from pytz import timezone
        lead.nextfollowupdate = datetime.strptime(data["followed_date"],'%m/%d/%Y %I:%M %p')
        lead.nextfollowupdate = lead.nextfollowupdate.replace(tzinfo=timezone(request.user.studiouser.studio_id.timezone))
        lead.save()
        return JSONResponse(serializer.data, status=200)
    else:
        print "data is not valid, hence returning", serializer.errors
    return JSONResponse(serializer.errors, status=400)

@api_view(['POST',])
@authentication_classes((TokenAuthenticator,))
def api_register_device_gcm(request):
    #it will register and save the device for push notification using google cloud messaging
    if request.method == 'POST':
        msg=request.body;
        string_msg=msg.decode("utf-8")
        json_data=json.loads(string_msg);
        print "json_data=",json_data
        data=byteify(json_data)
        device_name = data["device_name"]
        device_id = data["device_id"]
        reg_id = data["registration_id"]
        user=request.user
        print "user=",user
        #check if device is already registered If yes just update the entry else create a new entry
        device,created=GCMDevice.objects.get_or_create(name=device_name, user=user, registration_id=reg_id)
        print "device object=",device
        print "device created(true => new device)=",created
        device.save()
        #devices = GCMDevice.objects.filter(user=user)
        #devices.send_message("Device registered successfully for push notification ;) :)")
        response = http.HttpResponse("OK")
        return response;
   
    response = http.HttpResponse("ERROR")
    return response;
