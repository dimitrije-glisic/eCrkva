from django import template

register = template.Library()

@register.filter(name='div')
def division(value,arg):
    try:
        return int(value) / int(arg)
    except:
        return None

@register.filter(name='mul')
def multiplication(value,arg):
    return value * arg


@register.filter(name='kljuc')
def kljuc(value,arg):
    return value[arg]

@register.filter(name='minus')
def minus(value,arg):
    return arg - value