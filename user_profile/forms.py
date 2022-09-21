from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput, ImageField, models

from user_profile.models import UserProfile


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = CharField(
        required=True,
        label='Старый пароль',
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Обязательное поле'})

    new_password1 = CharField(
        required=True,
        label='Новый пароль',
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Обязательное поле'})

    new_password2 = CharField(
        required=True,
        label='Пароль еще раз)',
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Обязательное поле'})


class UpdateProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
        widgets = {'profile_pic': forms.FileInput(attrs={'class': 'form-control'})}
