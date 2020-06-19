from django import forms

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

from .models import Participation

from django.shortcuts import get_object_or_404, render
from .models import Instrument


class ParticipationForm(BSModalForm):

    class Meta:
        model = Participation
        fields = ['choice','instrument',]


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']