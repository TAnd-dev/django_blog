from django.urls import path

from user_profile.views import profile, UserProfileEdit, UserPersonalDataEdit, UserPasswordChangeView, logout_view, \
    VerifyEmail, verify_error

urlpatterns = [
    path('', profile, name='user_profile'),
    path('verify_email/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify_email'),
    path('verify_error', verify_error, name='verify_error'),
    path('edit/', UserProfileEdit.as_view(), name='user_profile_edit'),
    path('personal_edit/', UserPersonalDataEdit.as_view(), name='user_personal_data_edit'),
    path('edit_password/', UserPasswordChangeView.as_view(), name='password_change'),
    path('logout/', logout_view, name='logout')

]
