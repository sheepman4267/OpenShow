import base64

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def base64_string(value):
    return base64.b64encode(bytes(value, encoding="utf-8")).decode("utf-8")
