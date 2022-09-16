from django.urls import path

from blog.views import Blog, PostByCategory, PostDetail, PostByTag, Search

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('category/<str:slug>/', PostByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostByTag.as_view(), name='tag'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail'),
    path('post/', Search.as_view(), name='search'),
]