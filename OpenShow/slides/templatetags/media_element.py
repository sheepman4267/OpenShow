from django import template
from django.shortcuts import get_object_or_404

register = template.Library()

@register.inclusion_tag('media_element_base.html')
def media_element(media_object, **kwargs):
    context = {
        'media_object': media_object,
    }
    return context
