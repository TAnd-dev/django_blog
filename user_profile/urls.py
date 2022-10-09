from django.urls import path

from user_profile.views import profile, UserProfileEdit, UserPersonalDataEdit, UserPasswordChangeView, logout_view

urlpatterns = [
    path('', profile, name='user_profile'),
    path('edit/', UserProfileEdit.as_view(), name='user_profile_edit'),
    path('personal_edit/', UserPersonalDataEdit.as_view(), name='user_personal_data_edit'),
    path('edit_password/', UserPasswordChangeView.as_view(), name='password_change'),
    path('logout/', logout_view, name='logout')

]
