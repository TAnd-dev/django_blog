from django.urls import path

from blog.views import Blog, PostByCategory, PostDetail, PostByTag, Search, AddPost, MyPosts

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('my_posts', MyPosts.as_view(), name='my_posts'),
    path('category/<str:slug>/', PostByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostByTag.as_view(), name='tag'),
    path('post/add_post/', AddPost.as_view(), name='add_post'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail'),
    path('post/', Search.as_view(), name='search'),
]