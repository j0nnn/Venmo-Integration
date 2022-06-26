from django import template

register = template.Library()

@register.filter
def mod(num, val):
    return num % val

@register.filter
def pad(num):
    if num < 10:
        return "0" + str(num)
    return num
