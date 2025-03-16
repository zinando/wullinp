from django import template

register = template.Library()

@register.filter(name='list_to_string')
def list_to_string(value):
    if isinstance(value, list):
        return ','.join(value)
    return ''

@register.filter(name='none_to_empty')
def none_to_empty(value):
    if value is None or value == 'None' or value == 'null':
        return ''
    return value
