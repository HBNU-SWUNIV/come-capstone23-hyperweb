from django import template

register = template.Library()

@register.filter(name='remove_extension')
def remove_extension(value, arg):
    return value.replace(arg, '')
