from django import template
from home.models import Instrument
from home.models import Partition
from home.models import Trombipiece

register = template.Library()


# Instrument snippet
@register.inclusion_tag('home/tags/instruments.html', takes_context=True)
def instruments(context):
    return {
        'instruments': Instrument.objects.all(),
        'request': context['request'],
    }

# Partition snippet
@register.inclusion_tag('home/tags/partitions.html', takes_context=True)
def partitions(context):
    return {
        'partitions': Partition.objects.all(),
        'request': context['request'],
    }

# Trombipiece snippet
@register.inclusion_tag('home/tags/trombi.html', takes_context=True)
def trombi(context):
    return {
        'trombi': Trombipiece.objects.all(),
        'request': context['request'],
    }