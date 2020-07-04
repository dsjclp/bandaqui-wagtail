from django.contrib import admin

from .models import Participation
from .models import Instrument
from wagtail.core.models import Page



from django.contrib.contenttypes.admin import GenericTabularInline


admin.site.register(Participation)
admin.site.register(Instrument)
admin.site.register(Page)
