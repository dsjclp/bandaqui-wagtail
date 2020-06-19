from .util import events_to_json
from events.models import EventCalPage
from django.http import HttpResponse

def events_json(request):
    # Get all events
    events = EventCalPage.objects.all()
    # Create the fullcalendar json events list
    return HttpResponse(events_to_json(events),content_type='application/json')
