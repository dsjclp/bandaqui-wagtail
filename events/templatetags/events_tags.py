from django import template
from events.models import Instrument

register = template.Library()

# Instrument snippet
@register.inclusion_tag('home/tags/instruments.html', takes_context=True)
def instruments(context):
    return {
        'instruments': Instrument.objects.all(),
        'request': context['request'],
    }