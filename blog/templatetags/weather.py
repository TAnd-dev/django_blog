from django import template
import requests
from geopy.geocoders import Nominatim
from user_profile.models import UserProfile

register = template.Library()


@register.inclusion_tag('blog/weather_tpl.html')
def show_weather(request):
    # api ключ яндекс погоды
    api_key = 'your-api-key'

    try:
        city_name = UserProfile.objects.values('city').get(user=request.user)
        city_name = city_name.get('city') if city_name.get('city') else 'Moscow'
    except Exception:
        city_name = 'Moscow'

    geolocator = Nominatim(user_agent='django_blog')
    location = geolocator.geocode(city_name)
    lat = location.latitude
    lon = location.longitude

    url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}'
    res = requests.get(url, headers={'X-Yandex-API-Key': api_key}).json()

    try:
        city_info = {
            'city': city_name,
            'temp': res['fact']['temp'],
            'icon': f'https://yastatic.net/weather/i/icons/funky/dark/{res["fact"]["icon"]}.svg',
        }
    except Exception:
        city_info = {
            'error': 'Неизвестный город'
            }

    return city_info
