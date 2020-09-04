
from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url

app_name = 'home'

urlpatterns = [
   path('login/', views.CustomLoginView.as_view(), name='login'),
]