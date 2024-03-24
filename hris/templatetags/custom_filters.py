from django import template
from datetime import time

register = template.Library()

@register.filter(name='replace_if_na')
def replace_if_na(value):
    if isinstance(value, time) and value == time(0, 0):
        return 'N/A'
    else:
        return value