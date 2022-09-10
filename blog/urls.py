from django.urls import path

from blog.views import Blog, get_category, get_post

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('category/<str:slug>/', get_category, name='category'),
    path('post/<str:slug>/', get_post, name='post'),
]