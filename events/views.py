from .util import events_to_json
from events.models import EventCalPage
from django.http import HttpResponse

from .forms import ParticipationForm
from .forms import Participation2Form
from .models import Participation
from .models import Instrument
from .models import InstrumentEventPage


from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from wagtail.core.models import Page
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.template.loader import render_to_string

from django.db.models import  Q, Count


class ParticipationCreateView(BSModalCreateView):
    template_name = 'home/create_participation.html'
    form_class = ParticipationForm
    success_message = 'Inscription enregistrée, merci !'
    success_url = '/privé/calendrier'

    def form_valid(self, form):
            form.instance.user = self.request.user
            eventid = self.kwargs['eventid']
            event_name = get_object_or_404(Page, slug=eventid)
            #suppression des anciennes inscriptions du même utilisateur pour le même événement
            oldparticipations = Participation.objects.filter(event_page=event_name, user=self.request.user)
            oldparticipations.delete()
            form.instance.event_page = event_name
            return super().form_valid(form)

def events_json(request):
    # Get all events
    events = EventCalPage.objects.all()
    # Create the fullcalendar json events list
    return HttpResponse(events_to_json(events),content_type='application/json')

def participationajax_create(request, eventid):
    if request.method == 'POST':
        form = Participation2Form(eventid, request.POST)
    else:
        form = Participation2Form(eventid)
    return save_participationajax_form(request, form, eventid, 'events/includes/partial_participationajax_create.html')

def save_participationajax_form(request, form, eventid, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            #ajout du user au formulaire avant soumission
            form.instance.user = request.user
            #suppression des anciennes inscriptions du même utilisateur pour le même événement
            event = form.instance.event_page
            oldparticipations = Participation.objects.filter(event_page=event, user=request.user)
            oldparticipations.delete()
            form.save()
            data['form_is_valid'] = True
            participationajaxs = Participation.objects.filter(event_page=event)
            instrumentpresences = Instrument.objects.annotate(num_participations=Count('instrumentparticipations',filter=Q(instrumentparticipations__choice='OUI', instrumentparticipations__event_page=event)))
            presences = Participation.objects.filter(event_page=event, choice='OUI')
            absences = Participation.objects.filter(event_page=event, choice='NON')
            questions = Participation.objects.filter(event_page=event, choice='PEUT-ETRE')
            instrumentmaxs = InstrumentEventPage.objects.filter(page=event)
            data['html_participationajax_list'] = render_to_string('events/includes/partial_participationajax_list.html', {
'instrumentpresencesajax': instrumentpresences, 'presencesajax': presences, 'instrumentmaxsajax': instrumentmaxs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
