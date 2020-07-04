from django.conf.urls import url
from . import views


app_name = 'pieces'

urlpatterns = [
    url(r'^tag/(?P<tag>[-\w]+)/', views.tag_view, name="tag"),
    url(r'^category/(?P<category>[-\w]+)/', views.category_view, name="category"),
]
