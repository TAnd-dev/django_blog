from django.urls import path

from user_auth.views import user_login, user_reg

urlpatterns = [
    path('login/', user_login, name='login'),
    path('reg/', user_reg, name='reg'),

]
