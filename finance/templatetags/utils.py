import locale
from django.template import Library


register = Library()
locale.setlocale(locale.LC_ALL, '')


@register.filter
def pretty_money(value) -> str:
    if isinstance(value, str):
        value = int(value)
    value = locale.currency(value, grouping=True)
    return value 
