from django import template
from home.models import Trombipiece

register = template.Library()

# Trombipiece snippet
@register.inclusion_tag('home/tags/trombi.html', takes_context=True)
def trombi(context):
    return {
        'trombi': Trombipiece.objects.all(),
        'request': context['request'],
    }