from django.urls import include, path
from . import views

#app_name = 'core'

urlpatterns = [
    path('events.json', views.events_json, name='events.json'),
]
