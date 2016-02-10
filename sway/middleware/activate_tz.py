from  pytz import datetime
import pytz

from django.utils import timezone

class ActivateTimeZone(object):

    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if hasattr(request,'user'):
        	if hasattr(request.user, 'studiouser'):
        		tzname = request.user.studiouser.studio_id.timezone
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
