from django import template
import os

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]
@register.filter
def con(str1,str2):
    return os.path.join(str1,str2)