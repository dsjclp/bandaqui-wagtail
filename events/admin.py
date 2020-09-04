from django.contrib import admin
from .models import EventCalendar
from .models import EventCalPage
from .models import Participation
from .models import Instrument

admin.site.register(EventCalendar)
admin.site.register(EventCalPage)
admin.site.register(Participation)
admin.site.register(Instrument)
