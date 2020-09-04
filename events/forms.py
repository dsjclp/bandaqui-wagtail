from django import forms
from .models import Participation
from .models import Instrument
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm
from django.shortcuts import get_object_or_404, render
from wagtail.core.models import Page

class ParticipationForm(BSModalForm):

    class Meta:
        model = Participation
        fields = ['choice','instrument',]

class Participation2Form(forms.ModelForm):

    class Meta:
        model = Participation
        fields = ['event_page','choice','instrument',]
        widgets = {'event_page': forms.HiddenInput()}

    def __init__(self, eventid, *args, **kwargs):
        super(Participation2Form, self).__init__(*args, **kwargs)
        self.fields['choice'].label = 'Votre choix'
        self.fields['instrument'].label = 'Votre instrument'
        event = get_object_or_404(Page, slug=eventid)
        self.fields['event_page'].initial = event
        self.fields['event_page'].label = ''
    