import datetime

from django import template
from django.utils import timezone

from blog.models import Post, Tag

register = template.Library()


@register.inclusion_tag('blog/sidebar_tpl.html')
def show_sidebar():
    most_likes = Post.objects.filter(
        created_date__gte=(timezone.now() - datetime.timedelta(days=7))).order_by('-likes')[:3]
    tags = Tag.objects.order_by('tag_name')
    return {'most_likes': most_likes, 'tags': tags}
