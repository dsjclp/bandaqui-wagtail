from django.urls import include, path
from django.conf.urls import url
from . import views

app_name = 'events'

urlpatterns = [
    path('events.json', views.events_json, name='events.json'),
    path('participation/create/<slug:eventid>/', views.ParticipationCreateView.as_view(), name='create_participation'),
    path('participationajax/create/<slug:eventid>/', views.participationajax_create, name='participationajax_create'),
]
