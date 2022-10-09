from django.urls import path

from forum.views import Forum, ThemeDetail

urlpatterns = [
    path('', Forum.as_view(), name='forum'),
    path('<str:slug>/', ThemeDetail.as_view(), name='theme_detail'),
]
