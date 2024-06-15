from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user_auth.forms import UserRegisterForm, UserLoginForm


def user_reg(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            message = 'Вы успешно зарегестрировались. Для большего функционала привяжите почту в настройках профиля'
            messages.success(request, message)
            login(request, user)
            return redirect('blog')
        else:
            message = 'Ошибка регистрации'
            messages.error(request, message)
    else:
        form = UserRegisterForm()
    return render(request, 'user_auth/auth.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = UserLoginForm()
    return render(request, 'user_auth/auth.html', {'form': form})


class MyPasswordResetView(PasswordResetView):
    template_name = 'user_auth/password_reset.html'

    def form_valid(self, form):

        try:
            user_email = User.objects.get(email=form.cleaned_data.get('email'))
        except Exception:
            user_email = None

        if not user_email:
            messages.error(self.request, 'Данный email не зарегестрирован в системе')
            return redirect('password_reset')

        return super().form_valid(form)


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user_auth/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_auth/password_reset_confirm.html'


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user_auth/password_reset_complete.html'
