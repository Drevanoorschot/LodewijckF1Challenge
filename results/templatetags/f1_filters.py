from django import template

register = template.Library()


@register.filter(name='unpack_dict')
def unpack_dict(value, val):
    res = value.get(val)
    if res is None:
        return "-"
    return res
