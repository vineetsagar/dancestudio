from sway.models import Lead,StudioUser
import datetime
from push_notifications.models import GCMDevice
from django.utils import dateformat
from datetime import timedelta

def followup_notification_job():
    print "Cronjob followup_notification_job started"
    obj_curr_time=datetime.datetime.now()+timedelta(hours=5,minutes=30)
    obj_curr_time = obj_curr_time.replace(second=0, microsecond=0)
    print "Current Time after adding 5:30=",obj_curr_time.strftime('%m/%d/%Y %H:%M:%S')
    leads = Lead.objects.filter(nextfollowupdate = obj_curr_time)
    print "Lead count with current time =",leads.count()
    for lead in leads:
        print "lead value is " , lead
        print "lead date time=",lead.nextfollowupdate.strftime('%m/%d/%Y %H:%M:%S')
        studio=lead.studio
        print "studio" , studio
        id=studio.id
        print "id value is ", id
        #studioUser=StudioUser.objects.filter(studio_id=id)
        studio_user=StudioUser.objects.get(studio_id=id)
        print "studio_user" , studio_user
        curr_user=studio_user.user
        print "curr_user " , curr_user
        #now find all the device registered for this user
        devices=GCMDevice.objects.filter(user=curr_user)
        print "devices ", devices
        if devices is not None and devices.count()>0:
            print "Sending followup reminder for ",lead.name
            #print "devices=",devices
            devices.send_message("Followup reminder for "+lead.name)
        else:
            print "Device not found for push notification. Possibly a website user only. User=",curr_user
            