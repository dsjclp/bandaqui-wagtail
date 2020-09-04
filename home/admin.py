from django.contrib import admin
from wagtail.core.models import Page
from django.contrib.contenttypes.admin import GenericTabularInline

admin.site.register(Page)
