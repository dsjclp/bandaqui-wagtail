from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from wagtail.core.models import Page
from .forms import ParticipationForm
from .models import Participation


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
            #
            form.instance.event_page = event_name
            return super().form_valid(form)

from .forms import CustomAuthenticationForm

class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'home/login.html'
    success_message = 'Connexion réussie : bienvenue dans votre espace !'
    extra_context = dict(success_url='/privé')