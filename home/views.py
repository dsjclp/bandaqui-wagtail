from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from bootstrap_modal_forms.generic import (BSModalLoginView)
from wagtail.core.models import Page


from .forms import CustomAuthenticationForm

class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'home/login.html'
    success_message = 'Connexion réussie : bienvenue dans votre espace !'
    extra_context = dict(success_url='/privé')