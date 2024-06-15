from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path

from user_auth.views import user_login, user_reg, MyPasswordResetView, MyPasswordResetDoneView, \
    MyPasswordResetConfirmView, MyPasswordResetCompleteView

urlpatterns = [
    path('login/', user_login, name='login'),
    path('reg/', user_reg, name='reg'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
