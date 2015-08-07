from sway.models import Lead,StudioUser
import datetime
from push_notifications.models import GCMDevice
from django.utils import dateformat

def followup_notification_job():
    print "Cronjob followup_notification_job starts"
    obj_curr_time=datetime.datetime.now()
    obj_curr_time = obj_curr_time.replace(second=0, microsecond=0)
    leads = Lead.objects.filter(nextFollowUpDate = obj_curr_time)
    print "Lead count with current time =",leads.count()
    for lead in leads:
        print "lead date time=",lead.nextFollowUpDate.strftime('%m/%d/%Y %H:%M:%S')
        studio=lead.studio
        id=studio.id
        #studioUser=StudioUser.objects.filter(studio_id=id)
        studio_user=StudioUser.objects.get(studio_id=id)
        curr_user=studio_user.user
                  
        #now find all the device registered for this user
        devices=GCMDevice.objects.filter(user=curr_user)
        if devices is not None and devices.count()>0:
            print "Sending followup reminder for ",lead.name
            #print "devices=",devices
            devices.send_message("Followup reminder for "+lead.name)
        else:
            print "Device not found for push notification. Possibly a website user only. User=",curr_user
            