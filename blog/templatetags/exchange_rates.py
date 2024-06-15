import requests
from django import template

register = template.Library()


@register.inclusion_tag('blog/exchange_rates.html')
def show_exchange_rates():
    api_key = 'd7e35e735ec43194f26fb81c950f7637'
    url = f'https://currate.ru/api/?get=rates&pairs=USDRUB&key={api_key}'
    res = requests.get(url).json()
    return {'rate': res['data']['USDRUB'][:-2]}
