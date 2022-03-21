from django import template

register = template.Library()


@register.filter(name='unpack_dict')
def unpack_dict(value, val):
    res = value.get(val)
    if res is None:
        return "-"
    return res


@register.filter(name='shorten')
def shorten(value):
    return value[:3].upper()
