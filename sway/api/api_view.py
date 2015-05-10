import datetime
from dateutil.relativedelta import relativedelta
import json
import math

from django.contrib.auth import authenticate, login
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
from sway.api.serializers import LeadSerializer,FollowUpSerializer
from django.db.transaction import commit
from sway.api.api_helper import JSONResponse
from sway.events.event_forms_helper import getForm, getEventForm, setFormDefaultCssAndPlaceHolder
from sway.forms import EventsForm, EventCategoryForm, EventLocationForm
from sway.forms import MemberForm, InstructorForm, LeadForm, FollowupForm
from sway.models import Members, Events, EventType, EventCategory, Instructors, Lead, LeadFollowUp, \
    EventMembers, MembersView, EventOccurence, ProductContacts, EventLocations
from sway.storeevents import storeevents, updateEvents

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
def api_lead_list(request):
    print "in request for getting lead data page value", request.GET.get('page')
    print "in request for getting lead data search value", request.GET.get('search')
    if request.method == 'GET':
    	searchStr = request.GET.get('search')
    	if searchStr is None or searchStr == 'null':
            leads = Lead.objects.filter(Q(studio = request.user.studiouser.studio_id))
            paginator = Paginator(leads, 5,0,True) # Show 10 leads per page
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
    		leads = Lead.objects.filter((Q(name__icontains=searchStr)|Q(contact_detail__icontains=searchStr)|Q(email__icontains=searchStr)|Q(mobile__icontains=searchStr)|Q(inquiryFor__icontains=searchStr)) &Q(studio = request.user.studiouser.studio_id))
	    	paginator = Paginator(leads, 5,0,True) # Show 10 leads per page
	    	page = request.GET.get('page')
	    	try:
	        	leads = paginator.page(page)
	    	except PageNotAnInteger:
	        	# If page is not an integer, deliver first page.
	        	leads = paginator.page(1)
	    	except EmptyPage:
	        	# If page is out of range (e.g. 9999), deliver last page of results.
	        	leads = paginator.page(paginator.num_pages)
	    	print " inside the get lead call ", request.user.studiouser.studio_id
	        serializer = LeadSerializer(leads, many=True)
	        return JSONResponse(serializer.data)

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
    #data['studio']=request.user.studiouser.studio_id.id
    serializer = FollowUpSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=200)

    return JSONResponse(serializer.errors, status=400)