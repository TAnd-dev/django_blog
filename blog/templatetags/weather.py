from django import template
import requests

from user_profile.models import UserProfile

register = template.Library()


@register.inclusion_tag('blog/weather_tpl.html')
def show_weather(request):
    api_key = 'f49a157cfe4fc37eb3d80ba28dfd9562'

    try:
        city_name = UserProfile.objects.values('city').get(user=request.user)
        city_name = city_name.get('city') if city_name.get('city') else 'Moscow'
    except Exception:
        city_name = 'Moscow'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}'
    res = requests.get(url).json()

    try:
        city_info = {
            'city': city_name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
        }
    except Exception:
        city_info = {
            'error': 'Неизвестный город'
            }
    return city_info
