from django import template

from shop.models import Basket

register = template.Library()


@register.inclusion_tag('blog/profile_tpl.html')
def show_menu_profile(request):
    categories = Basket.objects.get(user=request.user).quantity
    return {'count_basket': categories, 'request': request}
