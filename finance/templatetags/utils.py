import locale
from django.template import Library


register = Library()


@register.filter
def pretty_money(value, prefix='Rp') -> str:
    if not isinstance(value, int):
        value = int(value)
    return f'{prefix}{value:,.0f}'
