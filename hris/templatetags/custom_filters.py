from django import template

register = template.Library()

@register.filter(name='blank_if_midnight')
def blank_if_midnight(value):
    if value.hour == 0 and value.minute == 0:
        return ''  # Return empty string if midnight
    return value  # Return the original value otherwise

@register.filter
def filter_date(records, date):
    return records.filter(date=date)