from django import template

from shop.models import Category

register = template.Library()


@register.inclusion_tag('shop/sidebar_shop.html')
def show_shop_sidebar():
    categories = Category.objects.all()
    return {'categories': categories}
