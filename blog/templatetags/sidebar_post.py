from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/sidebar_tpl.html')
def show_sidebar():
    most_views = Post.objects.order_by('-views')[:3]
    most_likes = Post.objects.order_by('-likes')[:3]
    return {'most_views': most_views, 'most_likes': most_likes}
