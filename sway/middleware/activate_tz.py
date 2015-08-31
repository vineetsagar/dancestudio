import pytz

from django.utils import timezone

class ActivateTimeZone(object):

    def process_request(self, request):
        #tzname = request.session.get('django_timezone')
        tzname = 'Asia/Calcutta'
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
