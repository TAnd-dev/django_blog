from django import template

from shop.models import Basket

register = template.Library()


@register.inclusion_tag('blog/profile_tpl.html')
def show_menu_profile(request):
    baskets = Basket.objects.filter(user=request.user)
    baskets = baskets.count if baskets else 0
    return {'count_basket': baskets, 'request': request}
